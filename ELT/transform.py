from io import BytesIO

import polars as pl

from database.db_setup import db_engine

from .auth import blob_client

# from .config import data_dir


def get_data_from_datalake():

  stream_downloader = blob_client.download_blob()
  stream = BytesIO()
  stream_downloader.readinto(stream)
  parquet_data = pl.read_parquet(stream, use_pyarrow=True)
  
  return parquet_data


def transform_data():

    response_df = get_data_from_datalake()

    # Rename columns to lowercase
    response_df = response_df.rename(
        {col: col.lower() for col in response_df.columns}
    )
   
    # rename dataframe columns
    school_df = response_df.rename({
        'latest.school.state':'state',
        'latest.school.degrees_awarded.predominant': 'predominant_degrees',
        'latest.school.degrees_awarded.highest':'highest_degree',
        'latest.admissions.admission_rate.overall': 'admission_rate',
        'latest.student.size': 'student_size',
        'latest.cost.tuition.in_state': 'tuition_in_statte',
        'latest.cost.tuition.out_of_state': 'tuition_out_of_state',
        'latest.aid.loan_principal':'loan_aid',
        'latest.school.ownership':'ownership',
        'latest.school.online_only': 'online_only', 
        'school.name': 'school_name'
    })
    
    # Verify changes
    # print(school_df.columns)

    # Drop duplicate values
    school_df = school_df.unique()


    # Load dataframe to parquet file
    # school_df.write_csv(f"{data_dir}/processed_data.csv")
    # print(f"Json files transformed and loaded as parquet to {data_dir} folder")

    school_df.write_database(
        "top_1000_USA_schools", connection=db_engine, if_table_exists="replace"
    )
    print(f"Json files transformed and loaded to database")

    return True
