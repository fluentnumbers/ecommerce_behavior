from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials
import calendar

from utils.snippets import get_config

cfg = get_config()
PREFECT_BLOCKNAME_GCP_BUCKET = cfg['PREFECT_BLOCKNAME_GCP_BUCKET']
GCP_PROJECT_ID = cfg['GCP_PROJECT_ID']
PREFECT_BLOCKNAME_GCP_CREDENTIALS=cfg['PREFECT_BLOCKNAME_GCP_CREDENTIALS']
GCP_BIGQUERY_DATASET = cfg['GCP_BIGQUERY_DATASET']
GCP_BIGQUERY_TABLE = cfg['GCP_BIGQUERY_TABLE']

@task(retries=3,name='extract_from_gcs',log_prints=True)
def extract_from_gcs(year: int, month: int) -> Path:
    """Download trip data from GCS"""
    gcs_path = f"data/{year}-{calendar.month_abbr[month]}.csv.parquet"
    gcs_block = GcsBucket.load(PREFECT_BLOCKNAME_GCP_BUCKET)
    gcs_block.get_directory(from_path=gcs_path, local_path=f"../data/")
    print(Path(f"../data/{gcs_path}").absolute())
    return Path(f"../data/{gcs_path}")


@task(name='transform')
def read(path: Path) -> pd.DataFrame:
    """Data cleaning example"""
    df = pd.read_parquet(path,)
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


@flow(name="gcs_to_bq_parent_flow")
def gcs_to_bq(month:int,year:int):
    """Main ETL flow to load data into Big Query"""
    path = extract_from_gcs(year, month)
    df = read(path)
    write_bq(df)


if __name__ == "__main__":
    month = 12
    year = 2019
    gcs_to_bq(month=month,year=year)
