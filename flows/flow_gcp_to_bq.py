from pathlib import Path
from typing import Dict, List
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials
import calendar
import os
from flows import year_months_combinations

from dotenv import load_dotenv

load_dotenv()

GCP_BIGQUERY_DATASET = os.environ.get('GCP_BIGQUERY_DATASET')
GCP_BIGQUERY_TABLE = os.environ.get('GCP_BIGQUERY_TABLE')
GCP_PROJECT_ID = os.environ.get('GCP_PROJECT_ID')

PREFECT_BLOCKNAME_GCP_CREDENTIALS = os.environ.get('PREFECT_BLOCKNAME_GCP_CREDENTIALS')
PREFECT_BLOCKNAME_GCP_BUCKET = os.environ.get('PREFECT_BLOCKNAME_GCP_BUCKET')
PREFECT_BLOCKNAME_DOCKER = os.environ.get('PREFECT_BLOCKNAME_DOCKER')
PREFECT_BLOCKNAME_GITHUB = os.environ.get('PREFECT_BLOCKNAME_GITHUB')

GITHUB_REPO_PATH = os.environ.get('GITHUB_REPO_PATH')

DOCKER_USERNAME = os.environ.get('DOCKER_USERNAME')
DOCKER_IMAGE = os.environ.get('DOCKER_IMAGE')

KAGGLE_DATASET_PATH = os.environ.get('KAGGLE_DATASET_PATH')




@task(retries=3,name='extract_from_gcs',log_prints=True)
def extract_from_gcs(year: int, month: int) -> Path:
    """Download trip data from GCS"""
    gcp_path = f"data/{year}-{calendar.month_abbr[month]}.csv.parquet"
    gcp_block = GcsBucket.load(PREFECT_BLOCKNAME_GCP_BUCKET)
    gcp_block.get_directory(from_path=gcp_path, local_path=f"../data/")
    print(Path(f"../data/{gcp_path}").absolute())
    return Path(f"../data/{gcp_path}")


@task(name='transform')
def read(path: Path) -> pd.DataFrame:
    """Data cleaning example"""
    df = pd.read_parquet(path,)
    df=df.dropna(subset=['user_session'], how='any')
    df['brand'] = df['brand'].fillna('Not defined')
    # print(f"pre: missing passenger count: {df['passenger_count'].isna().sum()}")
    # df["passenger_count"].fillna(0, inplace=True)
    # print(f"post: missing passenger count: {df['passenger_count'].isna().sum()}")
    return df


@task(name='write_to_BigQuery')
def write_bq(df: pd.DataFrame) -> None:
    """Write DataFrame to BiqQuery"""

    gcp_credentials_block = GcpCredentials.load(PREFECT_BLOCKNAME_GCP_CREDENTIALS)

    df.to_gbq(
        destination_table=f"{GCP_BIGQUERY_DATASET}.{GCP_BIGQUERY_TABLE}",
        project_id=GCP_PROJECT_ID,
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append",
    )


@flow(name="gcp_to_bq_parent_flow")
def gcp_to_bq_parent_flow(year_months_combinations:Dict[int,List[int]]=dict([(2019,[10,11,12]),(2020,[1,2])])):
    """Main ETL flow to load data into Big Query"""
    for year in year_months_combinations.keys():
        for month in year_months_combinations[year]:
            path = extract_from_gcs(year, month)
            df = read(path)
            write_bq(df)


if __name__ == "__main__":
    year_months = dict([(2019,[10,11,12]),(2020,[1,2])])
    # year_months = dict([(2020,[1,2])])
    year_months = year_months_combinations
    gcp_to_bq_parent_flow(year_months)
