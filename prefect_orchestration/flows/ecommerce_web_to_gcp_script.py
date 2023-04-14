import urllib
from urllib.parse import urlencode
import pandas as pd
import wget
import requests
from prefect_orchestration.flows.ecommerce_web_to_gcp import yearmonth2filename, fetch, clean, write_local
import os
import kaggle
kaggle.api.authenticate()

if __name__ == "__main__":
    month = 12
    year = 2019
    dataset_name = 'mkechinov/ecommerce-events-history-in-cosmetics-shop'
    dataset_file =yearmonth2filename[f"{year}_{month}"]
    os.system(f"kaggle datasets download {dataset_name} -f {dataset_file} -p 'data/'")
    local_path = f'data/{dataset_file}'
    df = pd.read_csv(local_path+'.zip', compression='zip')



    df = fetch.fn(local_path+'.zip')
    df_clean = clean.fn(df,)
    path = write_local.fn(df_clean, dataset_file)


