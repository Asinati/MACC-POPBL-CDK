import aws_cdk as cdk
from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam
)
from constructs import Construct

with open(
        "C:\\Users\\Asier\\Documents\\MU\\AWS\\Cloudformation\\cloudformation\\user_data\\OrderHoneyPot_userData.sh") as sh:
    user_data = sh.read()


class EC2_OrderHoneyPot(cdk.Stack):

    def __init__(self, scope: Construct, id: str, vpc: ec2.Vpc, sg: ec2.SecurityGroup, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.orderhoneypotEC2 = ec2.Instance(self, 'Order HoneyPot',
                                             vpc=vpc,
                                             private_ip_address='10.0.1.21',
                                             vpc_subnets=ec2.SubnetSelection(
                                                 subnet_group_name='HoneyPotSubnet'
                                             ),
                                             instance_type=ec2.InstanceType('t3.large'),
                                             machine_image=ec2.GenericLinuxImage({
                                                 "us-east-1": "ami-05135c3a41d0217f8"
                                             }),
                                             key_name='pblKey',
                                             user_data=ec2.UserData.custom(user_data),
                                             user_data_causes_replacement=True,
                                             security_group=sg
                                             )
