import json
import aws_cdk as cdk
from aws_cdk import (
    aws_iam as iam
)
from constructs import Construct

with open("C:\\Users\\Asier\\Documents\\MU\\AWS\\Cloudformation\\cloudformation\\policies\\SecretManagerReadOnly.json") as jsonFile:
    policy = json.load(jsonFile)

class SecretManager(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.custom_policy_document = iam.PolicyDocument.from_json(policy)

        self.role = iam.Role(self, id='SecretManagerReadOnly',
                             assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
                             description='Read only access to Secret Manager',
                             inline_policies=[self.custom_policy_document],
                             role_name="secretManagerRole")