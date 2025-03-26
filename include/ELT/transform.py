from io import BytesIO

import polars as pl

from .auth import blob_client
from .config import logger

# from .config import data_dir


def get_data_from_datalake()-> pl.DataFrame:
    """
    Downloads a parquet file from Azure Blob Storage 
    and reads it into a Polars DataFrame.
    
    Returns:
     pl.DataFrame: DataFrame read from the downloaded parquet file.
    """

    stream_downloader = blob_client.download_blob()
    stream = BytesIO()
    stream_downloader.readinto(stream)
    parquet_data:pl.DataFrame = pl.read_parquet(stream, use_pyarrow=True)
    
    logger.info("Data downloaded from data lake successfully")
    
    return parquet_data


def transform_data() -> pl.DataFrame:
    """
    Transforms the data by renaming columns and removing duplicates.

    Returns:
        pl.DataFrame: Transformed Polars DataFrame.
    """

    response_df: pl.DataFrame = get_data_from_datalake()

    # Rename columns to lowercase
    response_df = response_df.rename(
        {col: col.lower() for col in response_df.columns}
    )
   
    # rename dataframe columns
    school_df:pl.DataFrame = response_df.rename({
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
    
    # Drop duplicate values
    school_df = school_df.unique()


    # Load dataframe to parquet file
    # school_df.write_parquet(f"{data_dir}/processed_data.parquet")
    # print(f"Json files transformed and loaded as parquet to {data_dir} folder")
    
    logger.info("Data transformed successfully. Ready to be loaded to Database")
    
    return school_df

