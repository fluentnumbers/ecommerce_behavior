from prefect_dbt.cloud import DbtCloudCredentials
from prefect_gcp.cloud_storage import GcsBucket

from flows import DBT_USER_ID, PREFECT_BLOCKNAME_DBT


def dbt_block(api_key: str, account_id:int) -> None:
    credentials_block = DbtCloudCredentials(
        api_key=api_key,
        account_id=account_id
    )
    credentials_block.save(PREFECT_BLOCKNAME_DBT, overwrite=True)
    return None


if __name__=="__main__":
    # https://docs.getdbt.com/faqs/accounts/find-user-id

    api_key = "" #enter dbt api key
    account_id = DBT_USER_ID #enter dbt account id
    dbt_block(api_key, account_id)