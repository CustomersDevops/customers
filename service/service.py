"""
My Service

This is the service which creates, indexes, lists, updates, deletes, and locks a customer
"""

import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status  # HTTP Status Codes

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import Customer, DataValidationError

# Import Flask application
from . import app

# Import Not Found
from werkzeug.exceptions import NotFound


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return app.send_static_file('index.html')


######################################################################
# LIST ALL CUSTOMERS
######################################################################
@app.route("/customers", methods=["GET"])
def list_customers():
    """ Returns all of the Customers """
    app.logger.info("Request for customer list")
    customers = []
    user_name = request.args.get("user_name")
    name = request.args.get("name")
    if user_name:
        customers = Customer.find_by_user_name(user_name)
    elif name:
        customers = Customer.find_by_name(name)
    else:
        customers = Customer.all()

    results = [customer.serialize() for customer in customers]
    return make_response(jsonify(results), status.HTTP_200_OK)


######################################################################
# CREATE NEW CUSTOMER INFO
######################################################################
@app.route("/customers", methods=["POST"])
def create_customer():
    """
    Creates a new Customer
    This endpoint will create a Customer based the data in the body that is posted
    """
    app.logger.info("Request to create a Customer")
    check_content_type("application/json")
    customer = Customer()
    customer.deserialize(request.get_json())
    customer.create()
    message = customer.serialize()
    #location_url = url_for("get_customers", customer_id=customer.id, _external=True)
    location_url = "not implemented"
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )



######################################################################
# DELETE A CUSTOMER
######################################################################
@app.route("/customers/<int:customer_id>", methods=["DELETE"])
def delete_customers(customer_id):
    """
    Delete a Customer
    This endpoint will delete a Customer based the id specified in the path
    """
    app.logger.info("Request to delete customer with id: %s", customer_id)
    customer = Customer.find(customer_id)
    if customer:
        customer.delete()
    return make_response("", status.HTTP_204_NO_CONTENT)


    
######################################################################
# UPDATE A CUSTOMER
######################################################################
@app.route("/customers/<int:customer_id>", methods=["PUT"])
def update_customers(customer_id):
    """
    Update a Customer
    This endpoint will update a Customer based the body that is posted
    """
    app.logger.info("Request to update customer with id: %s", customer_id)
    check_content_type("application/json")
    customer = Customer.find(customer_id)
    if not customer:
        raise NotFound("Customer with id '{}' was not found.".format(customer_id))
    customer.deserialize(request.get_json())
    customer.id = customer_id
    customer.save()
    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)

######################################################################
# ACTION - LOCK A CUSTOMER
######################################################################
@app.route("/customers/<int:customer_id>/lock", methods=["PUT"])
def lock_customers(customer_id):
    """
    Lock A Customer
    This endpoint will lock a Customer based the body that is posted
    """
    app.logger.info("Request to lock customer with id: %s", customer_id)
    check_content_type("application/json")
    customer = Customer.find(customer_id)
    if not customer:
        raise NotFound("Customer with id '{}' was not found.".format(customer_id))
    customer.locked = True
    customer.save()
    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)

######################################################################
# ACTION - UNLOCK A CUSTOMER
######################################################################
@app.route("/customers/<int:customer_id>/unlock", methods=["PUT"])
def unlock_customers(customer_id):
    """
    Unlock A Customer
    This endpoint will unlock a Customer based the body that is posted
    """
    app.logger.info("Request to unlock a customer with id: %s", customer_id)
    check_content_type("application/json")
    customer = Customer.find(customer_id)
    if not customer:
        raise NotFound("Customer with id '{}' was not found.".format(customer_id))
    customer.locked = False
    customer.save()
    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)

######################################################################
# READ CUSTOMER
######################################################################
@app.route("/customers/<int:customer_id>", methods=["GET"])
def get_customers(customer_id):
    """
    Retrieve a single customer
    This endpoint will return a Customer based on it's id
    """
    app.logger.info("Request for customer with id: %s", customer_id)
    customer = Customer.find(customer_id)
    if not customer:
        raise NotFound("Customer with id '{}' was not found.".format(customer_id))

    app.logger.info("Returning customer: %s", customer.name)
    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)


######################################################################
# DELETE ALL CUSTOMER DATA (for testing only)
######################################################################
@app.route('/customers/reset', methods=['DELETE'])
def customers_reset():
    """ Removes all pets from the database """
    Customer.remove_all()
    return make_response('', status.HTTP_204_NO_CONTENT)


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    Customer.init_db(app)

def check_content_type(content_type):
    """ Checks that the media type is correct """
    if request.headers["Content-Type"] == content_type:
        return
    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(415, "Content-Type must be {}".format(content_type))

