HELL := /bin/bash

include .env
export


ifneq ("$(wildcard $(DBT_CREDENTIALS_PATH))","")
	export $(shell jq -r 'to_entries|map("DBT_\(.key|ascii_upcase)=\(.value|tostring)")|.[]' ${DBT_CREDENTIALS_PATH})
endif
# export $(shell jq -r 'to_entries|map("KAGGLE_\(.key|ascii_upcase)=\(.value|tostring)")|.[]' ${KAGGLE_CREDENTIALS_PATH})
# .PHONY: print_vars
# print_vars:
#	 @echo "KAGGLE_USERNAME = ${KAGGLE_USERNAME}"
#	 @echo "KAGGLE_KEY = ${KAGGLE_KEY}"

.EXPORT_ALL_VARIABLES:

TF_VAR_project = ${GCP_PROJECT_ID}
TF_VAR_region = $(GCP_REGION)
TF_VAR_BQ_DATASET = $(GCP_BIGQUERY_DATASET)
TF_VAR_BQ_DATASET_DBT_DEV = $(DBT_DEV_DATASET_NAME)
TF_VAR_BQ_DATASET_DBT_PROD = $(DBT_PROD_DATASET_NAME)
TF_VAR_data_lake_bucket = $(GCP_BUCKETNAME)

GOOGLE_APPLICATION_CREDENTIALS = ${GCP_CREDENTIALS_PATH}

REPO_DIR = ${PWD}


#######################################################################

test:
	echo ${DOCKER_VOLUME_PATH}






#############################################
################# VM ENVIRONMENT
##############################################
vm_install_terraform:
	cd /home/$(USER);\
	mkdir bin;\
	cd bin;\
	wget https://releases.hashicorp.com/terraform/1.3.9/terraform_1.3.9_linux_amd64.zip;\
	unzip -o terraform_1.3.9_linux_amd64.zip;\
	rm terraform_1.3.9_linux_amd64.zip

vm_install_anaconda:
	cd /home/$(USER);\
	wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh;\
	bash Anaconda3-2022.10-Linux-x86_64.sh;\
	source .bashrc

# make vm_install_docker
vm_install_docker:
	sudo apt-get install docker.io -y;\
	sudo groupadd docker;\
	sudo gpasswd -a ${USER} docker
	sudo service docker restart

# make vm_install_docker_compose
vm_install_docker_compose:
	sudo apt install docker docker-compose python3-pip make -y
	sudo chmod 666 /var/run/docker.sock

vm-setupdocker:
	sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
	sudo chmod +x /usr/local/bin/docker-compose
	docker-compose --version

vm_setup:
	cd /home/$(USER)/;\
	sudo apt-get update -y;\
	sudo apt-get install unzip;\
	sudo apt-get install wget;\
	cd $(REPO_DIR);\
	$(MAKE) vm_install_terraform;\
	$(MAKE) vm_install_docker;\
	$(MAKE) vm_install_docker_compose;\
	gcloud auth activate-service-account --key-file ${GOOGLE_APPLICATION_CREDENTIALS};\


#############################################
################# TERRAFORM
##############################################
terraform_setup:
	@echo "Initialiaze GCP infrastructure"
	cd terraform; \
	terraform init; \
	terraform plan; \
	terraform apply --auto-approve;

#############################################
################# Docker
##############################################

# make docker_build_image
docker_build_image:
	docker build --no-cache --network=host -f dockerfile -t python_prefect_dbt .

# make docker_clean
docker_clean:
	docker-compose down --remove-orphans

# make docker_remove_all
docker_remove_all:
	if [ -n "$$(docker ps -aq)" ]; then \
		docker rm $$(docker ps -aq); \
	else \
		echo "No containers found."; \
	fi
	if [ -n "$$(docker images -aq)" ]; then \
		docker rmi $$(docker images -aq); \
	else \
		echo "No images found."; \
	fi
	if [ -n "$$(docker images -aq)" ]; then \
		docker volume rm $(docker volume ls -q) \
	else \
		echo "No images found."; \
	fi

#############################################
################# PREFECT
##############################################
# make prefect_server_up
prefect_server_up:
	docker-compose --profile server up --detach
	@echo "Orion is up: http://localhost:4200/"
	@echo "Start agent with 'make prefect_agent_start'"

# make prefect_agent_up
prefect_agent_up:
	docker-compose --profile agent up --detach
	@echo "Prefect agent is up, listening to queue 'default'"
	@echo "Create necessary Prefect blocks by 'make prefect_create_blocks'"

# make prefect_create_blocks
prefect_create_blocks:
	docker-compose run job-python flows/create_blocks.py
	@echo "Initialiaze prefect blocks: http://localhost:4200/blocks"
	@echo "Build and apply deployments by 'make prefect_build_deployments'"

# make prefect_build_deployments
prefect_build_deployments:
	docker-compose run job-prefect deployment build flows/flow_web_to_gcp.py:web_to_gcp_parent_flow -n "web to GCP"
	docker-compose run job-prefect deployment apply web_to_gcp_parent_flow-deployment.yaml
	@echo "Initialized prefect deployment flows/flow_web_to_gcp.py"

	docker-compose run job-prefect deployment build flows/flow_gcp_to_bq.py:gcp_to_bq_parent_flow -n "GCP to BQ"
	docker-compose run job-prefect deployment apply gcp_to_bq_parent_flow-deployment.yaml
	@echo "Initialized prefect deployment flows/flow_gcp_to_bq.py"

	@echo "Run deployment to upload data from Kaggle to Google Storage: 'make prefect_run_web2gcp'"

prefect_run_web2gcp: 
	prefect deployment run "web_to_gcp_parent_flow/web to GCP" 	 --param year_months_combinations='{"2019": [ 10, 11, 12 ], "2020": [ 1, 2 ]}'	
	@echo "Runnning flows/flow_web_to_gcp..."

prefect_run_gcp2bq:
	prefect deployment run "gcp_to_bq_parent_flow/GCP to BQ" --param year_months_combinations='{"2019": [ 10, 11, 12 ], "2020": [ 1, 2 ]}'
	@echo "Runnning flows/flow_gco_to_bq..."

