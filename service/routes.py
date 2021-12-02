"""
Order Service

Paths:
------
GET / - Displays a UI for Selenium testing

# Orders service providing REST APIs to support CRUD + List + Cancel + Query operations on orders
# and order items
"""

from flask import jsonify, request, url_for, make_response, abort
from flask_restx import Api, Resource, fields, reqparse, inputs
from werkzeug.exceptions import NotFound
from service.models import Order, OrderStatus
from . import status  # HTTP Status Codes

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import Order, OrderItem, DataValidationError

# Import Flask application
from . import app

######################################################################
# GET HEALTH CHECK
######################################################################
@app.route("/healthcheck")
def healthcheck():
    """Let them know our heart is still beating"""
    return make_response(jsonify(status=200, message="Healthy"), status.HTTP_200_OK)


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return app.send_static_file("index.html")

######################################################################
# Configure Swagger before initializing it
######################################################################
api = Api(app,
          version='1.0.0',
          title='Orders REST API Service',
          description='This is the back end for an eCommerce web site as a RESTful microservice for the resource order.',
          default='orders',
          default_label='Orders operations',
          doc='/apidocs',
          prefix='/api'
          )

# Define the OrderItem model so that the docs reflect what can be sent
create_item_model = api.model('OrderItem', {
    'item_id': fields.Integer(required=True,
                              description='The product ID that identifies the item'),
    'item_name': fields.String(required=True,
                               description='The name of the item'),
    'item_qty': fields.Integer(required=True,
                                descrption='Quantity for the item'),
    'item_price': fields.Float(required=True,
                              description='Price of the item'),  
    'order_id' : fields.Integer(readOnly=True,
                                  description='The order id that the item corresponds to'),

})

item_model = api.inherit(
    'OrderItemModel',
    create_item_model,
    {
        'id': fields.Integer(readOnly=True,
                                  description='The unique item id assigned internally by service'),
                                          
    }
)
# Define the order model so that the docs reflect what can be sent
create_order_model = api.model('Order', {
    'cust_id': fields.Integer(required=True,
                          description='Customer ID for the customer who placed the order'),
    'status': fields.String(required=True,
                              description='Status of the order', enum = ['Received', 'Processing', 'Cancelled'])
})

order_model = api.inherit(
    'OrderModel', 
    create_order_model,
    {
        'id': fields.Integer(readOnly=True,
                            description='The unique order id assigned internally by service'),
        'order_items': fields.List(fields.Nested(create_item_model, required=True), required=True,
                               description='Items in the Order')
        
    }
)

# query string arguments
order_args = reqparse.RequestParser()
order_args.add_argument('cust_id', type=int, required=False, help='List Orders by cust_id')
order_args.add_argument('item_id', type=int, required=False, help='List Orders by item_id')


# query string arguments
list_items_args = reqparse.RequestParser()
list_items_args.add_argument('order_id', type=int, required=True, help='List All items by order_id')

######################################################################
# Special Error Handlers
######################################################################
@api.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    message = str(error)
    app.logger.error(message)
    return {
        'status_code': status.HTTP_400_BAD_REQUEST,
        'error': 'Bad Request',
        'message': message
    }, status.HTTP_400_BAD_REQUEST

######################################################################

######################################################################
#  PATH: /orders/{id}
######################################################################
@api.route("/orders/<int:order_id>", strict_slashes=False)
@api.param('order_id', 'The Order identifier')
class OrderResource(Resource):
    """
    OrderResource class
    Allows the manipulation of a single Order
    GET /order{id} - Returns an Order with the id
    PUT /order{id} - Update an Order with the id
    DELETE /order{id} -  Deletes an Order with the id
    """

    # ------------------------------------------------------------------
    # RETRIEVE AN ORDER
    # ------------------------------------------------------------------
    @api.doc('get_order')
    @api.response(404, 'Order not found')
    @api.marshal_with(order_model)
    def get(self, order_id):
        """
        Retrieve a single order
        This endpoint will return an Order based on it's id
        """
        app.logger.info("Request for order with id: %s", order_id)
        order = Order.find(order_id)
        if not order:
            abort(status.HTTP_404_NOT_FOUND, "Order was not found.")
        return order.serialize(), status.HTTP_200_OK



