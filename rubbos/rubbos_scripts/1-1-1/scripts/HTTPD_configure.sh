#!/bin/bash

cd /bottlenecks/rubbos/rubbos_scripts/1-1-1
source set_bottlenecks_rubbos_env.sh

echo "CONFIGURING APACHE on $HOSTNAME"

cp $OUTPUT_HOME/apache_conf/httpd.conf $HTTPD_HOME/conf/
cp $OUTPUT_HOME/apache_conf/workers.properties $HTTPD_HOME/conf/
cp -r $WORK_HOME/apache_files/rubbos_html $HTTPD_HOME/htdocs/rubbos

apache > /dev/null 2>&1

echo "APACHE CONFIGURED SUCCESSFULLY on $HOSTNAME"


 
