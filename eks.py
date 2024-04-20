import pulumi
import pulumi_aws as aws
from vpc import vpc, subnet1, subnet2

eks_role = aws.iam.Role("eks-role",
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {
                "Service": "eks.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }, {
            "Effect": "Allow",
            "Principal": {
                "Service": "ec2.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }]
    }),
    tags={"Name": "eks-role"})

# Attach IAM policies required for EKS
aws.iam.RolePolicyAttachment("eks-cluster-policy",
    role=eks_role.id,
    policy_arn=aws.iam.get_policy(arn="arn:aws:iam::aws:policy/AmazonEKSClusterPolicy").arn)

aws.iam.RolePolicyAttachment("eks-vpc-resource-controller",
    role=eks_role.id,
    policy_arn=aws.iam.get_policy(arn="arn:aws:iam::aws:policy/AmazonEKSVPCResourceController").arn)

# Create an EKS Cluster
cluster = aws.eks.Cluster("my-cluster",
    role_arn=eks_role.arn,
    vpc_config=aws.eks.ClusterVpcConfigArgs(
        subnet_ids=[subnet1.id, subnet2.id]
    ),
    tags={"Name": "my-eks-cluster"})

# Create an EKS Node Group
node_group = aws.eks.NodeGroup("my-node-group",
    cluster_name=cluster.name,
    node_role_arn=eks_role.arn,
    subnet_ids=[subnet1.id, subnet2.id],
    scaling_config=aws.eks.NodeGroupScalingConfigArgs(
        desired_size=2,
        max_size=3,
        min_size=1
    ),
    disk_size=20,
    instance_types=["t3.small"],
    tags={"Name": "my-eks-node-group"})
