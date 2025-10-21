terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket         = "cv-terraform-state-ec88c66e"
    key            = "terraform.tfstate"
    region         = "us-west-2"
    dynamodb_table = "cv-terraform-locks"
    encrypt        = true
  }
}

provider "aws" {
  region = "us-west-2"
}
