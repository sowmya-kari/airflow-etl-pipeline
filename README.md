
# Project: API-based ETL Pipeline using Airflow, Pandas, PostgreSQL & DuckDB

This project demonstrates an end-to-end ETL pipeline that:

* Extracts data from a public API
* Transforms it using Pandas
* Loads it into both PostgreSQL and DuckDB
* Orchestrates the flow using Apache Airflow

## Folder Structure

```
api_etl_pipeline/
├── dags/
│   └── api_etl_dag.py
├── extract/
│   └── fetch_api_data.py
├── transform/
│   └── transform_data.py
├── load/
│   ├── load_to_postgres.py
│   └── load_to_duckdb.py
├── data/
│   └── raw_data.json
├── requirements.txt
└── README.md
```

## Example API: COVID-19 Stats (can be replaced with any public API)

---

### `dags/api_etl_dag.py`

```python
from airflow import DAG
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
```

---

### `extract/fetch_api_data.py`

```python
import requests
import json

def fetch_data():
    url = 'https://api.covidtracking.com/v1/us/daily.json'
    response = requests.get(url)
    data = response.json()

    with open('data/raw_data.json', 'w') as f:
        json.dump(data, f)
```

---

### `transform/transform_data.py`

```python
import pandas as pd

def transform():
    df = pd.read_json('data/raw_data.json')
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
    df = df[['date', 'positive', 'death']]
    df.to_csv('data/cleaned_data.csv', index=False)
```

---

### `load/load_to_postgres.py`

```python
import pandas as pd
from sqlalchemy import create_engine

def load_postgres():
    df = pd.read_csv('data/cleaned_data.csv')
    engine = create_engine('postgresql+psycopg2://postgres:2508@localhost:5432/airflow')
    df.to_sql('covid_stats', engine, if_exists='replace', index=False)
```

---

### `load/load_to_duckdb.py`

```python
import pandas as pd
import duckdb

def load_duckdb():
    df = pd.read_csv('data/cleaned_data.csv')
    con = duckdb.connect(database='airflow_data.duckdb')
    con.execute("CREATE TABLE IF NOT EXISTS covid_stats AS SELECT * FROM df")
    con.close()
```

---

### `requirements.txt`

```
airflow
psycopg2-binary
sqlalchemy
pandas
requests
duckdb
```

---

### `README.md`

````markdown
# API ETL Pipeline

## Description
This project demonstrates how to:
- Fetch data from an API
- Clean and transform it using Pandas
- Load it into PostgreSQL and DuckDB
- Schedule and orchestrate the flow with Apache Airflow

## Prerequisites
- Python 3.11
- Airflow
- PostgreSQL running on localhost

## Running the Project
1. Install dependencies:
```bash
pip install -r requirements.txt
````

2. Run Airflow:

```bash
airflow db migrate
airflow webserver --port 8080
airflow scheduler
```

3. Enable the DAG in the UI.

---

Happy Data Engineering! 🚀

```
```
