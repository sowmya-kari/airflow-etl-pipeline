import pandas as pd
import duckdb

def load_duckdb():
    df = pd.read_csv('data/cleaned_data.csv')
    con = duckdb.connect(database='airflow_data.duckdb')
    con.execute("CREATE TABLE IF NOT EXISTS covid_stats AS SELECT * FROM df")
    con.close()
