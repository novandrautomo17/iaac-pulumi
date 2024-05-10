import pulumi
import pulumi_aws as aws

# Create a VPC
vpc = aws.ec2.Vpc("my-vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_support=True,
    enable_dns_hostnames=True,
    tags={
        "Name": "my-vpc",
    })

# Create Internet Gateway
igw = aws.ec2.InternetGateway("my-igw",
    vpc_id=vpc.id,
    tags={
        "Name": "my-internet-gateway",
    })

# Public Subnet (for Internet-facing Instances)
subnet_public = aws.ec2.Subnet("my-subnet-public",
    vpc_id=vpc.id,
    cidr_block="10.0.11.0/24",
    availability_zone="ap-southeast-3a",
    map_public_ip_on_launch=True,  # Enables public IP assignment
    tags={
    "Name": "my-public-subnet",
    "kubernetes.io/cluster/my-cluster": "shared"
    })

# Private Subnet (for EKS Node Group)
subnet_private_1 = aws.ec2.Subnet("subnet-private-1",
    vpc_id=vpc.id,
    cidr_block="10.0.31.0/24",
    availability_zone="ap-southeast-3a",  # First AZ
    tags={
    "Name": "my-private-subnet-1",
    "kubernetes.io/cluster/my-cluster": "shared"  # Replace 'my-cluster' with the actual cluster name
    })

subnet_private_2 = aws.ec2.Subnet("subnet-private-2",
    vpc_id=vpc.id,
    cidr_block="10.0.41.0/24",
    availability_zone="ap-southeast-3b",  # Second AZ
    tags={"Name": "my-private-subnet-2"})

# Create a Route Table for Public Subnet
route_table_public = aws.ec2.RouteTable("my-route-table-public",
    vpc_id=vpc.id,
    routes=[
        aws.ec2.RouteTableRouteArgs(
            cidr_block="0.0.0.0/0",
            gateway_id=igw.id,
        )
    ],
    tags={
        "Name": "my-route-table-public",
    })

# Associate Public Subnet with Route Table
route_table_assoc_public = aws.ec2.RouteTableAssociation("my-route-table-assoc-public",
    route_table_id=route_table_public.id,
    subnet_id=subnet_public.id)

# Optionally, create a NAT Gateway for Private Subnet to access the internet
nat_gateway = aws.ec2.NatGateway("my-nat-gateway",
    subnet_id=subnet_public.id,  # NAT Gateway must be in a public subnet
    allocation_id=aws.ec2.Eip("nat-eip", vpc=True).id,
    tags={
        "Name": "my-nat-gateway",
    })

# Create a Route Table for Private Subnet
route_table_private = aws.ec2.RouteTable("my-route-table-private",
    vpc_id=vpc.id,
    routes=[
        aws.ec2.RouteTableRouteArgs(
            cidr_block="0.0.0.0/0",
            nat_gateway_id=nat_gateway.id,  # Use NAT Gateway for internet access
        )
    ],
    tags={
        "Name": "my-route-table-private",
    })

# Associate the first private subnet
aws.ec2.RouteTableAssociation("my-route-table-assoc-private-1",
    route_table_id=route_table_private.id,
    subnet_id=subnet_private_1.id)

# Associate the second private subnet
aws.ec2.RouteTableAssociation("my-route-table-assoc-private-2",
    route_table_id=route_table_private.id,
    subnet_id=subnet_private_2.id)

# Create a security group for the EKS nodes
eks_node_sg = aws.ec2.SecurityGroup('eks-node-sg',
    vpc_id=vpc.id,
    description='Security group for EKS nodes',
    ingress=[
        {'protocol': '-1', 'from_port': 0, 'to_port': 0, 'cidr_blocks': ['0.0.0.0/0']},
    ],
    egress=[
        {'protocol': '-1', 'from_port': 0, 'to_port': 0, 'cidr_blocks': ['0.0.0.0/0']},
    ],
    tags={
        "Name": "eks-node-sg"
    }
)