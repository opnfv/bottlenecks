#!/bin/bash

cd /bottlenecks/rubbos/rubbos_scripts/1-1-1
source set_bottlenecks_rubbos_env.sh

echo "STOPPING APACHE on $HOSTNAME"

$HTTPD_HOME/bin/apachectl -f $HTTPD_HOME/conf/httpd.conf -k stop

echo "APACHE IS STOPPED on $HOSTNAME"

 
