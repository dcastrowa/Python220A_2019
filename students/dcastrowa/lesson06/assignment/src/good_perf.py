"""
good_perf.py
better performing, poorly written module
author: dcastrowa
"""

import datetime
import csv
from collections import defaultdict


def get_data(csv_filename):
    """
    row reader into a generator
    """
    with open(csv_filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            yield row


def analyze(file_name):
    """
    analyze the data created
    """
    start = datetime.datetime.now()
    gen_a = get_data(file_name)

    # turned the for loop creating a list into a generator
    new_ones = ((list(row)[5], list(row)[0]) for row in gen_a
                if list(row)[5] > '00/00/2012')

    # used default dict to create a dictionary
    year_count = defaultdict(int)
    for new in new_ones:
        if new[0][6:] == '2013':
            year_count["2013"] += 1
        elif new[0][6:] == '2014':
            year_count["2014"] += 1
        elif new[0][6:] == '2015':
            year_count["2015"] += 1
        elif new[0][6:] == '2016':
            year_count["2016"] += 1
        elif new[0][6:] == '2017':
            year_count["2017"] += 1
        elif new[0][6:] == '2018':
            year_count["2018"] += 1

    print(year_count)

    found = 0
    gen_b = get_data(file_name)

    # created a second generator for this second loop
    for line in gen_b:
        if "ao" in line[6]:
            found += 1

    print(f"'ea' was found {found} times")
    end = datetime.datetime.now()

    return start, end, year_count, found


def main():
    """
    main function to run all functions
    """
    filename = "/Users/danielcastro/Documents/PythonCert/Python220" \
               "/Python220A_2019/students/dcastrowa/lesson06/assignment" \
               "/data/exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    main()
