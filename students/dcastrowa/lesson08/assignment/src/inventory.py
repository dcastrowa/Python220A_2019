"""
inventory.py
author: @dcastrowa
"""

import csv
import os
from functools import partial


def add_furniture(invoice_file, customer_name, item_code,
                  item_description, item_monthly_price):
    """
    adds info for furniture invoice to a csv
    :param invoice_file: csv file name
    :param customer_name: first and last name
    :param item_code: id
    :param item_description: short description
    :param item_monthly_price: monthly price of item
    """
    info = [customer_name, item_code, item_description, item_monthly_price]

    if os.path.isfile(invoice_file):
        with open(invoice_file, 'a+') as file:
            writer = csv.writer(file)
            writer.writerow(info)
    else:
        with open(invoice_file, 'w+') as file:
            writer = csv.writer(file)
            writer.writerow(info)


# Input parameters: customer_name, invoice_file.
# Output: Returns a function that takes one parameter, rental_items.
def single_customer(customer_name, invoice_file):
    a = partial(add_furniture, customer_name=customer_name,
                invoice_file=invoice_file)

    def create_invoice(rental_items):
        with open(rental_items, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                a(item_code=row[0],
                  item_description=row[1],
                  item_monthly_price=row[2])

        return a

    return create_invoice


def main():
    """
    main function
    """
    add_furniture('invoice.csv', 'Elisa Miles',
                  'LR04', 'Leather Sofa', '25.00')
    add_furniture('invoice.csv', 'Edward Data',
                  'KT78', 'Kitchen Table', '10.00')
    add_furniture('invoice.csv', 'Alex Gonzales',
                  'BR02', 'Queen Mattress', '17.00')
    create_invoice = single_customer('Kev Cav',
                                     '/Users/danielcastro/Documents/PythonCert/Python220/Python220A_2019/students/dcastrowa/lesson08/assignment/src/invoice.csv')
    create_invoice('/Users/danielcastro/Documents/PythonCert/Python220/Python220A_2019/students/dcastrowa/lesson08/assignment/data/test_items.csv')


if __name__ == '__main__':
    main()
