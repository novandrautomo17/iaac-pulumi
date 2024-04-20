import pulumi
import json
import pulumi_aws as aws
from vpc import vpc, subnet_private_1, subnet_private_2, subnet_public

# IAM Role for EKS Cluster
node_role = aws.iam.Role("eks-node-role",
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "ec2.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }),
    tags={"Name": "eks-node-role"})

# Attach necessary policies to the Node Role
aws.iam.RolePolicyAttachment("eks-worker-node-policy",
    role=node_role.id,
    policy_arn="arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy")

aws.iam.RolePolicyAttachment("eks-cni-policy",
    role=node_role.id,
    policy_arn="arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy")

aws.iam.RolePolicyAttachment("ecr-readonly-policy",
    role=node_role.id,
    policy_arn="arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly")


# Create an EKS Cluster using subnets in different AZs
cluster = aws.eks.Cluster("my-cluster",
    role_arn=eks_role.arn,
    vpc_config=aws.eks.ClusterVpcConfigArgs(
        subnet_ids=[subnet_private_1.id, subnet_private_2.id],
        # Optionally specify the security group
        security_group_ids=[some_security_group_id]
    ),
    tags={"Name": "my-eks-cluster"})


# Create a Node Group
node_group = aws.eks.NodeGroup("my-node-group",
    cluster_name=cluster.name,
    node_role_arn=node_role.arn,
    subnet_ids=[subnet_private_1.id, subnet_private_2.id],
    scaling_config=aws.eks.NodeGroupScalingConfigArgs(
        desired_size=2,
        max_size=3,
        min_size=1
    ),
    disk_size=20,
    instance_types=["t3.medium"],
    ami_type="AL2_x86_64",
    remote_access=aws.eks.NodeGroupRemoteAccessArgs(
        ec2_ssh_key="my-keypair",
        source_security_group_ids=[some_security_group_id]
    ),
    tags={"Name": "my-node-group"})

