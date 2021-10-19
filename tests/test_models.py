"""
Test cases for Order Model

"""
import logging
import unittest
import os
from service.models import Order, OrderItem, DataValidationError, db
from service import app

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)

######################################################################
#  O R D E R   M O D E L   T E S T   C A S E S
######################################################################
class TestOrder(unittest.TestCase):
    """ Test Cases for Order Model """
    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Order.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables
        self.order = Order(cust_id = 999, order_items = [OrderItem(order_id = 1, item_id = 2000, \
            item_name = "IPHONE 13 PRO", \
            item_qty = 1, item_price = 1500)])


    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_order(self):
        """ Test order created successfully"""
        self.assertTrue(self.order is not None)
        self.assertEqual(self.order.id, None)
        self.assertEqual(self.order.cust_id, 999)
        self.assertEqual(len(self.order.order_items), 1)
        self.assertEqual(self.order.order_items[0].order_id, 1)
        self.assertEqual(self.order.order_items[0].item_id, 2000)
        self.assertEqual(self.order.order_items[0].item_name, "IPHONE 13 PRO")
        self.assertEqual(self.order.order_items[0].item_qty, 1)
        self.assertEqual(self.order.order_items[0].item_price, 1500)

    def test_add_order(self):
        """Test order added to database"""
        orders = Order.all()
        self.assertEqual(orders, [])        
        self.assertTrue(self.order is not None)
        self.assertEqual(self.order.id, None)
        self.order.create()
        self.assertEqual(self.order.id, 1)
        orders = Order.all()
        self.assertEqual(len(orders), 1)

    def test_update_order(self):
        """Test order updated to database"""
        self.order.create()
        self.assertEqual(self.order.id, 1)
        self.order.cust_id = 1234
        self.order.order_items[0].item_qty = 2
        original_order_id = self.order.id
        self.order.save()
        self.assertEqual(self.order.id, original_order_id)
        self.assertEqual(self.order.cust_id, 1234)
        self.assertEqual(self.order.order_items[0].item_qty, 2)
        #Fetch order back and check order ID has not changed but order details updated
        orders = Order.all()
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0].id, original_order_id)
        self.assertEqual(orders[0].cust_id, 1234)
        self.assertEqual(orders[0].order_items[0].item_qty, 2)

    def test_delete_order(self):
        """ Delete Order """
        self.order.create()
        self.assertEqual(len(Order.all()), 1)
        # delete the order and make sure it isn't in the database
        self.order.delete()
        self.assertEqual(len(Order.all()), 0)

    def test_serialize_order(self):
        """ Test serialization of Order """
        data = self.order.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], self.order.id)
        self.assertIn("cust_id", data)
        self.assertEqual(data["cust_id"], self.order.cust_id)
        self.assertIn("order_items", data)

        order_items = data["order_items"]
        self.assertEqual(len(order_items), 1)

        order_item = order_items[0]

        self.assertIn("id", order_item)
        self.assertIn("order_id", order_item)
        self.assertIn("item_id", order_item)
        self.assertIn("item_name", order_item)
        self.assertIn("item_qty", order_item)
        self.assertIn("item_price", order_item)

        actual_order_item = self.order.order_items[0]

        self.assertEqual(order_item["id"], actual_order_item.id)
        self.assertEqual(order_item["order_id"], actual_order_item.order_id)
        self.assertEqual(order_item["item_id"], actual_order_item.item_id)
        self.assertEqual(order_item["item_name"], actual_order_item.item_name)
        self.assertEqual(order_item["item_qty"], actual_order_item.item_qty)
        self.assertEqual(order_item["item_price"], actual_order_item.item_price)


    def test_deserialize_order(self):
        """ Test deserialization of Order """
        data = {
            "id": 1,
            "cust_id": 777,
            "order_items": [{
                "id" : 1,
                "order_id" : 1,
                "item_id" : 234,
                "item_name" : "Lenovo Thinkpad",
                "item_qty" : 1,
                "item_price" : 2000
            }]}
        order = Order()
        order.deserialize(data)
        self.assertNotEqual(order, None)
        self.assertEqual(order.id, None)
        self.assertEqual(order.cust_id, 777)

        order_items = order.order_items
        self.assertEqual(len(order_items), 1)
        order_item = order_items[0]

        self.assertEqual(order_item.id, None)
        self.assertEqual(order_item.order_id, data["order_items"][0]["order_id"])
        self.assertEqual(order_item.item_id, data["order_items"][0]["item_id"])
        self.assertEqual(order_item.item_name, data["order_items"][0]["item_name"])
        self.assertEqual(order_item.item_qty, data["order_items"][0]["item_qty"])
        self.assertEqual(order_item.item_price, data["order_items"][0]["item_price"])

    def test_deserialize_missing_data(self):
        """ Test deserialization of Order with missing data """
        data = {"id": 1, "cust_id": 1234}
        order = Order()
        self.assertRaises(DataValidationError, order.deserialize, data)

    def test_deserialize_bad_data(self):
        """ Test deserialization of bad data """
        data = "this is not a dictionary"
        order = Order()
        self.assertRaises(DataValidationError, order.deserialize, data)

    def test_find_order(self):
        """ Find Order by ID """
        self.order.create()

        #creating another order
        order_2 = Order(cust_id = 345, order_items = [OrderItem(order_id = 2, item_id = 5000, \
            item_name = "Lenovo Thinkpad", \
            item_qty = 1, item_price = 2000)])
        order_2.create()
        # make sure they got updated
        self.assertEqual(len(Order.all()), 2)
        # find the 2nd order in the list
        order_result = Order.find(order_2.id)
        self.assertIsNot(order_result, None)
        self.assertEqual(order_result.id, order_2.id)
        self.assertEqual(order_result.cust_id, order_2.cust_id)
        self.assertEqual(len(order_result.order_items), len(order_2.order_items))
        self.assertEqual(len(order_result.order_items), 1)
        self.assertEqual(order_result.order_items[0].order_id, order_2.order_items[0].order_id)
        self.assertEqual(order_result.order_items[0].item_id, order_2.order_items[0].item_id)
        self.assertEqual(order_result.order_items[0].item_name, order_2.order_items[0].item_name)
        self.assertEqual(order_result.order_items[0].item_qty, order_2.order_items[0].item_qty)
        self.assertEqual(order_result.order_items[0].item_price, order_2.order_items[0].item_price)
