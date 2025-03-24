import os
import sys
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator

from include.ELT.transform import transform_data
from include.dag_context.main import (
  connect_to_api, load_data_to_data_lake, db_load)

sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "ETL"),
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "dag_context")
)



default_args = {
    'owner': 'aviator',
    'depends_on_past': False,
    'start_date': datetime(2025, 03, 24),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'schedule_interval': '@hourly',
}


with DAG(dag_id='top_1000_usa_schools', 
         catchup=False, default_args=default_args) as dag: 

  start = DummyOperator(task_id='pipeline_start')
  slow_down = DummyOperator(task_id='slow_down')

  end = DummyOperator(task_id='pipeline_ends')


api_connect = PythonOperator(
    task_id="api_connect",
    python_callable=connect_to_api,
    provide_context=True
  )

load_to_data_lake = PythonOperator(
    task_id="load_to_data_lake",
    python_callable=load_data_to_data_lake,
    provide_context=True
  )

data_transform = PythonOperator(
    task_id="data_transform",
    python_callable=transform_data,
    provide_context=True
  )

load_to_db = PythonOperator(
    task_id="load_to_db",
    python_callable=db_load,
    provide_context=True
  )

( 
    start
    >> api_connect 
    >> load_to_data_lake
    >> slow_down
    >> data_transform
    >> load_to_db
    >> end
  )
  