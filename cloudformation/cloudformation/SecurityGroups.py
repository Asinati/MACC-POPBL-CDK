import aws_cdk as cdk
from aws_cdk import (
    aws_ec2 as ec2
)
from constructs import Construct

BASTION_IP = '10.0.0.11/32'
HAPROXY_IP = '10.0.0.21/32'
FLASK_CONSUL_IP = '10.0.2.11/32'
CLIENT1_IP = '10.0.2.12/32'
CLIENT2_IP = '10.0.2.13/32'
RABBITMQ_IP = '10.0.2.21/32'

class SecurityGroups(cdk.Stack):

    def __init__(self, scope: Construct, id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # --------------------- Bastion ---------------------
        self.bastionSG = ec2.SecurityGroup(self, 'Bastion_SG',
                                           security_group_name='Bastion_SG',
                                           vpc=vpc,
                                           description='Bastion Security Group',
                                           allow_all_outbound=True
                                           )
        # Inbound rules for Bastion_SG
        self.bastionSG.add_ingress_rule(ec2.Peer.any_ipv4(),
                                        ec2.Port.tcp(22),
                                        'Allow SSH access from anywhere')

        # --------------------- HAProxy ---------------------
        self.haproxySG = ec2.SecurityGroup(self, 'HAProxy_SG',
                                           security_group_name='HAProxy_SG',
                                           vpc=vpc,
                                           description='HAProxy Security Group',
                                           allow_all_outbound=True
                                           )

        # Inbound rules for HAProxy_SG
        self.haproxySG.add_ingress_rule(ec2.Peer.ipv4(BASTION_IP),
                                        ec2.Port.tcp(22),
                                        'SSH')
        self.haproxySG.add_ingress_rule(ec2.Peer.any_ipv4(),
                                        ec2.Port.tcp(80),
                                        'HTTP')
        self.haproxySG.add_ingress_rule(ec2.Peer.any_ipv4(),
                                        ec2.Port.tcp(443),
                                        'HTTPS')
        self.haproxySG.add_ingress_rule(ec2.Peer.any_ipv4(),
                                        ec2.Port.tcp(34443),
                                        'HAProxy Management')

        # --------------------- RabbitMQ ---------------------
        self.rabbitmqSG = ec2.SecurityGroup(self, 'RabbitMQ_SG',
                                            security_group_name='RabbitMQ_SG',
                                            vpc=vpc,
                                            description='RabbitMQ Security Group',
                                            allow_all_outbound=True
                                            )

        # Inbound rules for RabbitMQ_SG
        self.rabbitmqSG.add_ingress_rule(ec2.Peer.ipv4(BASTION_IP),
                                         ec2.Port.tcp(22),
                                         'SSH')
        self.rabbitmqSG.add_ingress_rule(ec2.Peer.ipv4(FLASK_CONSUL_IP),
                                         ec2.Port.tcp(5671),
                                         'RabbitMQ')
        self.rabbitmqSG.add_ingress_rule(ec2.Peer.ipv4(CLIENT1_IP),
                                         ec2.Port.tcp(5671),
                                         'RabbitMQ')
        self.rabbitmqSG.add_ingress_rule(ec2.Peer.ipv4(CLIENT2_IP),
                                         ec2.Port.tcp(5671),
                                         'RabbitMQ')
        self.rabbitmqSG.add_ingress_rule(ec2.Peer.ipv4(HAPROXY_IP),
                                         ec2.Port.tcp(15671),
                                         'RabbitMQ Management')

        # --------------------- Flask / Consul ---------------------
        self.flaskconsulSG = ec2.SecurityGroup(self, 'FlaskConsul_SG',
                                               security_group_name='FlaskConsul_SG',
                                               vpc=vpc,
                                               description='Flask and Consul Security Group',
                                               allow_all_outbound=True
                                               )

        # Inbound rules for Flask_Consul_SG
        self.flaskconsulSG.add_ingress_rule(ec2.Peer.ipv4(BASTION_IP),
                                            ec2.Port.tcp(22),
                                            'SSH')
        self.flaskconsulSG.add_ingress_rule(ec2.Peer.any_ipv4(),
                                            ec2.Port.tcp(80),
                                            'HTTP')
        self.flaskconsulSG.add_ingress_rule(ec2.Peer.any_ipv4(),
                                            ec2.Port.tcp(443),
                                            'HTTPS')
        self.flaskconsulSG.add_ingress_rule(ec2.Peer.ipv4(RABBITMQ_IP),
                                            ec2.Port.tcp(5671),
                                            'RabbitMQ')
        self.flaskconsulSG.add_ingress_rule(ec2.Peer.any_ipv4(),
                                            ec2.Port.tcp_range(8002,8010),
                                            'Flask container ports')
        self.flaskconsulSG.add_ingress_rule(ec2.Peer.any_ipv4(),
                                             ec2.Port.tcp_range(8300,8301),
                                             'Consul')
        self.flaskconsulSG.add_ingress_rule(ec2.Peer.any_ipv4(),
                                             ec2.Port.tcp_range(8500,8501),
                                             'Consul')
        self.flaskconsulSG.add_ingress_rule(ec2.Peer.any_ipv4(),
                                             ec2.Port.tcp(8600),
                                             'Consul')
        self.flaskconsulSG.add_ingress_rule(ec2.Peer.any_ipv4(),
                                            ec2.Port.tcp_range(21000, 21255),
                                            'Consul DNS')
        self.flaskconsulSG.add_ingress_rule(ec2.Peer.any_ipv4(),
                                            ec2.Port.udp_range(0, 65535),
                                            'Consul DNS')

        # --------------------- Clients ---------------------
        self.clientsSG = ec2.SecurityGroup(self, 'Clients_SG',
                                               security_group_name='Clients_SG',
                                               vpc=vpc,
                                               description='Clients Security Group',
                                               allow_all_outbound=True
                                               )

        # Inbound rules for Clients_SG
        self.clientsSG.add_ingress_rule(ec2.Peer.ipv4(BASTION_IP),
                                            ec2.Port.tcp(22),
                                            'SSH')
        self.clientsSG.add_ingress_rule(ec2.Peer.any_ipv4(),
                                            ec2.Port.tcp(80),
                                            'HTTP')
        self.clientsSG.add_ingress_rule(ec2.Peer.any_ipv4(),
                                            ec2.Port.tcp(443),
                                            'HTTPS')
        self.clientsSG.add_ingress_rule(ec2.Peer.ipv4(RABBITMQ_IP),
                                            ec2.Port.tcp(5671),
                                            'RabbitMQ')
        self.clientsSG.add_ingress_rule(ec2.Peer.any_ipv4(),
                                            ec2.Port.tcp(8001),
                                            'Flask container ports')
        self.clientsSG.add_ingress_rule(ec2.Peer.any_ipv4(),
                                            ec2.Port.tcp_range(8300, 8301),
                                            'Consul')
        self.clientsSG.add_ingress_rule(ec2.Peer.any_ipv4(),
                                            ec2.Port.tcp_range(8500, 8501),
                                            'Consul')
        self.clientsSG.add_ingress_rule(ec2.Peer.any_ipv4(),
                                            ec2.Port.tcp(8600),
                                            'Consul')
        self.clientsSG.add_ingress_rule(ec2.Peer.any_ipv4(),
                                            ec2.Port.tcp_range(21000, 21255),
                                            'Consul DNS')
        self.clientsSG.add_ingress_rule(ec2.Peer.any_ipv4(),
                                            ec2.Port.udp_range(0, 65535),
                                            'Consul DNS')

        # --------------------- HoneyPot ---------------------
        self.honeypotSG = ec2.SecurityGroup(self, 'HoneyPot_SG',
                                           security_group_name='HoneyPot_SG',
                                           vpc=vpc,
                                           description='HoneyPot Security Group',
                                           allow_all_outbound=True
                                           )

        # Inbound rules for HoneyPot_SG
        self.honeypotSG.add_ingress_rule(ec2.Peer.any_ipv4(),
                                            ec2.Port.tcp(64295),
                                            'SSH')
        self.honeypotSG.add_ingress_rule(ec2.Peer.any_ipv4(),
                                            ec2.Port.tcp(64297),
                                            'HTTP')
        self.honeypotSG.add_ingress_rule(ec2.Peer.any_ipv4(),
                                            ec2.Port.tcp_range(1, 64000),
                                            'Everything else')

        # --------------------- Order HoneyPot ---------------------
        self.orderhoneypotSG = ec2.SecurityGroup(self, 'OrderHoneyPot_SG',
                                            security_group_name='OrderHoneyPot_SG',
                                            vpc=vpc,
                                            description='Order HoneyPot Security Group',
                                            allow_all_outbound=True
                                            )

        # Inbound rules for HoneyPot_SG
        self.orderhoneypotSG.add_ingress_rule(ec2.Peer.any_ipv4(),
                                         ec2.Port.tcp(22),
                                         'SSH')
        self.orderhoneypotSG.add_ingress_rule(ec2.Peer.any_ipv4(),
                                         ec2.Port.tcp(13003),
                                         'Allow curl')
        self.orderhoneypotSG.add_ingress_rule(ec2.Peer.any_ipv4(),
                                         ec2.Port.tcp_range(0,13002),
                                         'Everything else')
        self.orderhoneypotSG.add_ingress_rule(ec2.Peer.any_ipv4(),
                                         ec2.Port.tcp_range(13004, 64000),
                                         'Everything else')

        # --------------------- ELK Stack / Machine Learning ---------------------
        self.elkmlSG = ec2.SecurityGroup(self, 'ELKStackML_SG',
                                            security_group_name='ELKStackML_SG',
                                            vpc=vpc,
                                            description='ELKStack and Machine Learning Security Group',
                                            allow_all_outbound=True
                                            )

        # Inbound rules for ELKStackML_SG
        self.elkmlSG.add_ingress_rule(ec2.Peer.ipv4(BASTION_IP),
                                         ec2.Port.tcp(22),
                                         'SSH')
        self.elkmlSG.add_ingress_rule(ec2.Peer.ipv4(BASTION_IP),
                                        ec2.Port.tcp(80),
                                        'HTTP')
        self.elkmlSG.add_ingress_rule(ec2.Peer.ipv4(BASTION_IP),
                                        ec2.Port.tcp(443),
                                        'HTTPS')
        self.elkmlSG.add_ingress_rule(ec2.Peer.any_ipv4(),
                                         ec2.Port.tcp(5601),
                                         'Kibana')
        self.elkmlSG.add_ingress_rule(ec2.Peer.any_ipv4(),
                                         ec2.Port.tcp(9200),
                                         'ElasticSearch')

