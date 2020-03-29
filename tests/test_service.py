"""
<your resource name> API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch
from flask_api import status  # HTTP Status Codes
from service.models import db
from service.service import app, init_db


# DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)

######################################################################
#  T E S T   C A S E S
######################################################################
class TestYourResourceServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ Run once before all tests """
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db()

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        """ Runs before each test """
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

    def test_create_customer(self):
        """ Create a new Customer """
        test_customer = {
            "name": "Alex Mical",
            "user_name": "ajmical",
            "password": "password",
        }
    
        resp = self.app.post(
            "/customers", 
            json=test_customer, 
            content_type="application/json"
        )

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)
        # Check the data is correct
        new_customer = resp.get_json()
        self.assertEqual(new_customer["name"], test_customer["name"], "Names do not match")
        self.assertEqual(new_customer["user_name"], test_customer["user_name"], "User Names do not match")
        self.assertEqual(new_customer["password"], test_customer["password"], "Passwords do not match")
  
        # Check that the location header was correct
        #WHEN create is implemented, uncomment
        #resp = self.app.get(location, content_type="application/json")
        #self.assertEqual(resp.status_code, status.HTTP_200_OK)
        #new_customer = resp.get_json()
        #self.assertEqual(new_customer["name"], test_customer["name"], "Names do not match")
        #self.assertEqual(new_customer["user_name"], test_customer["user_name"], "User Names do not match")
        #self.assertEqual(new_customer["password"], test_customer["password"], "Passwords do not match")