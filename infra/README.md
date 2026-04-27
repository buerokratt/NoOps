# Infrastructure

This directory contains the Terraform configuration for provisioning AWS infrastructure required for Buerokratt environments.

## Purpose

Terraform is used to provision:

- AWS networking (VPC, subnets, security groups)
- EKS cluster
- Worker nodes
- Required AWS addons and base infrastructure components

## Flow

1. Provision infrastructure with Terraform
2. Validate EKS cluster availability
3. Deploy platform/application components through CentOps / ArgoCD

## Structure

```text
infra/
  terraform/
    envs/
    modules/
```

## Usage

```bash
terraform init
terraform plan -var-file="<environment>.tfvars"
terraform apply -var-file="<environment>.tfvars"
```

After infrastructure is created:

```bash
aws eks update-kubeconfig --region <region> --name <cluster-name>
kubectl get nodes
```

Application deployments are handled separately through Kubernetes manifests, Helm charts, or ArgoCD/CentOps.

