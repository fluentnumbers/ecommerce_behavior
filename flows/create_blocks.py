import json
from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket
from prefect.filesystems import GitHub
from prefect.infrastructure.docker import DockerContainer
import os
from prefect_dbt.cloud import DbtCloudCredentials

from dotenv import load_dotenv

load_dotenv()

GCP_CREDENTIALS_PATH = os.environ.get('GCP_CREDENTIALS_PATH')
GCP_BUCKETNAME = os.environ.get('GCP_BUCKETNAME')

PREFECT_BLOCKNAME_GCP_CREDENTIALS = os.environ.get('PREFECT_BLOCKNAME_GCP_CREDENTIALS')
PREFECT_BLOCKNAME_GCP_BUCKET = os.environ.get('PREFECT_BLOCKNAME_GCP_BUCKET')
PREFECT_BLOCKNAME_DOCKER = os.environ.get('PREFECT_BLOCKNAME_DOCKER')
PREFECT_BLOCKNAME_GITHUB = os.environ.get('PREFECT_BLOCKNAME_GITHUB')
PREFECT_BLOCKNAME_DBT = os.environ.get('PPREFECT_BLOCKNAME_DBT')


DBT_USER_ID = os.environ.get('DBT_USER_ID')
DBT_KEY = os.environ.get('DBT_KEY')
DBT_CREDENTIALS_PATH = os.environ.get('DBT_CREDENTIALS_PATH')

GITHUB_REPO_PATH = os.environ.get('GITHUB_REPO_PATH')

DOCKER_USERNAME = os.environ.get('DOCKER_USERNAME')
DOCKER_IMAGE = os.environ.get('DOCKER_IMAGE')

with open(GCP_CREDENTIALS_PATH, 'r') as creds:
    gcp_creds = json.load(creds)


# alternative to creating GCP blocks in the UI
credentials_block = GcpCredentials(
    service_account_info=gcp_creds  # enter your credentials from the json file
)
credentials_block.save(PREFECT_BLOCKNAME_GCP_CREDENTIALS, overwrite=True)
print(f"Created GCP credentials block named {PREFECT_BLOCKNAME_GCP_CREDENTIALS}")

bucket_block = GcsBucket(
    gcp_credentials=GcpCredentials.load(PREFECT_BLOCKNAME_GCP_CREDENTIALS),
    bucket=GCP_BUCKETNAME,  # insert your  GCS bucket name
)

bucket_block.save(PREFECT_BLOCKNAME_GCP_BUCKET, overwrite=True)
print(f"Created GCP bucket block named {PREFECT_BLOCKNAME_GCP_BUCKET}")


# alternative to creating GitHub block in the UI
gh_block = GitHub(name=PREFECT_BLOCKNAME_GITHUB, repository=GITHUB_REPO_PATH)
gh_block.save(PREFECT_BLOCKNAME_GITHUB, overwrite=True)
print(f"Created Github block named {PREFECT_BLOCKNAME_GITHUB}")

# alternative to creating DockerContainer block in the UI
if False:  # currently not in use
    docker_block = DockerContainer(
        image=f"{DOCKER_USERNAME}/{DOCKER_IMAGE}",  # insert your image here
        image_pull_policy="ALWAYS",
        auto_remove=True,
    )

    docker_block.save(PREFECT_BLOCKNAME_DOCKER, overwrite=True)
    print(f"Created Docker block named {PREFECT_BLOCKNAME_DOCKER}")


# alternative to creating DBT block in the UI
if False:  # currently not in use
    credentials_block = DbtCloudCredentials(
            api_key=DBT_KEY,
            account_id=DBT_USER_ID
        )
    credentials_block.save(PREFECT_BLOCKNAME_DBT, overwrite=True)
    print(f"Created DBT block named {PREFECT_BLOCKNAME_DBT}")
