
from include.ELT.extract import api_connect
from include.ELT.load import load_to_data_lake, load_to_db
from include.ELT.transform import transform_data


def main():
  response = api_connect()
  load = load_to_data_lake(response)
  transform = transform_data()
  db_load = load_to_db(transform)
  
  return None
      

if __name__ == "__main__":
    main()