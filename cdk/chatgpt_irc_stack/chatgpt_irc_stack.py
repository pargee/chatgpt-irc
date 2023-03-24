from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_s3 as s3,
)


class ChatgptIrcStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a VPC
        vpc = ec2.Vpc(self, "ChatGPTVpc", max_azs=2)

        # Define a security group
        security_group = ec2.SecurityGroup(
            self, "ChatGPTSecurityGroup",
            vpc=vpc,
            description="Allow SSH and IRC traffic",
            allow_all_outbound=True
        )

        # Allow SSH (port 22) and IRC (port 6667) traffic
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(22),
            "Allow SSH traffic"
        )
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(6667),
            "Allow IRC traffic"
        )

        # Define the IAM role for the instance
        instance_role = iam.Role(
            self, "ChatGPTInstanceRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com")
        )

        # Define the instance user data (script to be executed on launch)
        user_data = ec2.UserData.for_linux()
        user_data.add_commands(
            "yum update -y",
            "yum install -y python38",
            "yum install -y git",
            "pip3 install --upgrade pip",
            "pip3 install irc openai"
        )

        # Create the EC2 instance
        ec2_instance = ec2.Instance(
            self, "ChatGPTInstance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux(),
            vpc=vpc,
            security_group=security_group,
            role=instance_role,
            user_data=user_data,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            key_name="ChatGPTInstance"
        )
