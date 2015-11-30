#!/bin/bash

cd /bottlenecks/rubbos/rubbos_scripts/1-1-1
source set_bottlenecks_rubbos_env.sh

echo "INSTALLING TOMCAT on $HOSTNAME"

mkdir -p $BOTTLENECKS_TOP
chmod 755 $BOTTLENECKS_TOP
mkdir -p $RUBBOS_TOP
chmod 755 $RUBBOS_TOP
mkdir -p $RUBBOS_APP
chmod 755 $RUBBOS_APP

tar xzf $SOFTWARE_HOME/$TOMCAT_TARBALL --directory=$RUBBOS_APP
tar xzf $SOFTWARE_HOME/$JAVA_TARBALL   --directory=$RUBBOS_APP
tar xzf $SOFTWARE_HOME/$J2EE_TARBALL   --directory=$RUBBOS_APP
tar xzf $SOFTWARE_HOME/$ANT_TARBALL    --directory=$RUBBOS_APP

echo "DONE INSTALLING TOMCAT on $HOSTNAME"
