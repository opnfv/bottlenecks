#!/bin/bash
##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

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
