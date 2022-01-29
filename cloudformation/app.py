#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cloudformation.VPC import VPC
from cloudformation.SecurityGroups import SecurityGroups
from cloudformation.SecretManager import SecretManager
from cloudformation.EC2_Bastion import EC2_Bastion
from cloudformation.EC2_HAProxy import EC2_HAProxy
from cloudformation.EC2_RabbitMQ import EC2_RabbitMQ
from cloudformation.EC2_Flask_Consul import EC2_Flask_Consul
from cloudformation.EC2_Client1 import EC2_Client1
from cloudformation.EC2_Client2 import EC2_Client2
from cloudformation.EC2_HoneyPot import EC2_HoneyPot
from cloudformation.EC2_OrderHoneyPot import EC2_OrderHoneyPot
from cloudformation.EC2_ELKStack_ML import EC2_ELKStack_ML


app = cdk.App()
vpc = VPC(app, "vpc")
securityGroup = SecurityGroups(app, 'securityGroup', vpc=vpc.vpc)
secretManager = SecretManager(app, 'secretManager')
ec2_Bastion = EC2_Bastion(app, 'bastion', vpc=vpc.vpc, sg=securityGroup.bastionSG)
ec2_HAProxy = EC2_HAProxy(app, 'haproxy', vpc=vpc.vpc, sg=securityGroup.haproxySG)
ec2_RabbitMQ = EC2_RabbitMQ(app, 'rabbitmq', vpc=vpc.vpc, sg=securityGroup.rabbitmqSG)
ec2_FlaskConsul = EC2_Flask_Consul(app, 'flaskconsul', vpc=vpc.vpc, sg=securityGroup.flaskconsulSG, role=secretManager.role)
ec2_Client1 = EC2_Client1(app, 'client1', vpc=vpc.vpc, sg=securityGroup.clientsSG, role=secretManager.role)
ec2_Client2 = EC2_Client2(app, 'client2', vpc=vpc.vpc, sg=securityGroup.clientsSG, role=secretManager.role)
ec2_HoneyPot = EC2_HoneyPot(app, 'honeypot', vpc=vpc.vpc, sg=securityGroup.honeypotSG)
ec2_OrderHoneyPot = EC2_OrderHoneyPot(app, 'orderhoneypot', vpc=vpc.vpc, sg=securityGroup.orderhoneypotSG)
ec2_ELKStackML = EC2_ELKStack_ML(app, 'elkstackml', vpc=vpc.vpc, sg=securityGroup.elkmlSG)

app.synth()
