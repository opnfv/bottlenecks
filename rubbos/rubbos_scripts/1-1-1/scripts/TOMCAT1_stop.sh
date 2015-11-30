#!/bin/bash

cd /bottlenecks/rubbos/rubbos_scripts/1-1-1
source set_bottlenecks_rubbos_env.sh

echo "STOPPING TOMCAT on $HOSTNAME"

cd $CATALINA_HOME/bin
./shutdown.sh

echo "TOMCAT IS STOPPED on $HOSTNAME"

 
