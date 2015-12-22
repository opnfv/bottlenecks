#!/bin/bash

. ../set_bottlenecks_rubbos_env.sh

scp_options="-o StrictHostKeyChecking=no -o BatchMode=yes"

# Packages for TOMCAT1 install
if true; then
ssh $TOMCAT1_HOST "mkdir -p /bottlenecks/rubbos/rubbos_scripts/1-1-1"
scp $scp_options ../set_bottlenecks_rubbos_env.sh $TOMCAT1_HOST:/bottlenecks/rubbos/rubbos_scripts/1-1-1

ssh $TOMCAT1_HOST "mkdir -p $SOFTWARE_HOME"

for i in $TOMCAT_TARBALL $JAVA_TARBALL $J2EE_TARBALL $ANT_TARBALL
do
    scp $scp_options $SOFTWARE_HOME/$i $TOMCAT1_HOST:$SOFTWARE_HOME/$i
done

fi

# Packages for TOMCAT1 rubbos install
if true; then
scp $scp_options $SOFTWARE_HOME/$RUBBOS_TARBALL $TOMCAT1_HOST:$SOFTWARE_HOME/$RUBBOS_TARBALL
scp $scp_options $SOFTWARE_HOME/flush_cache $TOMCAT1_HOST:$SOFTWARE_HOME/flush_cache
scp $scp_options $SOFTWARE_HOME/$SYSSTAT_TARBALL $TOMCAT1_HOST:$SOFTWARE_HOME/$SYSSTAT_TARBALL
ssh $TOMCAT1_HOST "mkdir -p $OUTPUT_HOME/rubbos_conf"
scp $scp_options $OUTPUT_HOME/rubbos_conf/cpu_mem.sh $TOMCAT1_HOST:$OUTPUT_HOME/rubbos_conf/cpu_mem.sh
fi

# Packages for TOMCAT1 configure
if true; then
ssh $TOMCAT1_HOST "mkdir -p $OUTPUT_HOME/tomcat_conf"
scp $scp_options $OUTPUT_HOME/tomcat_conf/server.xml $TOMCAT1_HOST:$OUTPUT_HOME/tomcat_conf/server.xml
fi

# Packages for TOMCAT1 rubbosSL configure
if true; then
ssh $TOMCAT1_HOST "mkdir -p $OUTPUT_HOME/rubbos_conf"
sed -e "s#REPLACE_MYSQL1_HOST#$MYSQL1_HOST#g" \
    $OUTPUT_HOME/rubbos_conf/mysql.properties_template \
    > $OUTPUT_HOME/rubbos_conf/mysql.properties
for i in build.properties mysql.properties build.xml Config.java web.xml
do
    scp $scp_options $OUTPUT_HOME/rubbos_conf/$i $TOMCAT1_HOST:$OUTPUT_HOME/rubbos_conf/$i
done
rm -rf $OUTPUT_HOME/rubbos_conf/mysql.properties

ssh $TOMCAT1_HOST "mkdir -p $WORK_HOME/rubbos_files"
scp $scp_options -r $WORK_HOME/rubbos_files/Servlets $TOMCAT1_HOST:$WORK_HOME/rubbos_files/Servlets
fi

