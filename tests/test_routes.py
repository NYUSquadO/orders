"""
TestOrder API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from service import status  # HTTP Status Codes
from service.models import db, init_db
from service.routes import app
from .factories import OrderFactory, OrderItemFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)
BASE_URL = "/orders"
CONTENT_TYPE_JSON = "application/json"

######################################################################
#  T E S T   C A S E S
######################################################################
class TestOrderResourceServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        db.drop_all()  # clean up the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def _create_orders(self, count):
        """Factory method to create orders in bulk"""
        orders = []
        for _ in range(count):
            test_order = OrderFactory()
            resp = self.app.post(
                BASE_URL, json=test_order.serialize(), content_type=CONTENT_TYPE_JSON
            )
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test order"
            )
            new_order = resp.get_json()
            test_order.id = new_order["id"]
            orders.append(test_order)
        return orders


    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """ Test index call """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], "Orders REST API Service")
        self.assertIn("/orders",data["paths"])

    def test_create_order(self):
        """Create Order"""
        test_order = OrderFactory()
        logging.debug(test_order)
        resp = self.app.post(
            BASE_URL, json=test_order.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)
        # Check the data is correct
        new_order = resp.get_json()
        self.assertEqual(new_order["cust_id"], test_order.cust_id, "cust_id do not match")
        # Check that the location header was correct
        resp = self.app.get(location, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_delete_order(self):
        """Delete Order"""
        test_order = self._create_orders(1)[0]
        resp = self.app.delete(
            "{0}/{1}".format(BASE_URL, test_order.id), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # make sure they are deleted
        resp = self.app.get(
            "{0}/{1}".format(BASE_URL, test_order.id), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_order_no_data(self):
        """ Create Order with missing data """
        resp = self.app.post(
            BASE_URL, json={}, content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_no_content_type(self):
        """ Create a Order with no content type """
        resp = self.app.post(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_order_bad_custid(self):
        """ Create Order with bad Customer ID data """
        order = OrderFactory()
        logging.debug(order)
        test_order = order.serialize()
        test_order["cust_id"] = "CUST_ID"    # wrong data type
        resp = self.app.post(
            BASE_URL, json=test_order, content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_order_list(self):
        """List all Orders"""
        self._create_orders(5)
        resp = self.app.get("/orders")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

    def test_get_order(self):
        """Get a single Order"""
        # get the id of an order
        test_order = self._create_orders(1)[0]
        resp = self.app.get(
            "/orders/{}".format(test_order.id), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["id"], test_order.id)

    def test_get_order_not_found(self):
        """Get an Order thats not found"""
        resp = self.app.get("/orders/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_order(self):
        """ Update an existing Order """
        # create an Order to update
        test_order = OrderFactory()
        logging.debug(test_order)
        resp = self.app.post(
            "/orders", json=test_order.serialize(), content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # update the cust_id
        new_order = resp.get_json()
        new_order["cust_id"] = 23
        resp = self.app.put(
            "/orders/{}".format(new_order["id"]),
            json=new_order,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_order = resp.get_json()
        self.assertEqual(updated_order["cust_id"], 23)

    def test_update_order_not_found(self):
        """Try to Update an non-existing Order"""
        test_order = OrderFactory()
        resp = self.app.put("/orders/0", json=test_order.serialize(),content_type="application/json",)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_item(self):
        """Add OrderItem"""
        # Create a test_order
        test_order = self._create_orders(1)[0]
        # Create a test_item
        test_order_item = OrderItemFactory()
        logging.debug(test_order_item)
        resp = self.app.post(
            "{0}/{1}/items".format(BASE_URL, test_order.id),
            json=test_order_item.serialize(), 
            content_type=CONTENT_TYPE_JSON
        )
        new_order_item = resp.get_json()
        self.assertEqual(test_order.id, new_order_item['order_id'])
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_add_item_missing_data(self):
        """Add OrderItem with Missing Data"""
        # Create a test_order
        test_order = self._create_orders(1)[0]
        resp = self.app.post(
            "{0}/{1}/items".format(BASE_URL, test_order.id),
            json={}, 
            content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_item_no_content(self):
        """Add OrderItem No Content"""
        # Create a test_order
        test_order = self._create_orders(1)[0]
        resp = self.app.post("{0}/{1}/items".format(BASE_URL, test_order.id))
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_add_item_wrong_type(self):
        """Add OrderItem Wrong Type"""
        # Create a test_order
        test_order = self._create_orders(1)[0]

        # Create a test_item with wrong item_id type
        test_order_item = OrderItemFactory()
        logging.debug(test_order_item)
        test_order_item.item_id = "ID"
        resp = self.app.post(
            "{0}/{1}/items".format(BASE_URL, test_order.id),
            json=test_order_item.serialize(), 
            content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        # Create a test_item with wrong item_name type
        test_order_item = OrderItemFactory()
        logging.debug(test_order_item)
        test_order_item.item_name = 0
        resp = self.app.post(
            "{0}/{1}/items".format(BASE_URL, test_order.id),
            json=test_order_item.serialize(), 
            content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        # Create a test_item with wrong item_qty type
        test_order_item = OrderItemFactory()
        logging.debug(test_order_item)
        test_order_item.item_qty = "QTY"
        resp = self.app.post(
            "{0}/{1}/items".format(BASE_URL, test_order.id),
            json=test_order_item.serialize(), 
            content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        # Create a test_item with wrong item_price type
        test_order_item = OrderItemFactory()
        logging.debug(test_order_item)
        test_order_item.item_price = "PRICE"
        resp = self.app.post(
            "{0}/{1}/items".format(BASE_URL, test_order.id),
            json=test_order_item.serialize(), 
            content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_items_in_order(self):
        """List all items in an order"""
        # get the id of an order
        test_order = self._create_orders(1)[0]
        resp = self.app.get(
            "/orders/{}/items".format(test_order.id), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(test_order.order_items))

    def test_get_items_in_order_not_found(self):
        """List all items in an non-existing order"""
        resp = self.app.get("/orders/0/items")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_item_in_order(self):
        """ Delete an Item in an order"""
        # Create a test_order
        order = self._create_orders(1)[0]
        # Add a test_item
        test_order_item = OrderItemFactory()
        logging.debug(test_order_item)
        resp = self.app.post(
            "{0}/{1}/items".format(BASE_URL, order.id),
            json=test_order_item.serialize(), 
            content_type=CONTENT_TYPE_JSON
        )
        new_order_item = resp.get_json()
        item_id = new_order_item['id']
        # Delete the item
        resp = self.app.delete("/orders/{}/items/{}".format(order.id, item_id))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_item_order_not_found(self):
        """ Delete an Item where order does not exist"""
        resp = self.app.delete("/orders/{}/items/{}".format(0, 0))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_item_item_not_found(self):
        """ Delete an Item where item does not exist"""
        order = self._create_orders(1)[0]
        resp = self.app.delete("/orders/{}/items/{}".format(order.id, 0))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_read_item_in_order(self):
        """ Read an Item in an order"""
        # Create a test_order
        order = self._create_orders(1)[0]
        # Add a test_item
        test_order_item = OrderItemFactory()
        logging.debug(test_order_item)
        resp = self.app.post(
            "{0}/{1}/items".format(BASE_URL, order.id),
            json=test_order_item.serialize(),
            content_type=CONTENT_TYPE_JSON
        )
        new_order_item = resp.get_json()
        item_id = new_order_item['id']
        # Read the item
        resp = self.app.get("/orders/{}/items/{}".format(order.id, item_id))
        data = resp.get_json()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        print(test_order_item)
        self.assertEqual(data["item_id"], test_order_item.item_id)
        self.assertEqual(data["item_name"], test_order_item.item_name)
        self.assertEqual(data["item_price"], test_order_item.item_price)
        self.assertEqual(data["item_qty"], test_order_item.item_qty)

    def test_read_item_order_not_found(self):
        """ Read an Item where order does not exist"""
        resp = self.app.get("/orders/{}/items/{}".format(0, 0))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_read_item_item_not_found(self):
        """ Read an Item where item does not exist"""
        order = self._create_orders(1)[0]
        resp = self.app.get("/orders/{}/items/{}".format(order.id, 0))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)