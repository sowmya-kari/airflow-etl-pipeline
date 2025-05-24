import pandas as pd
from sqlalchemy import create_engine

def load_postgres():
    df = pd.read_csv('data/cleaned_data.csv')
    engine = create_engine('postgresql+psycopg2://postgres:2508@localhost:5432/airflow')
    df.to_sql('covid_stats', engine, if_exists='replace', index=False)
