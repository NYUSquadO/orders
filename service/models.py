"""
Models for Order

All of the models are stored in this module
"""
import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

def init_db(app):
    """Initialies the SQLAlchemy app"""
    Order.init_db(app)

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """

    pass

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    item_id = db.Column(db.Integer) #Product ID
    item_name = db.Column(db.String(100), nullable=False) #Product name
    item_qty = db.Column(db.Integer)
    item_price = db.Column(db.Float)


    def serialize(self):
        """
        Serializes OrderItem into dictionary
        """
        return {
            "id" : self.id,
            "order_id" : self.order_id,
            "item_id" : self.item_id,
            "item_name" : self.item_name,
            "item_qty" : self.item_qty,
            "item_price" : self.item_price
        }

    def deserialize(self, data):
        """ 
        Deserializes OrderItem from a dictionary
        """
        try:
            self.order_id = data["order_id"]
            self.item_id = data["item_id"]
            self.item_name = data["item_name"]
            self.item_qty = data["item_qty"]
            self.item_price = data["item_price"]
        except KeyError as error:
            raise DataValidationError(
                "Invalid OrderItem: missing " + error.args[0]
            )
        except TypeError as error:
            raise DataValidationError(
                "Invalid OrderItem: body of request contained bad or no data"
            )
        return self


class Order(db.Model):
    """
    Class that represents a Order
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True) #Order ID
    cust_id  = db.Column(db.Integer)             #Customer ID for the order
    order_items = db.relationship('OrderItem', backref='order', lazy = True, cascade = "all,delete") #Items in the order

    def __repr__(self):
        return "<Order id=[%s] placed by cust_id=[%s]>" % (self.id, self.cust_id)

    def create(self):
        """
        Creates an Order to the database
        """
        logger.info("Creating order for customer :: %s", self.cust_id)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def save(self):
        """
        Updates an Order to the database
        """
        logger.info("Saving order for customer :: %s", self.cust_id)
        db.session.commit()

    def delete(self):
        """ Removes an Order from the data store """
        logger.info("Deleting order for customer :: %s", self.cust_id)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes an Order into a dictionary """
        return {
            "id": self.id, 
            "cust_id": self.cust_id,
            "order_items": [order_item.serialize() for order_item in self.order_items]}

    def deserialize(self, data):
        """
        Deserializes an Order from a dictionary

        Args:
            data (dict): A dictionary containing the order data
        """
        try:    
            self.cust_id = data["cust_id"]
            order_items = data["order_items"]
            for order_item in order_items:
                self.order_items.append(OrderItem(order_id = order_item['order_id'], item_id = order_item['item_id'] , \
                    item_name = order_item['item_name'] , item_qty = order_item['item_qty'], item_price = order_item['item_price'] ))
        except KeyError as error:
            raise DataValidationError(
                "Invalid Order: missing " + error.args[0]
            )
        except TypeError as error:
            raise DataValidationError(
                "Invalid Order: body of request contained bad or no data"
            )
        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the Orders in the database """
        logger.info("Processing all Orders")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a Order by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    #@classmethod
    #def find_or_404(cls, by_id):
        """ Find a Order by it's id """
        #logger.info("Processing lookup or 404 for id %s ...", by_id)
        #return cls.query.get_or_404(by_id)

    #@classmethod
    #def find_by_name(cls, name):
        """Returns all Orders with the given name

        Args:
            name (string): the name of the Orders you want to match
        """
        #logger.info("Processing name query for %s ...", name)
        #return cls.query.filter(cls.name == name)
