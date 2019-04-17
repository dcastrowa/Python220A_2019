'''
Returns total price paid for individual rentals
'''
import argparse
import json
from datetime import datetime
import math
import logging


def init_logging(logging_level):
    '''
    inint logging for debug command options
    :param logging_level:
    :return: logger
    '''

    # format of logging outputs and log file name
    log_format = '%(asctime)s %(filename)s:%(lineno)-3d' \
                 ' %(levelname)s %(message)s'
    formatter = logging.Formatter(log_format)
    log_file = datetime.now().strftime('%Y-%m-%d') + '_charges_calc.log'

    # set up file
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # set up whats prints to console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # set up loggers to file and console
    logger = logging.getLogger()

    if logging_level == 0:
        logger.disabled = True
    elif logging_level == 1:
        file_handler.setLevel(logging.ERROR)
        logger.addHandler(file_handler)
        console_handler.setLevel(logging.ERROR)
        logger.addHandler(console_handler)
    elif logging_level == 2:
        file_handler.setLevel(logging.WARNING)
        logger.addHandler(file_handler)
        console_handler.setLevel(logging.WARNING)
        logger.addHandler(console_handler)
    elif logging_level == 3:
        console_handler.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)
        file_handler.setLevel(logging.WARNING)
        logger.addHandler(file_handler)

    return logger


def parse_cmd_arguments():
    '''
    argument parser for commands
    :return: parse_args
    '''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input',
                        help='input JSON file',
                        required=True)
    parser.add_argument('-o', '--output',
                        help='output JSON file',
                        required=True)
    parser.add_argument('-d', '--debug',
                        choices=[0, 1, 2, 3],
                        help='Debugging level: 1-error, 2-warning, 3-debug',
                        default=0,
                        required=False)

    return parser.parse_args()


def load_rentals_file(filename):
    '''
    creates json data
    :param filename:
    :return: data (dictionary)
    '''
    with open(filename) as file:
        try:
            json_data = json.load(file)
        except ValueError:
            exit(0)
    return json_data


def calculate_additional_fields(json_data):
    '''
    add total days, total price, and square root total price to data
    :param json_data:
    :return: json_data (dictionary)
    '''
    for value in json_data.values():
        try:
            rental_start = datetime.strptime(value['rental_start'], f'%m/%d/%y')
            rental_end = datetime.strptime(value['rental_end'], '%m/%d/%y')
            if rental_end < rental_start:
                LOGGER.error(f'The end date {value["rental_end"]}'
                             f' shouldn\'t be before'
                             f' the start date {value["rental_start"]}.')
            elif rental_start == rental_end:
                LOGGER.warning(f'Returned the same day')
            else:
                value['total_days'] = (rental_end - rental_start).days
                value['total_price'] = \
                    value['total_days'] * value['price_per_day']
                value['sqrt_total_price'] = math.sqrt(value['total_price'])
                value['unit_cost'] = \
                    value['total_price'] / value['units_rented']
        except ValueError as value_error:
            if value['rental_end'] == "":
                LOGGER.warning(
                    f"Item has no rental end date. Msg: {value_error}")
        except ZeroDivisionError as division_error:
            if value['units_rented'] == 0:
                LOGGER.error(f"No units rented, can't calculate unit_cost. "
                             f"Msg: {division_error}")

    return json_data


def save_to_json(filename, json_data):
    '''
    saves a new json file of added data
    :param filename:
    :param json_data:
    :return:
    '''
    with open(filename, 'w') as file:
        json.dump(json_data, file)


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    LOGGER = init_logging(ARGS.debug)
    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)
