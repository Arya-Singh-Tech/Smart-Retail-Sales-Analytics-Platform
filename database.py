import sqlite3
import pandas as pd

# Database connection
conn = sqlite3.connect("retail.db", check_same_thread=False)
cursor = conn.cursor()

def create_database(df):
    df.to_sql("sales", conn, if_exists="replace", index=False)

def run_query(query, params=()):
    return pd.read_sql_query(query, conn,params=params)