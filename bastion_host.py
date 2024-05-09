import pulumi
import pulumi_aws as aws
from vpc import subnet_public, subnet_private_1, subnet_private_2, vpc

# Security Group for the Bastion Host
bastion_sg = aws.ec2.SecurityGroup("bastion-sg",
    vpc_id=vpc.id,
    description="Allow SSH inbound traffic",
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            from_port=22,
            to_port=22,
            protocol="tcp",
            cidr_blocks=["0.0.0.0/0"],
        )
    ],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            from_port=0,
            to_port=0,
            protocol="-1",
            cidr_blocks=["0.0.0.0/0"],
        )
    ])

# EC2 Bastion Host
bastion = aws.ec2.Instance("my-bastion",
    instance_type="t2.micro",
    vpc_security_group_ids=[bastion_sg.id],
    ami="ami-0ed62be0fb8004fc6",  # Make sure to replace with the correct AMI for your region
    subnet_id=subnet_public.id,
    associate_public_ip_address=True,
    key_name="my-keypair")  # Ensure you have this keypair created
