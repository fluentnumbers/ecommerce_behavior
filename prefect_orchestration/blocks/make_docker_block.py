# alternative to creating DockerContainer block in the UI

from prefect.infrastructure.docker import DockerContainer
from utils.snippets import get_config
cfg = get_config()
PREFECT_BLOCKNAME_DOCKER = cfg['PREFECT_BLOCKNAME_DOCKER']

docker_block = DockerContainer(
    image="discdiver/prefect:zoom",  # insert your image here
    image_pull_policy="ALWAYS",
    auto_remove=True,
)

docker_block.save(PREFECT_BLOCKNAME_DOCKER, overwrite=True)
