# Project Setup Guide

This guide walks you through the setup of a Pulumi project that creates an AWS EKS cluster along with the necessary VPC configurations and a bastion host for secure access. We will use Pulumi with Python, configure AWS CLI, and set up kubectl to interact with the EKS cluster.

Prerequisites:
- AWS Account
- GitHub Account
- Git installed on your machine
- Python installed on your machine
- Tools Installation


#### 1. AWS CLI
Install the AWS CLI to interact with AWS services directly from your terminal:
macOS:
```bash
brew install awscli
```

Linux:
```bash
sudo apt-get install awscli
```

Windows: Download from AWS CLI and install using the provided installer.
Configure AWS CLI:
```bash
aws configure
```

This command will prompt you to enter your AWS credentials which include:
- AWS Access Key ID
- AWS Secret Access Key
- Default region name
- Default output format


#### 2. Pulumi
Install Pulumi to manage your infrastructure as code:

macOS and Linux:
```bash
curl -fsSL https://get.pulumi.com | sh
```

Windows: Download the installer from Pulumi's website.

Set up the Pulumi project:
```bash
pulumi new python
```
This command creates a new Pulumi project in Python and includes initializing a virtual environment and installing the pulumi Python package.

#### 3. kubectl
Install kubectl to manage the Kubernetes cluster:

macOS:
```bash
brew install kubectl 
```

Linux:
```bash
sudo apt-get install kubectl
```

Windows: Download from Kubernetes.io and follow the installation instructions.

## Creating Infrastructure
Clone the GitHub repository where the Pulumi project is located:
```bash
git clone https://github.com/novandrautomo17/iaac-pulumi.git
cd iaac-pulumi
```

Set up Python environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install pulumi pulumi_aws
```

Install Python dependencies:
```bash
pip install -r requirements.txt
```

Initialize a new stack (if not already done):
```bash
pulumi stack init dev
```

Set the AWS region:
```bash
pulumi config set aws:region ap-southeast-1 #change the region accordingly
```


## Preview and deploy the infrastructure:

```bash
pulumi preview
```

```bash
pulumi up
```

## Accessing the EKS Cluster
### Configure kubectl to connect to your new EKS cluster:

```bash
pulumi stack output kubeconfig > kubeconfig.yaml
export KUBECONFIG=$PWD/kubeconfig.yaml
kubectl get nodes
```


### Cleaning Up
To destroy the resources:
```bash
pulumi destroy
```

To remove the stack:
```bash
pulumi stack rm dev
```
