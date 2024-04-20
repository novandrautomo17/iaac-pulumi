import pulumi
from vpc import vpc, subnet, igw, route_table, route_table_assoc
from bastion_host import bastion, bastion_sg
from eks import cluster, node_group

# Create an AWS provider instance with the specified region
aws_provider = aws.Provider("aws", region="ap-southeast-1")

pulumi.export("cluster_name", cluster.name)
pulumi.export("node_group_name", node_group.node_group_name)
pulumi.export("bastion_ip", bastion.public_ip)
