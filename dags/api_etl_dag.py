rom airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from extract.fetch_api_data import fetch_data
from transform.transform_data import transform
from load.load_to_postgres import load_postgres
from load.load_to_duckdb import load_duckdb

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
}

dag = DAG(
    dag_id='api_etl_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
)

t1 = PythonOperator(
    task_id='fetch_api_data',
    python_callable=fetch_data,
    dag=dag
)

t2 = PythonOperator(
    task_id='transform_data',
    python_callable=transform,
    dag=dag
)

t3 = PythonOperator(
    task_id='load_to_postgres',
    python_callable=load_postgres,
    dag=dag
)

t4 = PythonOperator(
    task_id='load_to_duckdb',
    python_callable=load_duckdb,
    dag=dag
)

t1 >> t2 >> [t3, t4]
