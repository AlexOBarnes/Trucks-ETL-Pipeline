'''Queries redshift database and extracts key information for a daily report'''
from os import environ as ENV
import json
from datetime import datetime as dt
from jinja2 import Template
from redshift_connector import connect
from dotenv import load_dotenv

def total_income() -> list:
    '''Gets the total transactions and income for the day'''
    query = """SELECT COUNT(*) as total_transactions, SUM(total) as total_income
    FROM FACT_transaction
    WHERE made_at >= CURRENT_DATE AND made_at < CURRENT_DATE + INTERVAL '1 day'"""
    with connect(host=ENV["DB_HOST"], database=ENV["DB_NAME"],
                 user=ENV["DB_USER"], password=ENV["DB_PASSWORD"]) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            data = cur.fetchone()
            conn.commit()
    return {'transactions':data[0],'total':data[1], 'date':get_date()}

def income_by_truck() -> list:
    '''Gets the number, value and average value of transactions by truck '''
    query = """SELECT dt.truck_name as Truck, COUNT(*) as total_transactions,
    SUM(ft.total) as total_income, AVG(ft.total) as average_transaction_value
    FROM FACT_transaction as ft
    JOIN DIM_truck as dt
    USING (truck_id)
    WHERE made_at >= CURRENT_DATE AND made_at < CURRENT_DATE + INTERVAL '1 day'
    GROUP BY dt.truck_name"""
    with connect(host=ENV["DB_HOST"], database=ENV["DB_NAME"],
                 user=ENV["DB_USER"], password=ENV["DB_PASSWORD"]) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            data = cur.fetchall()
            conn.commit()
    return data

def transactions_by_payment() -> list:
    '''Gets the number of transactions and value by payment.'''
    query = """SELECT dpm.payment_method_name as payment_method,
    COUNT(*) as total_transactions, SUM(ft.total) as total_income,
    AVG(ft.total) as average_transaction_value
    FROM FACT_transaction as ft
    JOIN DIM_payment_method as dpm
    USING (payment_method_id)
    WHERE made_at >= CURRENT_DATE AND made_at < CURRENT_DATE + INTERVAL '1 day'
    GROUP BY dpm.payment_method_name"""
    with connect(host=ENV["DB_HOST"], database=ENV["DB_NAME"],
                 user=ENV["DB_USER"], password=ENV["DB_PASSWORD"]) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            data = cur.fetchall()
            conn.commit()
    return data

def value_by_hour() -> list:
    '''Gets the average and total value and transactions by hour '''
    query = """SELECT DATE_TRUNC('hour', made_at) AS transaction_hour,
    COUNT(*) AS total_transactions, SUM(total) AS total_income
    FROM FACT_transaction
    WHERE made_at >= CURRENT_DATE AND made_at < CURRENT_DATE + INTERVAL '1 day'
    GROUP BY transaction_hour
    ORDER BY transaction_hour"""
    with connect(host=ENV["DB_HOST"], database=ENV["DB_NAME"],
                 user=ENV["DB_USER"], password=ENV["DB_PASSWORD"]) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            data = cur.fetchall()
            conn.commit()
    return data

def get_date() -> str:
    '''Returns the current formatted date string'''
    return dt.now().strftime('%Y_%m_%d')

def create_json() -> list[dict]:
    '''Creates the json that will be loaded into the .json file'''
    daily_overview = total_income()

    transaction_by_truck = [{'name':truck[0],'transactions':truck[1],'income':truck[2]}
                            for truck in income_by_truck()]

    transaction_data_by_payment = [{'name': method[0].capitalize(), 'transactions': method[1],
                                    'income': method[2]} for method in transactions_by_payment()]

    hourly_data = [{'time': hour[0].strftime('%H:%M'), 'transactions': hour[1], 'income': hour[2]}
                   for hour in value_by_hour()]

    return {'overview':daily_overview,
            'grouped_data':{'truck':transaction_by_truck,
            'payment_method':transaction_data_by_payment,
            'time':hourly_data}}

def format_html(data:dict) -> str:
    '''Uses jinja2 to format the json into an html file'''
    with open('template.html','r', encoding='UTF-8') as f:
        template = Template(f.read())
    html = template.render(overview=data['overview'], grouped_data=data['grouped_data'])
    return html

def load_html(data:list[dict]) -> None:
    '''Loads the json to a local html file'''
    with open(f'report_data_{get_date()}.html','w',encoding='UTF-8') as f:
        f.write(format_html(data))

def load_json(data:list[dict]) -> None:
    '''Loads the json to a local json file'''
    with open(f'report_data_{get_date()}.json', 'w',encoding='UTF-8') as f:
        json.dump(data, f, indent= 4)

def create_report() -> None:
    '''Calls the functions to create the json and load the data to file'''
    json_data = create_json()
    load_json(json_data)
    load_html(json_data)

if __name__ == '__main__':
    load_dotenv()
    create_report()
