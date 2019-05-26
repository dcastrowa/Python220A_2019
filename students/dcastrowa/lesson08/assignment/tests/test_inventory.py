"""
    Autograde Lesson 8 assignment

"""

import pytest
import csv
import os
from src import inventory


def test_add_furniture():
    inventory.add_furniture('invoice.csv', 'Elisa Miles', 'LR04',
                            'Leather Sofa', '25.00')
    inventory.add_furniture('invoice.csv', 'Edward Data', 'KT78',
                            'Kitchen Table', '10.00')
    inventory.add_furniture('invoice.csv', 'Alex Gonzales', 'BR02',
                            'Queen Mattress', '17.00')

    with open('invoice.csv', 'r') as file:
        reader = csv.reader(file)
        test_invoice = [line for line in reader]

    invoice = [['Elisa Miles', 'LR04', 'Leather Sofa', '25.00'],
               ['Edward Data', 'KT78', 'Kitchen Table', '10.00'],
               ['Alex Gonzales', 'BR02', 'Queen Mattress', '17.00']]

    assert test_invoice == invoice

    os.remove('invoice.csv')

# def single_customer(customer_name, invoice_file):
