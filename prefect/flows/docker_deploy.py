from prefect.deployments import Deployment
from prefect.infrastructure.docker import DockerContainer

from prefect.flows.ecommerce_web_to_gcp import web_to_gcp_parent_flow
from utils.snippets import get_config

cfg = get_config()
PREFECT_BLOCKNAME_DOCKER = cfg['PREFECT_BLOCKNAME_DOCKER']

docker_block = DockerContainer.load(PREFECT_BLOCKNAME_DOCKER)

docker_dep = Deployment.build_from_flow(
    flow=web_to_gcp_parent_flow,
    name="docker-web_to_gcp",
    infrastructure=docker_block,
)


if __name__ == "__main__":
    docker_dep.apply()
