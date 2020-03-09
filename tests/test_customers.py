# Copyright 2016, 2019 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test cases for customer Model

Test cases can be run with:
    nosetests
    coverage report -m

While debugging just these tests it's convinient to use this:
    nosetests --stop tests/test_customers.py:TestcustomerModel

"""
import logging
import unittest
import os
from werkzeug.exceptions import NotFound
from service.models import customer, DataValidationError, db
from service import app
from .factories import customerFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)

######################################################################
#  P E T   M O D E L   T E S T   C A S E S
######################################################################
class TestcustomerModel(unittest.TestCase):
    """ Test Cases for customer Model """

    @classmethod
    def setUpClass(cls):
        """ These run once per Test suite """
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        customer.init_db(app)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_a_customer(self):
        """ Create a customer and assert that it exists """
        customer = customer(name="fido", category="dog", available=True)
        self.assertTrue(customer != None)
        self.assertEqual(customer.id, None)
        self.assertEqual(customer.name, "fido")
        self.assertEqual(customer.category, "dog")
        self.assertEqual(customer.available, True)
        customer = customer(name="fido", category="dog", available=False)
        self.assertEqual(customer.available, False)

    def test_add_a_customer(self):
        """ Create a customer and add it to the database """
        customers = customer.all()
        self.assertEqual(customers, [])
        customer = customer(name="fido", category="dog", available=True)
        self.assertTrue(customer != None)
        self.assertEqual(customer.id, None)
        customer.create()
        # Asert that it was assigned an id and shows up in the database
        self.assertEqual(customer.id, 1)
        customers = customer.all()
        self.assertEqual(len(customers), 1)

    def test_update_a_customer(self):
        """ Update a customer """
        customer = customerFactory()
        logging.debug(customer)
        customer.create()
        logging.debug(customer)
        self.assertEqual(customer.id, 1)
        # Change it an save it
        customer.category = "k9"
        original_id = customer.id
        customer.save()
        self.assertEqual(customer.id, original_id)
        self.assertEqual(customer.category, "k9")
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        customers = customer.all()
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0].id, 1)
        self.assertEqual(customers[0].category, "k9")

    def test_delete_a_customer(self):
        """ Delete a customer """
        customer = customerFactory()
        customer.create()
        self.assertEqual(len(customer.all()), 1)
        # delete the customer and make sure it isn't in the database
        customer.delete()
        self.assertEqual(len(customer.all()), 0)

    def test_serialize_a_customer(self):
        """ Test serialization of a customer """
        customer = customerFactory()
        data = customer.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], customer.id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], customer.name)
        self.assertIn("category", data)
        self.assertEqual(data["category"], customer.category)
        self.assertIn("available", data)
        self.assertEqual(data["available"], customer.available)

    def test_deserialize_a_customer(self):
        """ Test deserialization of a customer """
        data = {"id": 1, "name": "kitty", "category": "cat", "available": True}
        customer = customer()
        customer.deserialize(data)
        self.assertNotEqual(customer, None)
        self.assertEqual(customer.id, None)
        self.assertEqual(customer.name, "kitty")
        self.assertEqual(customer.category, "cat")
        self.assertEqual(customer.available, True)

    def test_deserialize_bad_data(self):
        """ Test deserialization of bad data """
        data = "this is not a dictionary"
        customer = customer()
        self.assertRaises(DataValidationError, customer.deserialize, data)

    def test_find_customer(self):
        """ Find a customer by ID """
        customers = customerFactory.create_batch(3)
        for customer in customers:
            customer.create()
        logging.debug(customers)
        # make sure they got saved
        self.assertEqual(len(customer.all()), 3)
        # find the 2nd customer in the list
        customer = customer.find(customers[1].id)
        self.assertIsNot(customer, None)
        self.assertEqual(customer.id, customers[1].id)
        self.assertEqual(customer.name, customers[1].name)
        self.assertEqual(customer.available, customers[1].available)

    def test_find_by_category(self):
        """ Find customers by Category """
        customer(name="fido", category="dog", available=True).create()
        customer(name="kitty", category="cat", available=False).create()
        customers = customer.find_by_category("cat")
        self.assertEqual(customers[0].category, "cat")
        self.assertEqual(customers[0].name, "kitty")
        self.assertEqual(customers[0].available, False)

    def test_find_by_name(self):
        """ Find a customer by Name """
        customer(name="fido", category="dog", available=True).create()
        customer(name="kitty", category="cat", available=False).create()
        customers = customer.find_by_name("kitty")
        self.assertEqual(customers[0].category, "cat")
        self.assertEqual(customers[0].name, "kitty")
        self.assertEqual(customers[0].available, False)

    def test_find_or_404_found(self):
        """ Find or return 404 found """
        customers = customerFactory.create_batch(3)
        for customer in customers:
            customer.create()

        customer = customer.find_or_404(customers[1].id)
        self.assertIsNot(customer, None)
        self.assertEqual(customer.id, customers[1].id)
        self.assertEqual(customer.name, customers[1].name)
        self.assertEqual(customer.available, customers[1].available)

    def test_find_or_404_not_found(self):
        """ Find or return 404 NOT found """
        self.assertRaises(NotFound, customer.find_or_404, 0)
