#!/bin/bash

##############################################################################
# Copyright (c) 2015 Huawei
# hongbo.tianhongbo@huawei.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

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
