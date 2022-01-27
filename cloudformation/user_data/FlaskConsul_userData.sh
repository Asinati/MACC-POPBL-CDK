#!/bin/bash
cd home/ec2-user/
sudo yum update -y
sudo yum install git -y
git clone -b flask-only https://github.com/andercarrera/MACC-monolithic-to-master.git

sudo yum install docker -y
sudo systemctl enable docker
sudo service docker start
sudo usermod -a -G docker ec2-user

sudo curl -L https://github.com/docker/compose/releases/download/1.21.0/docker-compose-`uname -s`-`uname -m` | sudo tee /usr/local/bin/docker-compose > /dev/null
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

sudo systemctl daemon-reload

cd MACC-monolithic-to-master/
./start-dev.sh

cd ..
git clone https://github.com/andercarrera/MACC-popbl-beats.git
cd MACC-popbl-beats
docker-compose up -d

