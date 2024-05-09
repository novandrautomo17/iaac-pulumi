import pulumi
import pulumi_aws as aws
from vpc import subnet_public, subnet_private_1, subnet_private_2, vpc


size = 't2.micro'
ami = aws.ec2.get_ami(most_recent="true",
                  owners=["137112412989"],
                  filters=[{"name":"name","values":["amzn-ami-hvm-*"]}])


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
    instance_type="size",
    vpc_security_group_ids=[bastion_sg.id],
    ami="ami.id",  # Make sure to replace with the correct AMI for your region
    subnet_id=subnet_public.id,
    associate_public_ip_address=True,
    key_name="my-keypair")  # Ensure you have this keypair created
