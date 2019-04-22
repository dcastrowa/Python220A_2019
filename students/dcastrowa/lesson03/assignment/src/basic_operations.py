'''
basic_operations.py
Operation class to create, remove, update, and delete customer data
'''

from customer_model import *
import logging

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
    # create() function to add customer data to the database
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
    logger.info(f'Successfully added customer')

    # iterate through customer data to log
    for customer in Customer:
        logger.info(f'id: {customer.customer_id}')
        logger.info(f'first: {customer.first_name}')
        logger.info(f'last: {customer.last_name}')
        logger.info(f'address: {customer.home_address}')
        logger.info(f'phone: {customer.phone_number}')
        logger.info(f'email: {customer.email_address}')
        logger.info(f'status: {customer.status}')
        logger.info(f'limit: {customer.credit_limit}')

    return Customer


def search_customer(customer_id):
    """
    search for customer by customer id
    :return: (dictionary) customer data
    """
    with database.transaction():
        query = (Customer
                 .select(Customer)
                 .where(Customer.customer_id == customer_id)
                 )
        logger.info('SELECT * FROM Customer WHERE customer_id = '
                    f'{customer_id}')

    logger.info('iterate through query to create dictionary')
    results = {}
    for item in query:
        results['first_name'] = item.first_name
        results['last_name'] = item.last_name
        results['email'] = item.email_address
        results['phone_number'] = item.phone_number

    return results


def delete_customer(customer_id):
    """
    delete customer by customer id
    :return:
    """
    with database.transaction():
        customer = Customer.get(Customer.customer_id == customer_id)

        logger.info(f'Trying to delete {customer.first_name}')
        customer.delete_instance()
        logger.info(f'Deleted {customer.first_name}')


def update_customer(customer_id, credit_limit):
    """
    update customer credit limit by customer id
    :return:
    """
    with database.transaction():
        customer_update = Customer.get(Customer.customer_id == customer_id)
        logger.info(f'Current limit: {customer_update.credit_limit}')
        customer_update.credit_limit = credit_limit
        logger.info(f'New credit limit: {customer_update.credit_limit}')

    return customer_update


def list_active_customers():
    with database.transaction():
        query = (Customer
                 .select(fn.COUNT(Customer.status).alias('count'))
                 .where(Customer.status))

    for item in query:
        logger.info(f'Number of active customers {item.count}')
        return item.count


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

    # create a table
    database.create_tables([Customer])
    logger.info(f'Creating table {Customer.__name__}')

    # iterate through list of customer data to add to Customer
    logger.info('Creating Customer records: iterate though the list of lists')
    for customer in customers:
        try:
            with database.transaction():
                add_customer(customer[CUSTOMER_ID],
                             customer[FIRST_NAME],
                             customer[LAST_NAME],
                             customer[HOME_ADDRESS],
                             customer[PHONE_NUMBER],
                             customer[EMAIL_ADDRESS],
                             customer[STATUS],
                             customer[CREDIT_LIMIT])
        except Exception as e:
            logger.warning(f'Error creating = ID: {customer[CUSTOMER_ID]}')
            logger.warning(e)

    # search for customer data
    customer_info = search_customer(3)
    if not bool(customer_info):
        logger.warning(f'Customer not found')
    else:
        logger.info(customer_info)

    delete_customer(2)
    update_customer(1, 500)
    list_active_customers()

    # close database connection
    database.close()


