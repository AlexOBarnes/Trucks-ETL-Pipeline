'''Module loads a list of data into a given redshift database'''
from os import environ as ENV
from redshift_connector import connect
from dotenv import load_dotenv

def load_transaction_data(data: list[list]) -> None:
    """Uploads transaction data to the database."""
    query = f"""INSERT INTO {ENV["DB_SCHEMA"]}.FACT_transaction
            (made_at,payment_method_id,total,truck_id)"""
    query += """VALUES (%s,%s,%s,%s)"""
    with connect(host=ENV["DB_HOST"], database=ENV["DB_NAME"],
                 user=ENV["DB_USER"], password=ENV["DB_PASSWORD"]) as conn:
        with conn.cursor() as cur:
            cur.executemany(query, data)
            conn.commit()

if __name__ == "__main__":
    load_dotenv()
    load_transaction_data([[]])
