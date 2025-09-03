from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
)
from constructs import Construct

class EC2Stack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create new VPC
        vpc = ec2.Vpc(self, "VPC", max_azs=2)

        # Create IAM role with Bedrock access
        role = iam.Role(self, "EC2Role",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonBedrockFullAccess")
            ]
        )

        # Create security group with restricted access
        security_group = ec2.SecurityGroup(self, "SecurityGroup",
            vpc=vpc,
            description="Allow SSH from specific IP",
            allow_all_outbound=True
        )
        
        # Add SSH access from specific IP (replace with your IP)
        security_group.add_ingress_rule(
            peer=ec2.Peer.ipv4("110.226.182.141/32"),
            connection=ec2.Port.tcp(22),
            description="SSH access from specific IP"
        )

        # Create key pair
        key_pair = ec2.KeyPair(self, "KeyPair",
            key_pair_name="ec2-keypair"
        )

        # Create EC2 instance
        instance = ec2.Instance(self, "Instance",
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MEDIUM),
            machine_image=ec2.AmazonLinuxImage(),
            vpc=vpc,
            role=role,
            security_group=security_group,
            key_pair=key_pair
        )