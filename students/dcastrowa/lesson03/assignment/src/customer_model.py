import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Here we define our data (the schema)')
logger.info('First name and connect to a database (sqlite here)')

logger.info('The next 3 lines of code are the only database specific code')

database = SqliteDatabase('lesson03.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')
logger.info('Connect to database')


# Build BaseModel
class BaseModel(Model):
    """
    Base model from peewee
    """
    class Meta:
        database = database


# Customer class to hold all customer data
class Customer(BaseModel):
    """
    This class is the Customer class that stores all data about
    our customers.
    """
    customer_id = IntegerField(primary_key=True)
    first_name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    home_address = CharField(max_length=80)
    phone_number = IntegerField()
    email_address = CharField(max_length=80)
    status = BooleanField()
    credit_limit = IntegerField()
