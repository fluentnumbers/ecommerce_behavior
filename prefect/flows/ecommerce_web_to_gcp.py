
from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint
from prefect.tasks import task_input_hash
from datetime import timedelta
import calendar
import os
from utils.snippets import get_config

cfg = get_config()
PREFECT_BLOCKNAME_GCP_BUCKET = cfg['PREFECT_BLOCKNAME_GCP_BUCKET']
KAGGLE_DATASET_PATH = cfg['KAGGLE_DATASET_PATH']

# yearmonth2filename = {
#                       "2019_10":"2019-Oct.csv",
#                       "2019_11":"2019-Nov.csv",
#                       "2019_12":"2019-Dec.csv",
#                       "2020_01":"2020-Jan.csv",
#                       "2020_02":"2020-Feb.csv",
#                       }

# @task(retries=1)
def fetch(local_path: str):
    df = pd.read_csv(local_path, compression='zip',chunksize=1_000_000)
    return df


@task(log_prints=True)
def clean(df: pd.DataFrame,) -> pd.DataFrame:
    """Fix dtype issues"""
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df


@task(name='web_to_gcp_bucket_write_local')
def write_local(df: pd.DataFrame, path: Path) -> Path:
    """Write DataFrame out locally as parquet file"""

    if not os.path.isfile(path):
        df.to_parquet(path, engine='fastparquet')
    else:
        df.to_parquet(path, engine='fastparquet', append=True)
    # df.to_parquet(path, )
    return path


@task(name='web_to_gcp_bucket_write_gcs')
def write_gcs(path: Path) -> None:
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load(PREFECT_BLOCKNAME_GCP_BUCKET)
    gcs_block.upload_from_path(from_path=path, to_path=path)
    return


@flow(name="web_to_gcp_bucket_subflow",log_prints=True)
def etl_web_to_gcs(year: int, month: int, ) -> None:
    """The main ETL function"""
    source_filename =f"{year}-{calendar.month_abbr[month]}.csv"
    os.system(f"kaggle datasets download {KAGGLE_DATASET_PATH} -f {source_filename} -p 'data/'")
    local_path = f'data/{source_filename}.zip'
    local_parquet = Path(f"data/{source_filename}.parquet")

    df_iter = fetch(local_path)
    for i, df in enumerate(df_iter):
        df_clean = clean(df,)
        local_parquet = write_local(df_clean, local_parquet)
    write_gcs(local_parquet)
    os.remove(local_parquet)


@flow(name="web_to_gcp_bucket_parent_flow")
def web_to_gcp_parent_flow(
    months: list[int], year: int,
):
    # assert all([f"{year}_{m}" in yearmonth2filename.keys() for m in months]), \
        # f"Only {yearmonth2filename.keys()} year-month combinations available"
    for month in months:
        etl_web_to_gcs(year, month, )


if __name__ == "__main__":
    months = [11]
    year = 2019
    web_to_gcp_parent_flow(months, year, )
