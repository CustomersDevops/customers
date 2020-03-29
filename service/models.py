"""
Models for Customers

All of the models are stored in this module
"""
import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass


class Customer(db.Model):
    """
    Class that represents a Customers
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24))
    user_name = db.Column(db.String(24))
    password = db.Column(db.String(63))

    def __repr__(self):
        return "Customer %r id=[%s]>" % (self.name, self.id)

    def create(self):
        """
        Creates a Customers to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def save(self):
        """
        Updates a Customers to the database
        """
        logger.info("Saving %s", self.name)
        db.session.commit()

    def delete(self):
        """ Removes a Customers from the data store """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Customers into a dictionary """
        return {
            "id": self.id,
            "name": self.name,
            "user_name": self.user_name,
            "password": self.password,
            #"available": self.available

        }

    def deserialize(self, data):
        """
        Deserializes a Customers from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            self.user_name = data["user_name"]
            self.password = data["password"]
        except KeyError as error:
            raise DataValidationError("Invalid Customers: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid Customers: body of request contained" "bad or no data"
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
        """ Returns all of the Customers in the database """
        logger.info("Processing all Customers")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a Customers by its ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_or_404(cls, by_id):
        """ Find a Customers by it's id """
        logger.info("Processing lookup or 404 for id %s ...", by_id)
        return cls.query.get_or_404(by_id)

    @classmethod
    def find_by_name(cls, name):
        """ Returns all Customers with the given name

        Args:
            name (string): the name of the Customers you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_user_name(cls, user_name):
        """ Returns all Customers with the given user name

        Args:
            user_name (string): the name of the Customers you want to match
        """
        logger.info("Processing user name query for %s ...", user_name)
        return cls.query.filter(cls.user_name == user_name)
