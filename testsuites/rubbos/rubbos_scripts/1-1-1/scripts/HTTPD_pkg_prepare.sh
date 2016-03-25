#!/bin/bash
##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

. ../set_bottlenecks_rubbos_env.sh

scp_options="-o StrictHostKeyChecking=no -o BatchMode=yes"

# Packages for HTTPD install
if true; then
ssh $HTTPD_HOST "mkdir -p /bottlenecks/rubbos/rubbos_scripts/1-1-1"
scp $scp_options ../set_bottlenecks_rubbos_env.sh $HTTPD_HOST:/bottlenecks/rubbos/rubbos_scripts/1-1-1

ssh $HTTPD_HOST "mkdir -p $SOFTWARE_HOME"
scp $scp_options $SOFTWARE_HOME/$HTTPD_TARBALL $HTTPD_HOST:$SOFTWARE_HOME/$HTTPD_TARBALL
scp $scp_options $SOFTWARE_HOME/$MOD_JK_TARBALL $HTTPD_HOST:$SOFTWARE_HOME/$MOD_JK_TARBALL
scp $scp_options $SOFTWARE_HOME/$JAVA_TARBALL $HTTPD_HOST:$SOFTWARE_HOME/$JAVA_TARBALL

fi

# Packages for HTTPD rubbos install
if true; then
scp $scp_options $SOFTWARE_HOME/$RUBBOS_TARBALL $HTTPD_HOST:$SOFTWARE_HOME/$RUBBOS_TARBALL
scp $scp_options $SOFTWARE_HOME/flush_cache $HTTPD_HOST:$SOFTWARE_HOME/flush_cache
scp $scp_options $SOFTWARE_HOME/$SYSSTAT_TARBALL $HTTPD_HOST:$SOFTWARE_HOME/$SYSSTAT_TARBALL
ssh $HTTPD_HOST "mkdir -p $OUTPUT_HOME/rubbos_conf"
scp $scp_options $OUTPUT_HOME/rubbos_conf/cpu_mem.sh $HTTPD_HOST:$OUTPUT_HOME/rubbos_conf/cpu_mem.sh
fi

# Packages for HTTPD configure
if true; then
ssh $HTTPD_HOST "mkdir -p $OUTPUT_HOME/apache_conf"
scp $scp_options $OUTPUT_HOME/apache_conf/httpd.conf $HTTPD_HOST:$OUTPUT_HOME/apache_conf/httpd.conf

sed -e "s/REPLACE_TOMCAT1_HOST/$TOMCAT1_HOST/g" \
    $OUTPUT_HOME/apache_conf/workers.properties_template \
    > $OUTPUT_HOME/apache_conf/workers.properties
scp $scp_options $OUTPUT_HOME/apache_conf/workers.properties $HTTPD_HOST:$OUTPUT_HOME/apache_conf/workers.properties
rm -rf $OUTPUT_HOME/apache_conf/workers.properties

ssh $HTTPD_HOST "mkdir -p $WORK_HOME/apache_files"
scp $scp_options -r $WORK_HOME/apache_files/rubbos_html $HTTPD_HOST:$WORK_HOME/apache_files/rubbos_html
fi

