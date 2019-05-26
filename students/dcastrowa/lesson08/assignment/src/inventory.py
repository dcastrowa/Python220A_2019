"""
inventory.py
author: @dcastrowa
"""

import csv
import os


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


if __name__ == '__main__':
    main()
