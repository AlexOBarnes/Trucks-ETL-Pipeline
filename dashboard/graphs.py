'''Creates a streamlit dashboard using pandas and altair'''
# pylint: disable=W0125,W0612,C0103,E0401

from os import environ as ENV
from redshift_connector import connect
from dotenv import load_dotenv
import pandas as pd
import altair as alt

COLOURS = ["skyblue", "blue", "pink", "red", "#77DD77", " #FFA500"]

def get_truck_names():
    '''Returns a list of truck names'''
    load_dotenv()
    query = """SELECT truck_name FROM DIM_truck"""
    with connect(host=ENV["DB_HOST"], database=ENV["DB_NAME"],
             user=ENV["DB_USER"], password=ENV["DB_PASSWORD"]) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            truck_names = cur.fetchall()
            conn.commit()
    return [list(name)[0] for name in truck_names]

def get_truck_data():
    '''Gets truck data from redshift database'''
    query = f"""SELECT t.truck_name,pm.payment_method_name,ft.total,ft.made_at
    FROM {ENV["DB_SCHEMA"]}.FACT_transaction AS ft
    JOIN DIM_truck AS t USING (truck_id)
    JOIN DIM_payment_method AS pm USING (payment_method_id)"""
    with connect(host=ENV["DB_HOST"], database=ENV["DB_NAME"],
                 user=ENV["DB_USER"], password=ENV["DB_PASSWORD"]) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            truck_data = cur.fetchall()
            conn.commit()
    return pd.DataFrame(truck_data,columns=["truck_id","type","total","timestamp"])


def revenue_over_time(trucks: pd.DataFrame) -> alt.Chart:
    '''Returns a line chart for the total income per truck each day'''
    income_by_truck = trucks.groupby(['truck_id', 'timestamp'])['total'].sum().reset_index()
    truck_selection = alt.selection_point(fields=['truck_id'], bind='legend')
    revenue_by_time = alt.Chart(income_by_truck).mark_line().encode(
        x='timestamp:T',
        y='total:Q',
        color=alt.Color('truck_id:N', title='Truck',scale=alt.Scale(range=COLOURS)),
        opacity=alt.condition(truck_selection, alt.value(1), alt.value(0.2))
    ).properties(
        title='Total Income Over Time by Truck'
    ).add_params(
        truck_selection
    ).interactive()
    return revenue_by_time


def transactions_over_time(trucks: pd.DataFrame) -> alt.Chart:
    '''Returns a line chart for the number of transactions over time'''
    transactions = trucks.groupby(['timestamp','truck_id']).size().reset_index()
    transactions["Frequency"] = transactions[0]
    transactions.columns = transactions.columns.astype(str)
    truck_selection = alt.selection_point(fields=['truck_id'], bind='legend')
    transactions_by_time = alt.Chart(transactions).mark_line().encode(
        x='timestamp:T',
        y='Frequency:Q',
        color=alt.Color('truck_id:N', title='Truck',scale=alt.Scale(range=COLOURS)),
        opacity=alt.condition(truck_selection, alt.value(1), alt.value(0.2))
    ).properties(
        title='Total Transactions Over Time by Truck'
    ).add_params(
        truck_selection
    ).interactive()
    return transactions_by_time

def value_per_payment_type(trucks: pd.DataFrame) -> alt.Chart:
    '''Returns a bar chart of average value per transaction by payment method'''
    average_per_type = trucks.groupby('type')['total'].mean().apply(
        lambda x: round(x, 2)).reset_index()
    value_by_payment_type = alt.Chart(average_per_type).mark_bar().encode(
        x=alt.X('type:O', title='Payment Method'),
        y=alt.Y('total', title='Average Value of Transaction (GBP)'),
        color=alt.Color('type:O', title='Type', scale=alt.Scale(
            range=[COLOURS[0], COLOURS[1]])),
    ).properties(
        title='Average Value per Transaction by Payment Method'
    )
    return value_by_payment_type

