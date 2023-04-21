variable "data_lake_bucket" {
  description = "GCP data lake bucket name"
}

# ProjectID must match your projectID (not project name!!!) in GCP (also available in your GCP auth .json file)
variable "project" {
  description = "ProjectID"
}

# Set the bucket location as for your VM
variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  type = string
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default = "STANDARD"
}

# BigQuery dataset name (alpha-numeric + underscores)
variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type = string
}

# BigQuery dataset name (alpha-numeric + underscores)
variable "BQ_DATASET_DBT_DEV" {
  description = "BigQuery Dataset where the DBT development models will write into"
  type = string
}

# BigQuery dataset name (alpha-numeric + underscores)
variable "BQ_DATASET_DBT_PROD" {
  description = "BigQuery Dataset where the DBT deployment models will write into"
  type = string
}