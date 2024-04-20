import pulumi
import json
import pulumi_aws as aws
from vpc import vpc, subnet1, subnet2

# IAM Role for EKS Cluster
eks_role = aws.iam.Role("eks-role",
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Principal": {
                "Service": "eks.amazonaws.com"
            },
            "Effect": "Allow",
            "Sid": ""
        }]
    }),
    tags={
        "Name": "eks-role",
    })

# Attach IAM Policies to the Role
aws.iam.RolePolicyAttachment("eks-cluster-policy",
    role=eks_role.id,
    policy_arn="arn:aws:iam::aws:policy/AmazonEKSClusterPolicy")

aws.iam.RolePolicyAttachment("eks-service-policy",
    role=eks_role.id,
    policy_arn="arn:aws:iam::aws:policy/AmazonEKSServicePolicy")

# Create an EKS Cluster
cluster = aws.eks.Cluster("my-cluster",
    role_arn=eks_role.arn,
    vpc_config=aws.eks.ClusterVpcConfigArgs(
        subnet_ids=[subnet_private.id]  # Use private subnet for the EKS nodes
    ),
    tags={
        "Name": "my-eks-cluster",
    })

# Create a Node Group
node_group = aws.eks.NodeGroup("my-node-group",
    cluster_name=cluster.name,
    node_role_arn=eks_role.arn,
    subnet_ids=[subnet_private.id],  # Use private subnet for the EKS nodes
    scaling_config=aws.eks.NodeGroupScalingConfigArgs(
        desired_size=2,
        max_size=3,
        min_size=1
    ),
    disk_size=20,
    tags={
        "Name": "my-node-group",
    })
