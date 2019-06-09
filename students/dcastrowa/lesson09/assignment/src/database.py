"""
datbase.py
@author dastrowa
"""

import csv
import os
from pymongo import MongoClient
from pymongo import errors


class MongoDBConnection:
    """
    Context class for MongoDB connections
    """

    def __init__(self, host='127.0.0.1', port=27017):
        """
        initialize host, port, and connection
        """
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        """
        connects to DB when entering
        """
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        closes connection upon exiting
        """
        self.connection.close()


MONGO = MongoDBConnection()


def drop_collections(*collection_names):
    """
    drops a list of collections from database
    """
    with MONGO:
        database = MONGO.connection.HP_Norton_DB

        # delete collections
        for collection in collection_names:
            database.drop_collection(collection)

    return True


def csv_to_list_of_dict(directory_name, csv_file):
    """
    turns a csv file into a dictionary
    :return: list of dictionaries
    """
    # cur_path = os.path.dirname(os.path.abspath(__file__))
    # print(cur_path)
    # csv_path = os.path.relpath(f'../{directory_name}/{csv_file}', cur_path)
    # print(csv_path)
    csv_path = os.path.dirname(os.getcwd()) + '/' + directory_name + '/' + \
               csv_file
    with open(csv_path, encoding='utf-8-sig') as product:
        reader = csv.reader(product)
        item_list = [row for row in reader]
        header = item_list[0]
        all_items = []
        header_index = 0
        for rows in item_list[1:]:
            item_dict = {}
            for item in rows:
                item_dict[header[header_index]] = item
                header_index += 1
            all_items.append(item_dict)
            header_index = 0

    return all_items


def import_data(directory_name, product_file, customer_file, rental_file):
    """
    takes three csv files and imports the data into
    :return: 2 tuples with count of number of customers per input
    """
    products_list = csv_to_list_of_dict(directory_name, product_file)
    customers_list = csv_to_list_of_dict(directory_name, customer_file)
    rentals_list = csv_to_list_of_dict(directory_name, rental_file)

    with MONGO:
        # connect to database or create new one if it already exists
        database = MONGO.connection.HP_Norton_DB

        # insert data into the products collections
        product_errors = 0
        try:
            products = database['products']
            products.insert_many(products_list)
        except errors.CollectionInvalid:
            product_errors += 1

        # insert data into the customer collection
        customer_errors = 0
        try:
            customers = database['customers']
            customers.insert_many(customers_list)
        except errors.CollectionInvalid:
            customer_errors += 1

        # insert data into the rental collection
        rental_errors = 0
        try:
            rentals = database['rentals']
            rentals.insert_many(rentals_list)
        except errors.CollectionInvalid:
            rental_errors += 1

        # return tuple of record count per collection
        collection_count = (
            products.count_documents({}),
            customers.count_documents({}),
            rentals.count_documents({})
        )

        # count number of errors per collection
        errors_count = (
            product_errors,
            customer_errors,
            rental_errors
        )

    return collection_count, errors_count


def show_available_products():
    """
    shows all available products
    return: dictionary
    """
    with MONGO:
        database = MONGO.connection.HP_Norton_DB
        products = database['products']

        available_products = {}
        for doc in products.find({'quantity_available': {'$ne': '0'}}):
            available_products[doc['product_id']] = {
                'description': doc['description'],
                'product_type': doc['product_type'],
                'quantity_available': doc['quantity_available']
            }

    return available_products


def show_rentals(product_id):
    """
    shows all the customers info based on product id
    """
    with MONGO:
        database = MONGO.connection.HP_Norton_DB
        rentals = database['rentals']
        customers = database['customers']

        rentals_available = {}
        for prod in rentals.find({'product_id': product_id}):
            for customer in customers.find({'user_id': prod['user_id']}):
                rentals_available[prod['user_id']] = {
                    'name': customer['name'],
                    'address': customer['address'],
                    'phone_number': customer['phone_number'],
                    'email': customer['email']
                }

    return rentals_available


def main():
    """
    main function to integrate all functions
    """
    import_data('data', 'product.csv', 'customers.csv', 'rental.csv')
    print(show_available_products())
    print('')
    print(show_rentals('prd002'))

    drop_collections('products', 'customers', 'rentals')
    print(show_available_products())


if __name__ == '__main__':
    main()
