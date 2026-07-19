import sqlite3
import pandas as pd
import os
import tempfile

DB_PATH = os.path.join(tempfile.gettempdir(), "retail.db")

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

def create_database(df):
    df.to_sql("sales", conn, if_exists="replace", index=False)

def run_query(query, params=()):
    return pd.read_sql_query(query, conn,params=params)