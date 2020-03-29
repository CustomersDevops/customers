"""
Test cases for customers Model

"""
import logging
import unittest
import os
from service import app
from service.models import Customer, DataValidationError, db
 
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)

######################################################################
#  customers   M O D E L   T E S T   C A S E S
######################################################################
class TestCustomer(unittest.TestCase):
    """ Test Cases for <your resource name> Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Customer.init_db(app)


    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()

######################################################################
#  P L A C E   T E S T   C A S E S   H E R E 
######################################################################

    def test_create_a_customer(self):
        """ Create a customer and confirm that it exists """
        customer = Customer( 
            name="Alex Mical", 
            user_name="ajmical", 
            password="password",
            
            
        )
        self.assertTrue(customer != None)
        self.assertEqual(customer.id, None)
        self.assertEqual(customer.name, "Alex Mical")
        self.assertEqual(customer.user_name, "ajmical")
        self.assertEqual(customer.password, "password")
        
  




    def test_add_a_customer(self):
        """ Create a customer and add it to the database """ 
        customers = Customer.all()
        self.assertEqual(customers, [])
        customer = Customer(
            name="Alex Mical", 
            user_name="ajmical", 
            password="password",
            
        )
        self.assertTrue(customer != None)
        self.assertEqual(customer.id, None)
        customer.create()
        # Asert that it was assigned an id and shows up in the database
        self.assertEqual(customer.id, 1)
        customers = Customer.all()
        self.assertEqual(len(customers), 1)
