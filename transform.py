import glob
import json
import os

import polars as pl

from config import data_dir
from database.db_setup import db_engine

# Get all JSON files in the data folder
json_files = glob.glob(os.path.join(data_dir, "*.json"))


def load_json_with_polars(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Extract the 'result' list and convert it into a Polars DataFrame
    return pl.DataFrame(data.get("results", []))


def transform_data():
    # Use list comprehension to load each file into a DataFrame
    school_list_df = [load_json_with_polars(file) for file in json_files]

    # Concatenate all JSON DataFrames into one
    combined_json = pl.concat(school_list_df)
   
    # Rename columns to lowercase
    combined_json = combined_json.rename(
        {col: col.lower() for col in combined_json.columns}
    )
   
    # rename dataframe columns
    school_df = combined_json.rename({
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

    # print(school_df.head(2))

    # dd = school_df.to_pandas()

    # print(dd.info())

    # Load dataframe to parquet file
    school_df.write_parquet(f"{data_dir}/processed_data.parquet")
    print(f"Json files transformed and loaded as parquet to {data_dir} folder")

    school_df.write_database(
        "top_1000_USA_schools", connection=db_engine, if_table_exists="replace"
    )
    print(f"Json files transformed and loaded to database")

    return True

transform_data()