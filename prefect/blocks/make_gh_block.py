# alternative to creating GitHub block in the UI

from prefect.filesystems import GitHub
from utils.snippets import get_config
cfg = get_config()

PREFECT_BLOCKNAME_GCP_BUCKET = cfg['PREFECT_BLOCKNAME_GCP_BUCKET']
GCP_PROJECT_ID = cfg['GCP_PROJECT_ID']
PREFECT_BLOCKNAME_GCP_CREDENTIALS=cfg['PREFECT_BLOCKNAME_GCP_CREDENTIALS']
GCP_BUCKETNAME = cfg['GCP_BUCKETNAME']
PREFECT_BLOCKNAME_GITHUB = cfg['PREFECT_BLOCKNAME_GITHUB']
GITHUB_REPO_PATH = cfg['GITHUB_REPO_PATH']

gh_block = GitHub(name=PREFECT_BLOCKNAME_GITHUB, repository=GITHUB_REPO_PATH)
gh_block.save(PREFECT_BLOCKNAME_GITHUB, overwrite=True)
