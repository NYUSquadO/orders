"""
Models for Order

All of the models are stored in this module
"""
import logging
from flask_sqlalchemy import SQLAlchemy
from enum import Enum

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
    """Class that represents OrderItem model"""    
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
        Deserializes a OrderItem from a dictionary
        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            # self.order_id = data["order_id"]
            if isinstance(data["item_id"], int):
                self.item_id = data["item_id"]
            else:
                raise DataValidationError("Invalid type for int [item_id]: " + type(data["item_id"]))
            if isinstance(data["item_name"], str):
                self.item_name = data["item_name"]
            else:
                raise DataValidationError("Invalid type for int [item_name]: " + type(data["item_name"]))
            if isinstance(data["item_qty"], int):
                self.item_qty = data["item_qty"]
            else:
                raise DataValidationError("Invalid type for int [item_qty]: " + type(data["item_qty"]))
            if isinstance(data["item_price"], float):
                self.item_price = data["item_price"]
            else:
                raise DataValidationError("Invalid type for int [item_price]: " + type(data["item_price"]))
        except KeyError as error:
            raise DataValidationError("Invalid OrderItem: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid OrderItem: details of OrderItem contained bad or no data"
            )
        return self

    def delete(self):
        """ Removes an Item from the order"""
        logger.info("Deleting an item from order %s", self.order_id)
        
        db.session.delete(self)
        db.session.commit()

    def save(self):
        """
        Updates an item in an Order to the database
        """
        logger.info("Saving item in order :: %s", self.item_id)
        db.session.commit()

    @classmethod
    def all(cls):
        """ Returns all of the Orders in the database """
        logger.info("Processing all OrderItems")
        return cls.query.all()

    @classmethod
    def find_by_item(cls,item_id):
        """Returns all orders containing the specified item id"""
        return cls.query.filter(cls.item_id==item_id)

class OrderStatus(Enum):
    """ Enumeration of valid Order Status """
    Received = 0
    Processing = 1
    Cancelled = 2

class Order(db.Model):
    """
    Class that represents a Order
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True) #Order ID
    cust_id  = db.Column(db.Integer)             #Customer ID for the order
    order_items = db.relationship('OrderItem', backref='order', lazy = True, \
        cascade = "all,delete") #Items in the order
    status = db.Column(db.Enum(OrderStatus), nullable=False, server_default=(OrderStatus.Received.name)) # status of the order

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
            "order_items": [order_item.serialize() for order_item in self.order_items],
            "status": self.status.name if self.status else None
            }

    def deserialize(self, data):
        """
        Deserializes an Order from a dictionary

        Args:
            data (dict): A dictionary containing the order data
        """
        try:    
            self.cust_id = int(data["cust_id"])
            order_items = data["order_items"]
            for order_item in order_items:
                self.order_items.append(OrderItem(item_id = order_item['item_id'] , \
                    item_name = order_item['item_name'] , item_qty = order_item['item_qty'], \
                    item_price = order_item['item_price'] ))

        except KeyError as error:
            raise DataValidationError(
                "Invalid Order: missing " + error.args[0]
            )
        except TypeError as error:
            raise DataValidationError(
                "Invalid Order: body of request contained bad or no data: " + error.args[0])
        except  ValueError as error:
                raise DataValidationError(
                "Invalid Order: cust_id must be int " + error.args[0]
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
        logger.info("Processing lookup for order id %s ...", by_id)
        return cls.query.get(by_id)
        
    @classmethod
    def find_or_404(cls, by_id):
        """ Find a Order by it's id """
        logger.info("Processing lookup or 404 for order id %s ...", by_id)
        return cls.query.get_or_404(by_id)

    @classmethod
    def find_by_customer(cls, customer_id) :
        """Returns all orders for the specified customer ID"""
        logger.info("Finding all orders for the specified customer ID %s", customer_id)
        return cls.query.filter(cls.cust_id == customer_id)

    @classmethod
    def find_by_item(cls, item_id):
        """Returns all orders for the specified item ID"""
        logger.info("Finding all orders for the specified item ID %s", item_id)
        return cls.query.join(
            OrderItem
        ).filter(Order.id==OrderItem.order_id).filter(OrderItem.item_id==item_id).all()



