'''
Returns total price paid for individual rentals 
'''
import argparse
import json
import datetime
import math
import logging

# format of logging outputs
log_format = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'
formatter = logging.Formatter(log_format)
log_file = datetime.datetime.now().strftime('%Y-%m-%d') + '_charges_calc.log'
#
# set up file
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
#
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)
# console_handler.setFormatter(formatter)
#
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# logger.addHandler(console_handler)
logger.addHandler(file_handler)


def parse_cmd_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)

    return parser.parse_args()


def load_rentals_file(filename):
    with open(filename) as file:
        try:
            data = json.load(file)
        except ValueError:
            exit(0)
    return data


def calculate_additional_fields(data):
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            if rental_end < rental_start:
                logging.error(f'The end date {value["rental_end"]} shouldn\'t be before the start date.')
            elif rental_start == rental_end:
                logging.warning(f'Returned the same day {value["rental_start"]}.')
            else:
                value['total_days'] = (rental_end - rental_start).days
                value['total_price'] = value['total_days'] * value['price_per_day']
                value['sqrt_total_price'] = math.sqrt(value['total_price'])
                value['unit_cost'] = value['total_price'] / value['units_rented']
        except ValueError as value_error:
            if value['rental_end'] == "":
                logger.warning(
                    "Item has no rental end date. Msg: %s", value_error)
        except ZeroDivisionError as division_error:
            if value['units_rented'] == 0:
                logger.error("No units rented, can't calculate unit_cost. Msg: %s",
                             division_error)

    return data


def save_to_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    args = parse_cmd_arguments()
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
