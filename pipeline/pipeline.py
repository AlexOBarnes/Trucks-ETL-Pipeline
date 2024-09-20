'''Extracts, transforms and loads data from the S3 bucket'''
import argparse
import logging
from datetime import datetime as dt
from dotenv import load_dotenv
from extract import extract_truck_data
from transform import transform
from load import load_transaction_data

def get_date() -> str:
    '''Returns the current date'''
    return dt.now().strftime('%d-%m-%Y_%H:%M:%S')

def config_log() -> None:
    '''Configures the log'''
    date = get_date()
    logging.basicConfig(filename=f'pipeline_{date}_log.txt',
                        encoding='UTF-8', level=logging.WARNING)

def parse_arguments() -> None:
    '''Parses CL arguments'''
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", "-l", action='store_true')
    args = parser.parse_args()

    log = args.log
    if log:
        config_log()
    else:
        logging.basicConfig(level=logging.INFO)

def pipeline() -> None:
    '''Runs ETL pipeline extracting, cleaning and loading the truck data'''
    data = extract_truck_data()
    if not data.empty:
        logging.info('Data extracted successfully.')
        data = transform(data)
        logging.info('Data cleaned successfully.')
        load_transaction_data(data)
        logging.info('Data loaded successfully.')
    else:
        logging.info('No data found.')


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    parse_arguments()
    load_dotenv()
    pipeline()
