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
from werkzeug.exceptions import NotFound



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


    def _create_customer(self):
        """ Get a list of Customers """
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

        new_customer = resp.get_json()
        return new_customer


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




    def test_query_customer_list_by_user_name(self):
        """ Query Customers by Category """
        self._create_customer()
        self._create_customer()
        resp = self.app.get("/customers", query_string="user_name=ajmical")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 2)
        # check the data just to be sure
        for customer in data:
            self.assertEqual(customer["user_name"],"ajmical")



    def test_get_customer_list(self):
        """ Get a list of Customers """
        self._create_customer()
        self._create_customer()
        resp = self.app.get("/customers")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 2)



    def test_delete_customer(self):
        """ Delete a Customer """
        test_customer = self._create_customer()
        logging.debug(test_customer)
        resp = self.app.delete(
            "/customers/{}".format(test_customer["id"]), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # TODO: Uncomment this code after Ted adds retrieve
        # make sure they are deleted
        # resp = self.app.get(
        #     "/customers/{}".format(test_customer["id"]), content_type="application/json"
        # )
        # self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)



    def test_update_customer(self):
        """ Update an existing Customer """
        # create a customer to update
        new_customer = self._create_customer()

        # update the customer
        logging.debug(new_customer)
        new_customer["password"] = "unknown"
        resp = self.app.put(
            "/customers/{}".format(new_customer["id"]),
            json=new_customer,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_customer = resp.get_json()
        self.assertEqual(updated_customer["id"], new_customer["id"])
        self.assertEqual(updated_customer["password"], "unknown")


    def test_lock_customer(self):
        """ Lock an existing Customer """
        # create a customer to lock
        new_customer = self._create_customer()

        # lock the customer
        logging.debug(new_customer)
        resp = self.app.put(
            "/customers/{}/lock".format(new_customer["id"]),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        locked_customer = resp.get_json()
        self.assertEqual(locked_customer["id"], new_customer["id"])
        self.assertEqual(locked_customer["locked"], True)

    def test_get_customer(self):
        """ Get a single Customer """
        # get the id of a customer
        test_customer = self._create_customer()
        resp = self.app.get(
            "/customers/{}".format(test_customer["id"]), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["user_name"], test_customer["user_name"])

    def test_get_customer_not_found(self):
        """ Get a Customer thats not found """
        resp = self.app.get("/customers/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)



