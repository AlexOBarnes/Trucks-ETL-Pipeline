'''Module extracts batched data from trucks bucket'''
from os import environ as ENV
import logging
from io import BytesIO
from datetime import datetime, timedelta
from dotenv import load_dotenv
from boto3 import client
import pandas as pd

def format_file_date(filename:str) -> datetime:
    '''Formats the csv file names into the file creation dates'''
    file_date = "/".join(filename.split('/')[1:4])
    return datetime.strptime(file_date,'%Y-%m/%d/%H')

def find_truck_data(objects: list) -> list:
    '''Uses endwith to find all csv files from the last 3 hours in a bucket'''
    today = datetime.now()-timedelta(hours=3)
    truck_filenames = [o for o in objects if o.endswith('.csv')]
    return [file for file in truck_filenames if format_file_date(file) >= today]


def list_all_objects(bucket_name: str, storage_client) -> list:
    '''Returns all object names from a given bucket'''
    return find_truck_data([objects.get("Key") for objects in
                        storage_client.list_objects(Bucket=bucket_name)["Contents"]])

def download_truck_data(files: list, storage_client) -> pd.DataFrame:
    '''Downloads the specified files into a pandas dataframe'''
    truck_data= BytesIO()
    trucks_df = pd.DataFrame()

    for file in files:
        storage_client.download_fileobj(Bucket=ENV["BUCKET"],Key=file,Fileobj=truck_data)
        logging.info("%s downloaded successfully.", file.capitalize())
        truck_data.seek(0)
        truck = pd.read_csv(truck_data)
        truck['truck_id'] = int(file.split("_")[1][-1])
        trucks_df= pd.concat([trucks_df, truck], ignore_index=True)
        logging.info("%s merged successfully.", file.capitalize())

    return trucks_df


def extract_truck_data():
    '''Extracts files from the last 3 hours from the specified bucket'''
    aws_client = client(service_name="s3",
                        aws_access_key_id=ENV["AWS_ACCESS_KEY"],
                        aws_secret_access_key=ENV["AWS_SECRET_ACCESS_KEY"])
    file_names = list_all_objects(ENV["BUCKET"], aws_client)
    if file_names:
        logging.info("Files found")
    return download_truck_data(file_names,aws_client)


if __name__ == "__main__":
    load_dotenv()
    extract_truck_data()
