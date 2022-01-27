cdk deploy vpc --require-approval never
cdk deploy securityGroup --require-approval never
cdk deploy secretManager --require-approval never
cdk deploy bastion --require-approval never
cdk deploy elkstackml --require-approval never
cdk deploy rabbitmq --require-approval never
cdk deploy haproxy --require-approval never
cdk deploy flaskconsul --require-approval never
cdk deploy client1 --require-approval never
cdk deploy client2 --require-approval never
cdk deploy honeypot --require-approval never

# cd..
# cd..
# ssh -v -N -L 80:10.0.2.11:8501 -i .\pblKey.pem ec2-user@ #IPPúblicaBastion
# ssh -v -N -L 8000:10.0.2.21:15671 -i .\pblKey.pem ec2-user@ #IPPúblicaBastion
# ssh -v -N -L 8080:10.0.2.31:5601 -i .\pblKey.pem ec2-user@ #IPPúblicaBastion

cdk deploy "*" --require-approval never