"""
create_data.py
generate random data for assignment
author: dcastrowa
"""

import csv
import uuid
from faker import Faker

faker = Faker()


def generate_data(csv_file):
    """
    creates more data in the csv file
    """
    with open(csv_file, 'w') as file:
        writer = csv.DictWriter(file,
                                delimiter=',',
                                lineterminator='\n',
                                fieldnames=[
                                    'seq',
                                    'guid',
                                    'seq',
                                    'seq',
                                    'ccnumber',
                                    'date',
                                    'sentence'
                                ])

        writer.writeheader()
        for new_lines in range(1000000):
            writer.writerow(dict(
                seq=new_lines + 1,
                guid=uuid.uuid4(),
                ccnumber=faker.credit_card_number(),
                date=faker.date(pattern='%m/%d/%Y'),
                sentence=faker.sentence()
            ))


if __name__ == '__main__':
    generate_data('/Users/danielcastro/Documents/PythonCert/Python220'
                  '/Python220A_2019/students/dcastrowa/lesson06/assignment'
                  '/data/exercise.csv')