def proportion(trucks: pd.DataFrame) -> alt.Chart:
    '''Returns a pie chart for the different payment types'''
    type_proportion = trucks["type"].value_counts(
    ).reset_index().replace({2: 'card', 1: 'cash'})
    proportion_of_payment_types = alt.Chart(type_proportion).mark_arc().encode(
        theta=alt.Theta(field='count', type='quantitative'),
        color=alt.Color('type:N', title='Transaction Type',
                        scale=alt.Scale(range=[COLOURS[0],COLOURS[1]])),
    ).properties(
        title='Proportion of Transactions by Type'
    )
    return proportion_of_payment_types

def revenue_by_truck(trucks: pd.DataFrame) -> alt.Chart:
    '''Returns a bar chart with revenue plotted for each truck'''
    revenue_per_truck = trucks.groupby('truck_id')['total'].sum().reset_index()
    total_revenue_per_truck = alt.Chart(revenue_per_truck).mark_bar().encode(
        x=alt.X('truck_id:O', title='Truck', sort=alt.EncodingSortField(
            field='total', op='sum', order='ascending')),
        y=alt.Y('total', title='Total Income (GBP)'),
        color=alt.Color('truck_id:N', title='Truck',
                        scale=alt.Scale(range=COLOURS)),
    ).properties(
        title='Total Income by Truck'
    )
    return total_revenue_per_truck

def fsa_by_revenue(trucks:pd.DataFrame) -> alt.Chart:
    '''Returns a scatter plot with rating plotted against total value'''
    food_safety = pd.DataFrame({'truck_id':['Burrito Madness','Kings of Kebabs',
                                            'Cupcakes by Michelle',"Hartmann's Jellied Eels",
                                            'Yoghurt Heaven','SuperSmoothie'],
                                'fsa_rating':[4,2,5,4,4,3]})
    revenue_per_truck = trucks.groupby('truck_id')['total'].sum().reset_index()
    revenue_by_fsa= pd.merge(revenue_per_truck,food_safety, on='truck_id')
    fsa_rating_by_revenue = alt.Chart(revenue_by_fsa).mark_point().encode(
        x=alt.X('fsa_rating:Q', title='FSA Rating',scale=alt.Scale(domain=[2,5])),
        y=alt.Y('total:Q', title='Total Income (GBP)'),
        color=alt.Color('truck_id:N', title='Truck',
                        scale=alt.Scale(range=COLOURS)),
    ).properties(
        title='Total Income by FSA Rating'
    )
    return fsa_rating_by_revenue

def transactions_by_truck(trucks:pd.DataFrame) -> alt.Chart:
    '''Returns a bar chart of the total number of transactions by truck'''
    most_transactions = trucks.groupby('truck_id').size().reset_index()
    most_transactions["total"] = most_transactions[0]
    most_transactions.columns = most_transactions.columns.astype(str)
    transactions_per_truck = alt.Chart(most_transactions).mark_bar().encode(
        x=alt.X('truck_id:O', title='Truck', sort=alt.EncodingSortField(
            field='total', op='sum', order='ascending')),
        y=alt.Y('total', title='Number of transactions'),
        color=alt.Color('truck_id:N', title='Truck',
                        scale=alt.Scale(range=COLOURS)),
    ).properties(
        title='Total Transactions by Truck'
    )
    return transactions_per_truck

def make_graphs() -> alt.Chart:
    '''Returns the all the graphs made in this file'''
    load_dotenv()
    data = get_truck_data()
    data['timestamp'] = pd.to_datetime(data['timestamp']).dt.date
    return transactions_over_time(data),revenue_over_time(data)

def make_revenue_graphs(truck_filter: list=None) -> alt.Chart:
    '''Returns graphs relating to truck revenue and filters data if argument is given'''
    load_dotenv()
    data = get_truck_data()
    data['timestamp'] = pd.to_datetime(data['timestamp']).dt.date
    if filter:
        data = data[data["truck_id"].isin(truck_filter)]
    return transactions_by_truck(data),revenue_by_truck(data),fsa_by_revenue(data)

def make_payment_graphs(type_filter: list= None) -> alt.Chart:
    '''Returns graphs relating to payments and filters data if argument is given'''
    load_dotenv()
    data = get_truck_data()
    if filter:
        data = data[data["type"].isin(type_filter)]
    return proportion(data),value_per_payment_type(data)

if __name__ == "__main__":
    load_dotenv()
    trucks_data = get_truck_data()
    trucks_data['timestamp'] = pd.to_datetime(trucks_data['timestamp']).dt.date
