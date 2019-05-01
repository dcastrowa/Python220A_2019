"""
basic_operations.py
Operation class to create, remove, update, and delete customer data
"""
import logging
import csv
from datetime import datetime
from peewee import fn
from peewee import DoesNotExist
from peewee import IntegrityError
from customer_model import database
from customer_model import Customer


# format of logging outputs and log file name
LOG_FORMAT = '%(asctime)s %(filename)s:%(lineno)-3d' \
             ' %(levelname)s %(message)s'
FORMATTER = logging.Formatter(LOG_FORMAT)
LOG_FILE = datetime.now().strftime('%Y-%m-%d') + '_db.log'

# set up loggers to file and console
LOGGER = logging.getLogger()

# set up file
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setFormatter(FORMATTER)
FILE_HANDLER.setLevel(logging.INFO)
LOGGER.addHandler(FILE_HANDLER)

# set up whats prints to console
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(FORMATTER)
CONSOLE_HANDLER.setLevel(logging.ERROR)
LOGGER.addHandler(CONSOLE_HANDLER)

# customer attributes
CUSTOMER_ID = 0
FIRST_NAME = 1
LAST_NAME = 2
HOME_ADDRESS = 3
PHONE_NUMBER = 4
EMAIL_ADDRESS = 5
STATUS = 6
CREDIT_LIMIT = 7


def add_customer(customer_id, first, last, addr, phone, email, status, limit):
    """
    adds a new customer to Customer table
    :return: Customer table
    """
    try:
        LOGGER.info('Creating customer record')
        with database.transaction():
            new_customer = Customer.create(
                customer_id=customer_id,
                first_name=first,
                last_name=last,
                home_address=addr,
                phone_number=phone,
                email_address=email,
                status=status,
                credit_limit=limit
            )
            new_customer.save()
            LOGGER.info('Added customer: %s', new_customer.customer_id)
    except IntegrityError as err:
        LOGGER.warning('Error creating = ID: %s', customer_id)
        LOGGER.warning(err)

    return Customer


def search_customer(customer_id):
    """
    search for customer by customer id
    :return: (dict) customer data
    """
    try:
        customer = Customer.get(Customer.customer_id == customer_id)
        LOGGER.info('Getting info for customer %s', customer.customer_id)

        results = {
            'first_name': customer.first_name,
            'last_name': customer.last_name,
            'email': customer.email_address,
            'phone_number': customer.phone_number
        }

        LOGGER.info(results)

    except DoesNotExist as err:
        LOGGER.warning('Customer ID: %s does not exist', customer_id)
        LOGGER.warning(err)

        results = {}

    return results


def delete_customer(customer_id):
    """
    delete customer by customer id
    :return:
    """
    try:
        customer = Customer.get(Customer.customer_id == customer_id)

        LOGGER.info('Trying to delete %s', customer.first_name)
        customer.delete_instance()
        LOGGER.info('Deleted %s', customer.first_name)

        return True

    except DoesNotExist as err:
        LOGGER.warning('Customer ID: %s does not exist', customer_id)
        LOGGER.warning(err)

        return False


def update_customer(customer_id, credit_limit):
    """
    update customer credit limit by customer id
    :return:
    """
    try:
        with database.transaction():
            customer_update = Customer.get(Customer.customer_id == customer_id)
            LOGGER.info('Current limit: %s', customer_update.credit_limit)
            customer_update.credit_limit = credit_limit
            LOGGER.info('New credit limit: %s', customer_update.credit_limit)

            return True

    except DoesNotExist as err:

        LOGGER.warning('Customer ID: %s does not exist', customer_id)
        LOGGER.warning(err)

        return False


def list_active_customers():
    """
    gets total number of active customers
    :return: (int) # of active customers
    """
    with database.transaction():
        query = (Customer
                 .select(fn.COUNT(Customer.status).alias('count'))
                 .where(Customer.status == 'Active'))
        LOGGER.info(query)

    customer_count = [item.count for item in query]
    LOGGER.info('Number of active customers: %s', customer_count[0])

    return customer_count[0]


def get_data_from_csv(csv_file):
    """
    creates a list of data from a csv file
    :return: (list) full list of customer data
    """
    # create customer list form csv file
    with open(csv_file, encoding='utf-8', errors='ignore') as people:
        customer_reader = csv.reader(people)
        customers = [row for row in customer_reader]

    return customers


if __name__ == '__main__':

    CUSTOMER_DATA = get_data_from_csv('../data/customer.csv')
    # create a table
    database.create_tables([Customer])
    LOGGER.info('Creating table %s', Customer.__name__)

    # add customers from data to Customer table
    for person in CUSTOMER_DATA[1:]:
        add_customer(person[CUSTOMER_ID],
                     person[FIRST_NAME],
                     person[LAST_NAME],
                     person[HOME_ADDRESS],
                     person[PHONE_NUMBER],
                     person[EMAIL_ADDRESS],
                     person[STATUS],
                     person[CREDIT_LIMIT])
    #
    # search for customer id C002345
    search_customer('C0023450')
    #
    # # delete customer id C000002
    delete_customer('C0023450')
    #
    # # update credit limit to 500000 for customer id C003312
    update_customer('C003312', '500000')
    #
    # # number of active users
    list_active_customers()

    database.close()
