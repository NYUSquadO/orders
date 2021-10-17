"""
TestOrder API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch
from service import status  # HTTP Status Codes
from service.models import db, init_db
from service.routes import app
from .factories import OrderFactory

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

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """ Test index call """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_order(self):
        """Create a new order"""
        test_order = OrderFactory()
        logging.debug(test_order)
        resp = self.app.post(
            BASE_URL, json=test_order.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        # location = resp.headers.get("Location", None)
        # self.assertIsNotNone(location)
        # Check the data is correct
        new_order = resp.get_json()
        print(new_order)
        self.assertEqual(new_order["cust_id"], test_order.cust_id, "cust_id do not match")
        # Check that the location header was correct
        # resp = self.app.get(location, content_type=CONTENT_TYPE_JSON)
        # self.assertEqual(resp.status_code, status.HTTP_200_OK)