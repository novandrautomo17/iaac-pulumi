import pulumi
from vpc import vpc, subnet_public, subnet_private, igw, route_table_assoc_private, route_table_assoc_public
from bastion_host import bastion, bastion_sg
from eks import cluster, node_group

pulumi.export("cluster_name", cluster.name)
pulumi.export("node_group_name", node_group.node_group_name)
pulumi.export("bastion_ip", bastion.public_ip)
