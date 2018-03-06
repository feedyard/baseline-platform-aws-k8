terraform {
  required_version = ">= 0.11"

  backend "s3" {
  }
}

provider "aws" {
  version = "~> 1.10"
  region = "${var.cluster_aws_region}"
}

variable "cluster_aws_region" { default = "us-east-1" }