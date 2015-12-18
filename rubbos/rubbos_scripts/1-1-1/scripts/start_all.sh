#!/bin/bash

cd /bottlenecks/rubbos/rubbos_scripts/1-1-1
source set_bottlenecks_rubbos_env.sh

ssh $MYSQL1_HOST  /tmp/MYSQL1_ignition.sh
sleep 10

ssh $TOMCAT1_HOST  /tmp/TOMCAT1_ignition.sh 
sleep 10

ssh $HTTPD_HOST  /tmp/HTTPD_ignition.sh 
sleep 5
