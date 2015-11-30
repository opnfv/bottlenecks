#!/bin/bash

cd /bottlenecks/rubbos/rubbos_scripts/1-1-1
source set_bottlenecks_rubbos_env.sh

echo "STARTING TOMCAT on $HOSTNAME"

cd $CATALINA_HOME/bin
./startup.sh

echo "TOMCAT IS RUNNING on $HOSTNAME" 
