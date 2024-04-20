import pulumi
import pulumi_aws as aws
from vpc import subnet, vpc

# IAM Role for EKS
eks_role = aws.iam.Role("eks-role",
    assume_role_policy="""{
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Effect": "Allow",
            "Principal": {
                "Service": "eks.amazonaws.com"
            }
        }]
    }""")

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
        subnet_ids=[subnet.id]
    ))

# Create a Node Group
node_group = aws.eks.NodeGroup("my-node-group",
    cluster_name=cluster.name,
    node_role_arn=eks_role.arn,
    subnet_ids=[subnet.id],
    scaling_config=aws.eks.NodeGroupScalingConfigArgs(
        desired_size=2,
        max_size=3,
        min_size=1
    ),
    disk_size=20)
