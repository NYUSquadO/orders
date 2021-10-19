"""
Order Service

# TODO: Describe what service does here
A collection of order items created from products and quantity
"""

from flask import jsonify, request, url_for, make_response, abort

from werkzeug.exceptions import NotFound
from service.models import Order
from . import status  # HTTP Status Codes

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import Order, OrderItem

# Import Flask application
from . import app

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return (
        jsonify(
            name="Orders REST API Service",
            version="1.0",
            paths=url_for("list_orders", _external=True),
        ),
        status.HTTP_200_OK,
    )

######################################################################
# CREATE ORDER
######################################################################
@app.route("/orders", methods=["POST"])
def create_order():
    """
    Creates an Order
    This endpoint will create an Order based the data in the body that is posted
    """
    app.logger.info("Request to create an Order")
    check_content_type("application/json")
    order = Order()
    order.deserialize(request.get_json())
    order.create()
    message = order.serialize()
    location_url = url_for("get_order", order_id=order.id, _external=True)

    app.logger.info("Order with ID [%s] created.", order.id)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

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
# LIST ALL ORDERS
######################################################################
@app.route("/orders", methods=["GET"])
def list_orders():
    """Returns all of the Orders"""
    app.logger.info("Request for order list")
    orders = []
    orders = Order.all()
    results = [order.serialize() for order in orders]
    app.logger.info("Returning %d orders", len(results))
    return make_response(jsonify(results), status.HTTP_200_OK)

######################################################################
# RETRIEVE AN ORDER
######################################################################
@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    """
    Retrieve a single order
    This endpoint will return an Order based on it's id
    """
    app.logger.info("Request for order with id: %s", order_id)
    order = Order.find(order_id)
    if not order:
        raise NotFound("Order with id '{}' was not found.".format(order_id))

    app.logger.info("Returning order: %s", order.id)
    return make_response(jsonify(order.serialize()), status.HTTP_200_OK)

######################################################################
# ADD ITEM
######################################################################
@app.route("/orders/<int:order_id>/items", methods=["POST"])
def add_item(order_id):
    """
    Add an Item
    This endpoint will add an Item to the Order based the data in the body and the order_id
    """
    app.logger.info("Request to add an item")
    check_content_type("application/json")
    order = Order.find_or_404(order_id)
    order_item = OrderItem()
    order_item.deserialize(request.get_json())
    order.order_items.append(order_item)
    order.save()
    message = order_item.serialize()
    # location_url = url_for("get_item", order_id=order.id, item_id=order_item.id, _external=True)
    location_url = "To be implemented"

    app.logger.info("Item with ID [%s] added.", order_item.id)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

######################################################################
# LIST ALL ITEMS IN AN ORDER
######################################################################
@app.route("/orders/<int:order_id>/items", methods=["GET"])
def get_items_in_order(order_id):
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
    return make_response(jsonify(items_list), status.HTTP_200_OK)

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
    
    if not order:
        raise NotFound("Order with id '{}' was not found.".format(order_id))
    item_found = False
    for item in order.order_items:
        if item.id == item_id:
            item_found = True
            item.delete()
            order.save()
            break
    if not item_found:
        raise NotFound("Item with id '{}' was not found.".format(item_id))
    # item = order.order_items.find(item_id)
    # if item:
    #     item.delete()
    #     order.save()
    app.logger.info("Item with ID [%s] in order %s is deleted.", item_id, order_id)
    
    return make_response("", status.HTTP_204_NO_CONTENT)

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


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
