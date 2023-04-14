
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

yearmonth2filename = {
                      "2019_10":"2019-Oct.csv",
                      "2019_11":"2019-Nov.csv",
                      "2019_12":"2019-Dec.csv",
                      "2020_01":"2020-Jan.csv",
                      "2020_02":"2020-Feb.csv",
                      }

@task(retries=3)
def fetch(local_path: str) -> pd.DataFrame:
    df = pd.read_csv(local_path, compression='zip')
    return df


@task(log_prints=True)
def clean(df: pd.DataFrame,) -> pd.DataFrame:
    """Fix dtype issues"""
    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df


@task()
def write_local(df: pd.DataFrame, dataset_file: str) -> Path:
    """Write DataFrame out locally as parquet file"""
    path = Path(f"data/{dataset_file}.parquet")
    df.to_parquet(path, )
    return path


@task()
def write_gcs(path: Path) -> None:
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load(PREFECT_BLOCKNAME_GCP_BUCKET)
    gcs_block.upload_from_path(from_path=path, to_path=path)
    return


@flow(name="web_to_gcp_bucket_subflow")
def etl_web_to_gcs(year: int, month: int, ) -> None:
    """The main ETL function"""
    dataset_file =f"{year}-{calendar.month_abbr[month]}.csv"
    os.system(f"kaggle datasets download {KAGGLE_DATASET_PATH} -f {dataset_file} -p 'data/'")
    local_path = f'data/{dataset_file}.zip'

    df = fetch(local_path)
    df_clean = clean(df,)
    path = write_local(df_clean, dataset_file)
    write_gcs(path)


@flow(name="web_to_gcp_bucket_parent_flow")
def etl_parent_flow(
    months: list[int] = [12], year: int = 2019,
):
    assert all([f"{year}_{m}" in yearmonth2filename.keys() for m in months]), \
        f"Only {yearmonth2filename.keys()} year-month combinations available"
    for month in months:
        etl_web_to_gcs(year, month, )


if __name__ == "__main__":
    months = [12]
    year = 2019
    etl_parent_flow(months, year, )
