"""
basic_operations.py
Operation class to create, remove, update, and delete customer data
"""

from customer_model import *
import logging
# import csv

# set logger at info level
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        logger.info('Creating Customer record')
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
            logger.info(f'Successfully added customer: {new_customer}')
            logger.info(f'id: {new_customer.customer_id}')
            logger.info(f'first: {new_customer.first_name}')
            logger.info(f'last: {new_customer.last_name}')
            logger.info(f'address: {new_customer.home_address}')
            logger.info(f'phone: {new_customer.phone_number}')
            logger.info(f'email: {new_customer.email_address}')
            logger.info(f'status: {new_customer.status}')
            logger.info(f'limit: {new_customer.credit_limit}')
    except Exception as e:
        logger.warning(f'Error creating = ID: {customer_id}')
        logger.warning(e)

    return Customer


def search_customer(customer_id):
    """
    search for customer by customer id
    :return: (dict) customer data
    """
    with database.transaction():
        query = (Customer
                 .select(Customer)
                 .where(Customer.customer_id == customer_id)
                 )
        logger.info(query)

    logger.info('iterate through query to create dictionary')
    results = {}
    for item in query:
        results['first_name'] = item.first_name
        results['last_name'] = item.last_name
        results['email'] = item.email_address
        results['phone_number'] = item.phone_number

    if not bool(results):
        logger.warning('Customer not found')

    return results


def delete_customer(customer_id):
    """
    delete customer by customer id
    :return:
    """
    try:
        with database.transaction():
            customer = Customer.get(Customer.customer_id == customer_id)

            logger.info(f'Trying to delete {customer.first_name}')
            customer.delete_instance()
            logger.info(f'Deleted {customer.first_name}')

            return True

    except Exception as e:
        logger.warning(f'Customer ID: {customer_id} does not exist')
        logger.warning(e)

        return False


def update_customer(customer_id, credit_limit):
    """
    update customer credit limit by customer id
    :return:
    """
    try:
        with DATABASE.transaction():
            customer_update = Customer.get(Customer.customer_id == customer_id)
            logger.info(f'Current limit: {customer_update.credit_limit}')
            customer_update.credit_limit = credit_limit
            logger.info(f'New credit limit: {customer_update.credit_limit}')

            return True

    except Exception as e:
        logger.warning(f'Customer ID: {customer_id} does not exist')
        logger.warning(e)

        return False


def list_active_customers():
    """
    gets total number of active customers
    :return: (int) # of active customers
    """
    with database.transaction():
        query = (Customer
                 .select(fn.COUNT(Customer.status).alias('count'))
                 .where(Customer.status))
        logger.info(query)

    active_customers = []
    for item in query:
        logger.info(f'Number of active customers {item.count}')
        active_customers.append(item.count)

    return active_customers[0]


if __name__ == '__main__':
    customers = [
        [
            1, 'Jerry', 'Springer', '243 Daytime Street',
            55523476543, 'springer@show.com', False, 1000
        ],
        [
            2, 'Drew', 'Carey', '9986 Television Avenue',
            5556234577, 'dcarey@show.com', False, 200000
        ],
        [
            3, 'Oprah', 'Winfrey', '777 Everybody Boulevard',
            5559082313, 'winfrey@own.com', True, 900000
        ],
    ]

# create customer list form csv file
# customers = []
# with open('/Users/danielcastro/Documents/PythonCert/Python220/'
#           'Python220A_2019/students/template_student/lesson03/assignment/'
#           'data/customer.csv', encoding='utf-8', errors='ignore') as people:
#     customer_reader = csv.reader(people)
#     for row in customer_reader:
#         customers.append(row)

    # create a table
    database.create_tables([Customer])
    logger.info(f'Creating table {Customer.__name__}')

    # add customers from data to Customer table
    for customer in customers:
        add_customer(customer[CUSTOMER_ID],
                     customer[FIRST_NAME],
                     customer[LAST_NAME],
                     customer[HOME_ADDRESS],
                     customer[PHONE_NUMBER],
                     customer[EMAIL_ADDRESS],
                     customer[STATUS],
                     customer[CREDIT_LIMIT])

    # search for customer id 3
    search_customer(3)

    # delete customer id 2
    delete_customer(2)

    # update credit limit to 500 for customer id 1
    update_customer(1, 500)

    # number of active users
    list_active_customers()

    # close database connection
    database.close()



