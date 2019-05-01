"""
customer_model.py
Customer model for creating customer data
"""
import logging
from peewee import Model
from peewee import SqliteDatabase
from peewee import CharField

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

database = SqliteDatabase('../data/lesson04.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')
LOGGER.info('Connect to database')


# Build BaseModel
class BaseModel(Model):
    """
    Base model from peewee
    """
    class Meta:
        """
        set up database
        """
        database = database


# Customer class to hold all customer data
class Customer(BaseModel):
    """
    This class is the Customer class that stores all data about
    our customers.
    """
    customer_id = CharField(primary_key=True)
    first_name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    home_address = CharField(max_length=80)
    phone_number = CharField()
    email_address = CharField(max_length=80)
    status = CharField()
    credit_limit = CharField()
