from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket

# alternative to creating GCP blocks in the UI
# copy your own service_account_info dictionary from the json file you downloaded from google
# IMPORTANT - do not store credentials in a publicly available repository!

cfg = get_config()
PREFECT_BLOCKNAME_GCP_BUCKET = cfg['PREFECT_BLOCKNAME_GCP_BUCKET']
GCP_PROJECT_ID = cfg['GCP_PROJECT_ID']
PREFECT_BLOCKNAME_GCP_CREDENTIALS=cfg['PREFECT_BLOCKNAME_GCP_CREDENTIALS']
GCP_BUCKETNAME = cfg['GCP_BUCKETNAME']

credentials_block = GcpCredentials(
    service_account_info={}  # enter your credentials from the json file
)
credentials_block.save(PREFECT_BLOCKNAME_GCP_CREDENTIALS, overwrite=True)


bucket_block = GcsBucket(
    gcp_credentials=GcpCredentials.load(PREFECT_BLOCKNAME_GCP_CREDENTIALS),
    bucket=GCP_BUCKETNAME,  # insert your  GCS bucket name
)

bucket_block.save(PREFECT_BLOCKNAME_GCP_BUCKET, overwrite=True)
