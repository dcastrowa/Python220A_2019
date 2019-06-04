"""
parallel.py
@author dastrowa
"""

import csv
import datetime as dt
import threading
import queue
from pymongo import MongoClient
from multiprocessing import Pool


class MongoDBConnection:
    """
    MongoDB Connection to server
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


def csv_to_list_of_dict(directory_name):
    """
    turns a csv file into a dictionary
    :return: list of dictionaries
    """
    with open(directory_name, encoding='utf-8-sig') as product:
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


def mongo_processor(db_name, db_content, out_queue):
    """
    processor for importing the data
    :param db_name: name of target database
    :param db_content: data from database
    :param out_queue: queue for output
    :return: tuple: relative count, final count, and final time
    """
    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.HP_Norton_DB

        target_db = database[db_name]
        count = target_db.count_documents({})
        out_queue.put(count)

        total_process = (len(db_content))
        out_queue.put(total_process)

        target_db.insert_many(db_content)

        final_count = target_db.count_documents({})
        out_queue.put(final_count)

        end_time = dt.datetime.now()
        out_queue.put(end_time)

    return count, final_count, end_time


def main():
    """
    main function to integrate all functions
    """
    start = dt.datetime.now()
    dir_name = '/Users/danielcastro/Documents/PythonCert/Python220' \
               '/Python220A_2019/students/dcastrowa/lesson07/assignment/data/'
    product_file = 'product.csv'
    customer_file = 'customers.csv'

    product_file_dir = dir_name + product_file
    customer_file_dir = dir_name + customer_file

    directory_list = [product_file_dir, customer_file_dir]

    with Pool(processes=2) as p:
        return_lists = p.map(csv_to_list_of_dict, directory_list)

    product_dicts = return_lists[0]
    customer_dicts = return_lists[1]

    prod_queue = queue.Queue()
    cust_queue = queue.Queue()

    prod_thread = threading.Thread(target=mongo_processor,
                                   args=('products',
                                         product_dicts,
                                         prod_queue))
    cust_thread = threading.Thread(target=mongo_processor,
                                   args=('customers',
                                         customer_dicts,
                                         cust_queue))

    prod_thread.start()
    cust_thread.start()

    prod_thread.join()
    cust_thread.join()

    prod_return = []
    cust_return = []

    while not prod_queue.empty():
        prod_return.append(prod_queue.get())

    while not cust_queue.empty():
        cust_return.append(cust_queue.get())

    end = dt.datetime.now()
    prod_tuple = (prod_return[0],
                  prod_return[1],
                  prod_return[2],
                  (prod_return[3] - start).total_seconds())
    print(prod_tuple)

    cust_tuple = (cust_return[0],
                  cust_return[1],
                  cust_return[2],
                  (cust_return[3] - start).total_seconds())
    print(cust_tuple)
    print((end-start).total_seconds())


if __name__ == '__main__':
    main()
