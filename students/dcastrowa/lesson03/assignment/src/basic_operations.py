'''
basic_operations.py
Operation class to create, remove, update, and delete customer data
'''

from customer_model import *
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CUSTOMER_ID = 0
FIRST_NAME = 1
LAST_NAME = 2
HOME_ADDRESS = 3
PHONE_NUMBER = 4
EMAIL_ADDRESS = 5
STATUS = 6
CREDIT_LIMIT = 7


def add_customer(customer_id, first, last, addr, phone, email, status, limit):
    new_customer = Customer.create(
        customer_id=customer_id,
        first_name=last,
        last_name=first,
        home_address=addr,
        phone_number=phone,
        email_address=email,
        status=status,
        credit_limit=limit
    )
    new_customer.save()
    logger.info('Successfully added database')

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

    database.create_tables([Customer])
    logging.info(f'Creating table {Customer.__name__}')

    logging.info('Creating Customer records: iterate though the list of lists')
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
            logger.info(f'Error creating = ID:{customer[CUSTOMER_ID]}')
            logger.info(e)

    database.close()
