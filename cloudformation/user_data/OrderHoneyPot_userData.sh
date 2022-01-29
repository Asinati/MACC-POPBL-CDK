#!/bin/bash
cd home/ec2-user/
sudo yum update -y

cd MACC-monolithic-to-master-ELK
docker-compose up -d

cd ..
sudo service filebeat start

./FakeOrder/flask_app/order/start-dev.sh

