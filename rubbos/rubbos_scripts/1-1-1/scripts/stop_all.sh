#!/bin/bash

cd /bottlenecks/rubbos/rubbos_scripts/1-1-1
source set_bottlenecks_rubbos_env.sh

ssh $HTTPD_HOST  /tmp/HTTPD_stop.sh

ssh $TOMCAT1_HOST  /tmp/TOMCAT1_stop.sh

ssh $MYSQL1_HOST  /tmp/MYSQL1_stop.sh
