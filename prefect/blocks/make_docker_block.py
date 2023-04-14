# alternative to creating DockerContainer block in the UI

from prefect.infrastructure.docker import DockerContainer
from utils.snippets import get_config
cfg = get_config()
PREFECT_BLOCKNAME_DOCKER = cfg['PREFECT_BLOCKNAME_DOCKER']
DOCKER_USERNAME = cfg['DOCKER_USERNAME']
DOCKER_IMAGE = cfg['DOCKER_IMAGE']

docker_block = DockerContainer(
    image=f"{DOCKER_USERNAME}/{DOCKER_IMAGE}",  # insert your image here
    image_pull_policy="ALWAYS",
    auto_remove=True,
)

docker_block.save(PREFECT_BLOCKNAME_DOCKER, overwrite=True)
