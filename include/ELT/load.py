from typing import Any, Dict, List

import pandas as pd
import polars as pl

from .auth import blob_service_client
from .config import logger
from .database.db_setup import db_engine


def load_to_data_lake(data: List[Dict[str, Any]])->None:
  """
  Loads data to the data lake from a list of dictionaries.
    
  Args:
    data (List[Dict[str, Any]]): A list of json where each json
                                     represents an API response containing
                                     a "results" key.
  """
  
  all_records:List = []
  
  for resp in data:
    all_records.extend(resp.get("results", []))
  
  data_df: pd.DataFrame = pd.DataFrame(all_records)
  
  # Define your Azure Blob Storage account details
  container_name:str = 'raw'
  blob_name:str = 'top_1000_usa_schools.parquet'

  # Convert your pandas dataframe to a parquet 
  parquet = data_df.to_parquet(index=False)

  # Upload the bytes object to Azure Blob Storage
  blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
  blob_client.upload_blob(parquet, overwrite=True)
  
  logger.info('Upload to storage account successful')
  
  return None


def load_to_db(data:pl.DataFrame)->None:
  """
  Loads data into the database.

  Args:
    data (pl.DataFrame): A polars dataframe representing 
    the data records.
  """

  data:pl.DataFrame = pl.DataFrame(data)
  data.write_database(
      "top_1000_USA_schools", connection=db_engine, if_table_exists="replace"
    )
  
  logger.info("JSON files transformed and loaded to database")
  
  return None