######################################################################
#  PATH: /orders
######################################################################
@api.route('/orders', strict_slashes=False)
class OrderCollection(Resource):
    """ Handles all interactions with Orders """
    
    ######################################################################
    # LIST ALL ORDERS
    ######################################################################
    @api.doc('list_orders')
    @api.expect(order_args, validate=True)
    @api.marshal_list_with(order_model)
    def get(self):
        """Returns all of the Orders"""
        app.logger.info("Request for order list")
        orders = []
        args = order_args.parse_args()

        if args['cust_id']:
            app.logger.info('Filtering by cust_id: %s', args['cust_id'])
            orders = Order.find_by_customer(args['cust_id'])
        elif args['item_id']:
            app.logger.info('Filtering by item_id: %s', args['item_id'])
            orders = Order.find_by_item(args['item_id'])
        else:
            app.logger.info('Find all')
            orders = Order.all()
        results = [order.serialize() for order in orders]
        app.logger.info("Returning %d orders", len(results))
        return results, status.HTTP_200_OK


    #------------------------------------------------------------------
    # CREATE AN ORDER
    #------------------------------------------------------------------
    @api.doc('create_order')
    @api.response(400, 'The posted data was not valid')
    @api.expect(create_order_model)
    @api.marshal_with(order_model, code=201)
    def post(self):
        """
        Creates an Order
        This endpoint will create an Order based the data in the body that is posted
        """
        app.logger.info('Request to Create an Order')

        check_content_type("application/json")
        order = Order()
        app.logger.debug('Payload = %s', api.payload)
        order.deserialize(api.payload)
        order.create()        
        app.logger.info("Order with ID [%s] created.", order.id)
        location_url = api.url_for(OrderResource, order_id=order.id, _external=True)
        return order.serialize(), status.HTTP_201_CREATED, {'Location': location_url}


######################################################################
#  PATH: /orders
######################################################################
@api.route('/orders/<int:order_id>/items', strict_slashes=False)
class OrderItemCollection(Resource):
    """ Handles all interactions with Orders """
    
    ######################################################################
    # LIST ALL ITEMS IN AN ORDER
    ######################################################################
    @api.doc('list_order_item')
    @api.expect(list_items_args, validate=True)
    @api.marshal_list_with(item_model)
    def get(self, order_id):
        """
        Get all items in an order
        This endpoint will return a list of items in an Order based on it's order_id
        """
        app.logger.info("Request all items for order with id: %s", order_id)
        order = Order.find(order_id)
        if not order:
            raise NotFound("Order with id '{}' was not found.".format(order_id))
        items_list = []
        for item in order.order_items:
            items_list.append(item.serialize())
        app.logger.info("Returning items in order: %s", order.id)
        return items_list, status.HTTP_200_OK
        
    #------------------------------------------------------------------
    # ADD ITEM TO ORDER
    #------------------------------------------------------------------
    @api.doc('add_item')
    @api.response(400, 'The posted data was not valid')
    @api.expect(create_item_model)
    @api.marshal_with(item_model, code=201)
    def post(self, order_id):
        """
        Add an Item
        This endpoint will add an Item to the Order based the data in the body and the order_id
        """
        app.logger.info('Request to add an item')

        check_content_type("application/json")

        order = Order.find_or_404(order_id)
        order_item = OrderItem()
        app.logger.debug('Payload = %s', api.payload)
        order_item.deserialize(api.payload)
        order.order_items.append(order_item)
        order.save()    
        app.logger.info("Item with ID [%s] added.", order_item.id)
        location_url = api.url_for(OrderItemResource, order_id=order.id, item_id = order_item.id, _external=True)
        return order_item.serialize(), status.HTTP_201_CREATED, {'Location': location_url}

