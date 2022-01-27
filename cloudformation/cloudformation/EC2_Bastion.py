import aws_cdk as cdk
from aws_cdk import (
    aws_ec2 as ec2
)
from constructs import Construct

with open("C:\\Users\\Asier\\Documents\\MU\\AWS\\Cloudformation\\cloudformation\\user_data\\Bastion_userData.sh") as sh:
    user_data = sh.read()

class EC2_Bastion(cdk.Stack):

    def __init__(self, scope: Construct, id: str, vpc: ec2.Vpc, sg: ec2.SecurityGroup, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.bastionEC2 = ec2.Instance(self, 'Bastion',
                                        vpc=vpc,
                                        private_ip_address='10.0.0.11',
                                        vpc_subnets=ec2.SubnetSelection(
                                            subnet_group_name='PublicSubnet'
                                        ),
                                        instance_type=ec2.InstanceType('t2.micro'),
                                        machine_image=ec2.AmazonLinuxImage(
                                            edition=ec2.AmazonLinuxEdition.STANDARD,
                                            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
                                            virtualization=ec2.AmazonLinuxVirt.HVM,
                                            storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
                                        ),
                                        key_name='pblKey',
                                        user_data=ec2.UserData.custom(user_data),
                                        user_data_causes_replacement=True,
                                        security_group=sg
                                        )

        elastic_ip = ec2.CfnEIP(self, "Bastion EIP",
                                domain="vpc",
                                instance_id=self.bastionEC2.instance_id
                                )