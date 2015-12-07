#!/bin/bash

cd /bottlenecks/rubbos/rubbos_scripts/1-1-1
source set_bottlenecks_rubbos_env.sh

#ssh_options=""

ssh root@$TOMCAT1_HOST service tomcat status
ssh root@$HTTPD_HOST service apache2 status
ssh root@$MYSQL1_HOST service mysql status

