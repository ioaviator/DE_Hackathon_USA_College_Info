import pandas as pd
import polars as pl

from .auth import blob_service_client
from .database.db_setup import db_engine


def load_to_data_lake(data):
  all_records = []
  for resp in data:
    all_records.extend(resp.get("results", []))
  
  data_df = pd.DataFrame(all_records)
  
  # Define your Azure Blob Storage account details
  container_name = 'raw'
  blob_name = 'top_1000_usa_schools.parquet'

  # Convert your pandas dataframe to a parquet 
  parquet = data_df.to_parquet(index=False)

  # Upload the bytes object to Azure Blob Storage
  blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
  blob_client.upload_blob(parquet, overwrite=True)
  print('upload to storage account successful')

  return None


def load_to_db(data):
  
  data = pl.DataFrame(data)
  data.write_database(
      "top_1000_USA_schools", connection=db_engine, if_table_exists="replace"
    )
  print(f"Json files transformed and loaded to database")