######################################################################
# DELETE ORDER
######################################################################
@app.route("/orders/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    """
    Deletes an Order
    This endpoint will delete an Order based on the id specified in the path
    """
    app.logger.info("Request to delete order with id: %s", order_id)
    order = Order.find(order_id)
    if order:
        order.delete()

    app.logger.info("Order with ID [%s] delete complete.", order_id)
    return make_response("", status.HTTP_204_NO_CONTENT)

######################################################################
# UPDATE AN EXISTING ORDER
######################################################################
@app.route("/orders/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    """
    Update an Order
    This endpoint will update an Order's cust_id based the id that is posted
    """
    app.logger.info("Request to update order with id: %s", order_id)
    check_content_type("application/json")
    order = Order.find(order_id)
    if not order:
        raise NotFound("Order with id '{}' was not found.".format(order_id))
    order.deserialize(request.get_json())
    order.id = order_id
    order.save()
    return make_response(jsonify(order.serialize()), status.HTTP_200_OK)

######################################################################
# UPDATE AN EXISTING ORDER'S ITEMS
######################################################################
@app.route("/orders/<int:order_id>/items/<int:item_id>", methods=["PUT"])
def update_order_item(order_id, item_id):
    """
    Update an item in an Order
    This endpoint will update an Order's item based the id that is posted
    """
    app.logger.info("Request to update the item id: %s in order id: %s", item_id, order_id)
    check_content_type("application/json")
    order = Order.find(order_id)
    if not order:
        raise NotFound("Order with id '{}' was not found.".format(order_id))
    item_found = False
    return_item = None
    for item in order.order_items:
        if item.id == item_id:
            item_found = True
            item.deserialize(request.get_json())
            item.id = item_id
            item.save()
            order.save()
            return_item = item
            break
    if not item_found:
        raise NotFound("Item with id '{}' was not found.".format(item_id))
    return make_response(jsonify(return_item.serialize()), status.HTTP_200_OK)





######################################################################
#  PATH: /orders/{order_id}/items/{item_id}
######################################################################
@api.route('/orders/<int:order_id>/items/<int:item_id>', strict_slashes=False)
@api.param('order_id', 'The Order identifier')
@api.param('item_id', 'The Order Item identifier')
class OrderItemResource(Resource):
    """
    OrderItemResource class
    Allows the manipulation of a single Order Item
    GET /orders/{order_id}/items/{item_id} - Retrieve an Order Item with the id
    """
    # ------------------------------------------------------------------
    # RETRIEVE AN ITEM IN AN ORDER
    # ------------------------------------------------------------------
    @api.doc('get_order_item')
    @api.response(404, 'Item not found')
    @api.marshal_with(item_model)
    def get(self, order_id, item_id):
        """
        Read an Item in an Order
        This endpoint will get an Item based on the order_id and item_id specified in the path
        """
        app.logger.info("Request to read an item in order %s with item_id: %s", order_id, item_id)
        order = Order.find(order_id)

        if not order:
            abort(status.HTTP_404_NOT_FOUND, "Order was not found.")
        item_found = False
        item_obj = None
        for item in order.order_items:
            if item.id == item_id:
                item_found = True
                item_obj = item.serialize()
                break
        if not item_found:
            abort(status.HTTP_404_NOT_FOUND, "Item was not found.")
        print(item_obj)
        return item_obj, status.HTTP_200_OK



######################################################################
# DELETE AN ITEM IN AN ORDER
######################################################################
@app.route("/orders/<int:order_id>/items/<int:item_id>", methods=["DELETE"])
def delete_item(order_id, item_id):
    """
    Delete an Item in an Order
    This endpoint will delete an Item based on the order_id and item_id specified in the path
    """
    app.logger.info("Request to delete an item in order %s with item_id: %s", order_id, item_id)
    order = Order.find(order_id)
    
    if order:
        for item in order.order_items:
            if item.id == item_id:
                item_found = True
                item.delete()
                order.save()
                break
    
    app.logger.info("Item with ID [%s] in order %s is deleted.", item_id, order_id)
    
    return make_response("", status.HTTP_204_NO_CONTENT)


######################################################################
# CANCEL AN ORDER
######################################################################
@app.route('/orders/<int:order_id>/cancel', methods=['PUT'])
def cancel_orders(order_id):
    """
    Cancel an Order
    This endpoint will update an Order based the body that is posted
    """
    order = Order.find(order_id)
    if not order:
        raise NotFound("Order with id '{}' was not found.".format(order_id))
    order.status = OrderStatus.Cancelled
    order.save()
    return make_response(jsonify(order.serialize()), status.HTTP_200_OK)




######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def abort(error_code: int, message: str):
    """Logs errors before aborting"""
    app.logger.error(message)
    api.abort(error_code, message)

def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        "Content-Type must be {}".format(media_type),
    )
