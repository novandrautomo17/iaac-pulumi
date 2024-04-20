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
        "Name": "my-igw",
    })

# Create Subnets in different Availability Zones
subnet1 = aws.ec2.Subnet("my-subnet-1",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    availability_zone="ap-southeast-1a",
    map_public_ip_on_launch=True,
    tags={
        "Name": "my-subnet-1",
    })

subnet2 = aws.ec2.Subnet("my-subnet-2",
    vpc_id=vpc.id,
    cidr_block="10.0.2.0/24",
    availability_zone="ap-southeast-1b",
    map_public_ip_on_launch=True,
    tags={
        "Name": "my-subnet-2",
    })

# Create a Route Table and Associate it with Subnets
route_table = aws.ec2.RouteTable("my-route-table",
    vpc_id=vpc.id,
    routes=[
        aws.ec2.RouteTableRouteArgs(
            cidr_block="0.0.0.0/0",
            gateway_id=igw.id,
        )
    ],
    tags={
        "Name": "my-route-table",
    })

# Association for the first subnet
route_table_assoc1 = aws.ec2.RouteTableAssociation("my-route-table-assoc1",
    route_table_id=route_table.id,
    subnet_id=subnet1.id)

# Association for the second subnet
route_table_assoc2 = aws.ec2.RouteTableAssociation("my-route-table-assoc2",
    route_table_id=route_table.id,
    subnet_id=subnet2.id)
