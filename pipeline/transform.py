'''Transforms data extracted from S3 bucket'''
from datetime import datetime,timedelta
import logging
import pandas as pd

def get_time() -> str:
    '''Returns string for the current time and three horus ago'''
    today = datetime.now()
    last_valid_time = today-timedelta(hours=3)
    return today.strftime('%Y-%m-%d %H:%M:%S'),last_valid_time.strftime('%Y-%m-%d %H:%M:%S')

def check_date(date:str) -> bool:
    '''Returns true if the date is in the correct format else false'''
    try:
        pd.to_datetime(date,format='%Y-%m-%d %H:%M:%S%z')
        return True
    except ValueError:
        return False

def remove_invalid_rows(truck_data: pd.DataFrame) -> pd.DataFrame:
    '''Removes rows that are invalid, data that is extreme and formats rows'''
    truck_data = truck_data.dropna(subset=["total","timestamp"])
    truck_data = truck_data[~truck_data['total'].isin(['NULL', 'ERR', 'blank', 'None','VOID',''])]

    logging.info("Invalid rows removed.")
    return truck_data

def format_data(truck_data:pd.DataFrame) -> pd.DataFrame:
    '''Sets the types of each row to valid datatypes 
    and formats the data ready for database entry'''
    truck_data['total'] = truck_data['total'].astype(float)
    truck_data = truck_data.loc[truck_data['timestamp'].apply(check_date)]
    truck_data.loc[:,'timestamp'] = pd.to_datetime(truck_data['timestamp'])
    truck_data.loc[:,'type'] = truck_data['type'].replace({'card': "2", 'cash': "1"}).astype(int)

    logging.info("Data types formatted successfully.")
    return truck_data

def remove_extreme_values(truck_data:pd.DataFrame) -> pd.DataFrame:
    '''Removes mismatched data and extreme data from the trucks dataframe'''
    current_time,last_valid_time = get_time()
    current_time = pd.to_datetime(current_time).tz_localize('UTC')
    last_valid_time = pd.to_datetime(last_valid_time).tz_localize('UTC')

    truck_data = truck_data.loc[(truck_data['total'] > 0) & (truck_data['total'] <= 100)]
    truck_data = truck_data.loc[(truck_data['timestamp'] >= last_valid_time) &
                                (truck_data['timestamp'] <= current_time)]

    logging.info("Extreme values removed from dataframe.")
    return truck_data

def transform(data: pd.DataFrame) -> list:
    '''Returns formatted truck data'''
    data = remove_invalid_rows(data)
    data = format_data(data)
    data = remove_extreme_values(data)
    return data.values.tolist()

if __name__ == "__main__":
    transform(pd.DataFrame())
