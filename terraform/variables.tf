locals {
  data_lake_bucket = "ecommerce"  # Storage bucket name
}

# ProjectID must match your projectID (not project name!!!) in GCP (also available in your GCP auth .json file)
variable "project" {
  description = "ProjectID"
  default = "ecommerce-behavior-381716"
}

# Set the bucket location as for your VM
variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  default = "europe-west4"
  type = string
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default = "STANDARD"
}

# BigQuery dataset name
variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type = string
  default = "ecommerce"
}
