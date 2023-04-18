from prefect.deployments import Deployment
from prefect.infrastructure.docker import DockerContainer
from flows import PREFECT_BLOCKNAME_DOCKER

from flows.flow_web_to_gcp import web_to_gcp_parent_flow


docker_block = DockerContainer.load(PREFECT_BLOCKNAME_DOCKER)

docker_dep = Deployment.build_from_flow(
    flow=web_to_gcp_parent_flow,
    name="docker-web_to_gcp",
    infrastructure=docker_block,
)


if __name__ == "__main__":
    docker_dep.apply()
