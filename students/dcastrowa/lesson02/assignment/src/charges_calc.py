'''
Returns total price paid for individual rentals 
'''
import argparse
import json
import datetime
import math
import logging


def init_logging(logging_level):

    # format of logging outputs and log file name
    log_format = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'
    formatter = logging.Formatter(log_format)
    log_file = datetime.datetime.now().strftime('%Y-%m-%d') + '_charges_calc.log'

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
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='Enter debugging level: 0-no action 1-error, 2-warning, 3-debug',
                        default=0, required=False)

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
                logging.error(f'The end date {value["rental_end"]} shouldn\'t be before'
                              f' the start date {value["rental_start"]}.')
            elif rental_start == rental_end:
                logging.warning(f'Returned the same day {value["rental_start"]}.')
            else:
                value['total_days'] = (rental_end - rental_start).days
                value['total_price'] = value['total_days'] * value['price_per_day']
                value['sqrt_total_price'] = math.sqrt(value['total_price'])
                value['unit_cost'] = value['total_price'] / value['units_rented']
        except ValueError as value_error:
            if value['rental_end'] == "":
                logging.warning(
                    f"Item has no rental end date. Msg: {value_error}")
        except ZeroDivisionError as division_error:
            if value['units_rented'] == 0:
                logging.error(f"No units rented, can't calculate unit_cost. Msg: {division_error}")

    return data


def save_to_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    args = parse_cmd_arguments()
    logging = init_logging(args.debug)
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
