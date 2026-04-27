provider "aws" {
  region = var.aws_region
}

provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"
  }
}