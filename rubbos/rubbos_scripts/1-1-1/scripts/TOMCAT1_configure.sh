#!/bin/bash

cd /bottlenecks/rubbos/rubbos_scripts/1-1-1
source set_bottlenecks_rubbos_env.sh

echo "CONFIGURING TOMCAT on $HOSTNAME"

cp $OUTPUT_HOME/tomcat_conf/server.xml-$HOSTNAME $CATALINA_HOME/conf/server.xml

echo "DONE CONFIGURING TOMCAT on $HOSTNAME" 
