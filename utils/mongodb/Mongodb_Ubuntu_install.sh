#!/bin/bash
#from OPNFV project:bottlenecks
#hongbo tian(hongbo.tianhongbo@huawei.com)

#import the public ke used by the package managment system
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10

#create a list for MangoDB
#for Ubuntu 12.04
#echo "deb http://repo.mongodb.org/apt/ubuntu precise/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list

#for Ubuntu14.04
echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list

#Reload local pachage database
sudo apt-get update

#install the MongoDB for the latest stable version
sudo apt-get install -y mongodb-org

#start MongoDB
sudo service mongod start

#try test
# mongo
