
from ELT.extract import api_connect
from ELT.load import load_to_data_lake
from ELT.transform import transform_data


def main():
  response = api_connect()
  load = load_to_data_lake(response)
  transform = transform_data()
  
  return None
      

if __name__ == "__main__":
    main()