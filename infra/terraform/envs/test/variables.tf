variable "project_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "aws_region" {
  type = string
}

variable "cluster_version" {
  type = string
}

variable "node_instance_type" {
  type = string
}

variable "node_min_size" {
  type = number
}

variable "node_max_size" {
  type = number
}

variable "node_desired_size" {
  type = number
}

variable "install_argocd" {
  type    = bool
  default = false
}