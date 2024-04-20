import pulumi
import json
import pulumi_aws as aws
from vpc import vpc, subnet_private_1, subnet_private_2, subnet_public

# IAM Role for EKS Cluster
eks_role = aws.iam.Role("eks-role",
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {
                "Service": ["eks.amazonaws.com", "ec2.amazonaws.com"]
            },
            "Action": "sts:AssumeRole"
        }]
    }),
    tags={"Name": "eks-role"})

# Attach IAM Policies to the EKS Role
cluster_policy_attachment = aws.iam.RolePolicyAttachment("eks-cluster-policy",
    role=eks_role.name,  # Use the `name` attribute of the `eks_role` object
    policy_arn="arn:aws:iam::aws:policy/AmazonEKSClusterPolicy")

service_policy_attachment = aws.iam.RolePolicyAttachment("eks-service-policy",
    role=eks_role.name,  # Use the `name` attribute of the `eks_role` object
    policy_arn="arn:aws:iam::aws:policy/AmazonEKSServicePolicy")

# IAM Role for EKS Nodes
eks_node_role = aws.iam.Role("eks-node-role",
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {
                "Service": "ec2.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }]
    }),
    tags={"Name": "eks-node-role"})

# Attach IAM Policies to the Node Role
worker_node_policy_attachment = aws.iam.RolePolicyAttachment("eks-worker-node-policy",
    role=eks_node_role.name,  # Use the `name` attribute of the `eks_node_role` object
    policy_arn="arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy")

cni_policy_attachment = aws.iam.RolePolicyAttachment("eks-cni-policy",
    role=eks_node_role.name,  # Use the `name` attribute of the `eks_node_role` object
    policy_arn="arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy")

ecr_policy_attachment = aws.iam.RolePolicyAttachment("ecr-readonly-policy",
    role=eks_node_role.name,  # Use the `name` attribute of the `eks_node_role` object
    policy_arn="arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly")

# Create an EKS Cluster using subnets in different AZs
cluster = aws.eks.Cluster("my-cluster",
    role_arn=eks_role.arn,  # Use the `arn` attribute correctly
    vpc_config=aws.eks.ClusterVpcConfigArgs(
        subnet_ids=[subnet_private_1.id, subnet_private_2.id]
    ),
    tags={"Name": "my-eks-cluster"})

# Create a Node Group
node_group = aws.eks.NodeGroup("my-node-group",
    cluster_name=cluster.name,  # This should correctly reference `cluster.name`
    node_role_arn=eks_node_role.arn,  # Use the `arn` of `eks_node_role`
    subnet_ids=[subnet_private_1.id, subnet_private_2.id],
    scaling_config=aws.eks.NodeGroupScalingConfigArgs(
        desired_size=2,
        max_size=3,
        min_size=1
    ),
    disk_size=20,
    tags={"Name": "my-node-group"})
