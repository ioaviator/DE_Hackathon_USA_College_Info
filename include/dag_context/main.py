from ..ELT.extract import api_connect
from ..ELT.load import load_to_data_lake, load_to_db
from ..ELT.transform import transform_data


def connect_to_api(**context):
  json_data = api_connect()
 
  task_instance = context['ti']
  task_instance.xcom_push(key="json_file", value=json_data)

def load_data_to_data_lake(**context):
  task_instance = context['ti']
  json = task_instance.xcom_pull(task_ids='api_conect',key='json_file')
  
  data = load_to_data_lake(json)

def transform(**context):
  json_data = transform_data()
 
  task_instance = context['ti']
  task_instance.xcom_push(key="json_file", value=json_data)


def load_to_db(**context):
  task_instance = context['ti']
  json = task_instance.xcom_pull(task_ids='data_transform',key='json_file')
  
  data = load_to_db(json)
