from unittest import TestCase
from src.basic_operations import *
from src.customer_model import *
from peewee import *

test_db = SqliteDatabase(':memory:')


class BasicOperationsTests(TestCase):

    # set up temporary databases for testing
    def setUp(self):
        test_db.bind([Customer], bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.execute_sql('PRAGMA foreign_keys = ON;')
        test_db.create_tables([Customer])

    def turnDown(self):
        test_db.drop_tables([Customer])
        database.close()

    # test add customer
    def test_add_customer(self):

        add_customer(1, 'Lady', 'Gaga', '453 Hollywood Blvd',
                     555334290, 'badromance@gaga.com', True, 20000)

        test_customer = [1, 'Lady', 'Gaga', '453 Hollywood Blvd',
                         555334290, 'badromance@gaga.com', True, 20000]

        self.assertEqual(test_customer[0], Customer.customer_id)
        self.assertEqual(test_customer[1], Customer.first_name)
        self.assertEqual(test_customer[2], Customer.last_name)
        self.assertEqual(test_customer[3], Customer.home_address)
        self.assertEqual(test_customer[4], Customer.phone_number)
        self.assertEqual(test_customer[5], Customer.email_address)
        self.assertEqual(test_customer[6], Customer.status)
        self.assertEqual(test_customer[7], Customer.credit_limit)

    def test_search_customer(self):

        customer_dict = search_customer(1)

        test_customer = {
            'first_name': 'Lady',
            'last_name': 'Gaga',
            'email': 'badromance@gaga.com',
            'phone_number': 555334290
        }

        self.assertDictEqual(test_customer, customer_dict)


if __name__ == '__main__':
    unittest.main()
