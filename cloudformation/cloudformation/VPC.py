import aws_cdk as cdk
from aws_cdk import (
    aws_ec2 as ec2
)
from constructs import Construct

class VPC(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = ec2.Vpc(self, "PBL_VPC",
                           cidr="10.0.0.0/16",
                           max_azs=1,
                           nat_gateways=1,
                           subnet_configuration=[
                               ec2.SubnetConfiguration(
                                   name="PublicSubnet",
                                   subnet_type=ec2.SubnetType.PUBLIC,
                                   cidr_mask=24,
                               ),
                               ec2.SubnetConfiguration(
                                   name="HoneyPotSubnet",
                                   subnet_type=ec2.SubnetType.PUBLIC,
                                   cidr_mask=24
                               ),
                               ec2.SubnetConfiguration(
                                   name="PrivateSubnet",
                                   subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
                                   cidr_mask=24
                               )
                           ]
        )
