SHELL := /bin/bash

include .env
export


export $(shell jq -r 'to_entries|map("KAGGLE_\(.key|ascii_upcase)=\(.value|tostring)")|.[]' ${KAGGLE_CREDENTIALS_PATH})
export $(shell jq -r 'to_entries|map("DBT_\(.key|ascii_upcase)=\(.value|tostring)")|.[]' ${DBT_CREDENTIALS_PATH})
.PHONY: print_vars
print_vars:
	@echo "KAGGLE_USERNAME = ${KAGGLE_USERNAME}"
	@echo "KAGGLE_KEY = ${KAGGLE_KEY}"

.EXPORT_ALL_VARIABLES:

TF_VAR_project = ${GCP_PROJECT_ID}
TF_VAR_region = $(GCP_REGION)
TF_VAR_BQ_DATASET = $(GCP_BIGQUERY_DATASET)
TF_VAR_BQ_DATASET_DBT_DEV = $(DBT_DEV_DATASET_NAME)
TF_VAR_BQ_DATASET_DBT_PROD = $(DBT_PROD_DATASET_NAME)
TF_VAR_data_lake_bucket = $(GCP_BUCKETNAME)

GOOGLE_APPLICATION_CREDENTIALS = ${GCP_CREDENTIALS_PATH}

REPO_DIR = ${PWD}
# export $(echo $values | jq -r 'to_entries|map("KAGGLE_\(.key|ascii_upcase)=\(.value|tostring)")|.[]' ${KAGGLE_CREDENTIALS_PATH})
# for s in $(jq -r 'to_entries|map("KAGGLE_\(.key|ascii_upcase)=\(.value|tostring)")|.[]' ${KAGGLE_CREDENTIALS_PATH} ); do export '%s\n' "$s"; done


#######################################################################

test:
	echo ${KAGGLE_KEY}

vm_install_anaconda:
	cd /home/$(USER);\
	wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh;\
	bash Anaconda3-2022.10-Linux-x86_64.sh;\
	source .bashrc

# vm_install_docker:
# 	sudo apt-get install docker.io;\
# 	sudo groupadd docker;\
# 	sudo gpasswd -a ${USER} docker;\
# 	RESTART
# 	# RESTAAAAAAAAAAAAAAAAAAAAART
# 	# sudo service docker restart

vm_install_terraform:
	cd /home/$(USER);\
	mkdir bin;\
	cd bin;\
	wget https://releases.hashicorp.com/terraform/1.3.9/terraform_1.3.9_linux_amd64.zip;\
	unzip -o terraform_1.3.9_linux_amd64.zip


# vm_install_docker_compose:
# 	sudo apt-get update -y
# 	sudo apt install docker docker-compose python3-pip make -y
# 	sudo chmod 666 /var/run/docker.sock


# copy gcp creds
# copy kaggle creds, dbt as json
# pip clone
# install anaconda, docker, compose,
# install req


#############################################
################# VM ENVIRONMENT
##############################################
vm_setup:
	cd /home/$(USER)/;\
	sudo apt-get update -y;\
	sudo apt-get install unzip;\
	sudo apt-get install wget;\
	cd $(REPO_DIR);\
	$(MAKE) vm_install_terraform;\
	@gcloud auth activate-service-account --key-file ${GOOGLE_APPLICATION_CREDENTIALS};\

	conda create -n <my-env-name>;\
	conda install python=3.10;\
	pip install -r requirements.txt;\



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
################# PREFECT
##############################################
prefect_start_ui:
	@echo "prefect orion start";\
	@prefect config set PREFECT_API_URL=http://localhost:4200/api;\
	@prefect orion start;

prefect_create_blocks:
	@echo "Initialiaze prefect blocks"
	@python flows/create_blocks.py

prefect_build_deployment:
	@echo "Initialize prefect deployment"
	@prefect deployment build flows/flow_web_to_gcp.py:web_to_gcp_parent_flow -n "web to GCP"
	@prefect deployment build flows/flow_gcp_to_bq.py:gcp_to_bq_parent_flow -n "GCP to BQ"

	@prefect deployment apply web_to_gcp_parent_flow-deployment.yaml
	@prefect deployment apply gcp_to_bq_parent_flow-deployment.yaml

prefect_agent_start:
	@echo "Start prefect agent"
	prefect agent start --work-queue "default"

prefect_run_web2gcp: 
	prefect deployment run "web_to_gcp_parent_flow/web to GCP" 	 --param year_months_combinations='{"2019": [ 10, 11, 12 ], "2020": [ 1, 2 ]}'	

prefect_run_gcp2bq:
	prefect deployment run "gcp_to_bq_parent_flow/GCP to BQ" --param year_months_combinations='{"2019": [ 10, 11, 12 ], "2020": [ 1, 2 ]}'

# prefect_run_deployments: prefect_run_web2gcp prefect_run_gcp2bq	

