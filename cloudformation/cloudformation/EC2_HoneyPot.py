import aws_cdk as cdk
from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam
)
from constructs import Construct

class EC2_HoneyPot(cdk.Stack):

    def __init__(self, scope: Construct, id: str, vpc: ec2.Vpc, sg: ec2.SecurityGroup, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.honeypotEC2 = ec2.Instance(self, 'HoneyPot',
                                        vpc=vpc,
                                        private_ip_address='10.0.1.11',
                                        vpc_subnets=ec2.SubnetSelection(
                                            subnet_group_name='HoneyPotSubnet'
                                        ),
                                        instance_type=ec2.InstanceType('t3.2xlarge'),
                                        machine_image=ec2.GenericLinuxImage({
                                            "us-east-1": "ami-0bfcae1869e77025c"
                                        }),
                                        key_name='pblKey',
                                        security_group=sg
                                        )