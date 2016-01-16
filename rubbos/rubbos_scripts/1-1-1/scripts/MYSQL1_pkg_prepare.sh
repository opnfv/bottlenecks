#!/bin/bash
##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

source ../set_bottlenecks_rubbos_env.sh

scp_options="-o StrictHostKeyChecking=no -o BatchMode=yes"

# Packages for MYSQL1 install
echo "MYSQL PREPARE DEPENDANT LIBRARY BEGIN"
if true; then
ssh $MYSQL1_HOST "mkdir -p /bottlenecks/rubbos/rubbos_scripts/1-1-1"
scp $scp_options ../set_bottlenecks_rubbos_env.sh $MYSQL1_HOST:/bottlenecks/rubbos/rubbos_scripts/1-1-1

ssh $MYSQL1_HOST "mkdir -p $SOFTWARE_HOME"
scp $scp_options $SOFTWARE_HOME/$MYSQL_TARBALL $MYSQL1_HOST:$SOFTWARE_HOME/$MYSQL_TARBALL
scp $scp_options $SOFTWARE_HOME/$RUBBOS_DATA_TARBALL $MYSQL1_HOST:$SOFTWARE_HOME/$RUBBOS_DATA_TARBALL

fi
echo "MYSQL PREPARE DEPENDANT LIBRARY END"

# Packages for MYSQL1 rubbos install
if true; then
scp $scp_options $SOFTWARE_HOME/$RUBBOS_TARBALL $MYSQL1_HOST:$SOFTWARE_HOME/$RUBBOS_TARBALL
scp $scp_options $SOFTWARE_HOME/flush_cache $MYSQL1_HOST:$SOFTWARE_HOME/flush_cache
scp $scp_options $SOFTWARE_HOME/$SYSSTAT_TARBALL $MYSQL1_HOST:$SOFTWARE_HOME/$SYSSTAT_TARBALL
ssh $MYSQL1_HOST "mkdir -p $OUTPUT_HOME/rubbos_conf"
scp $scp_options $OUTPUT_HOME/rubbos_conf/cpu_mem.sh $MYSQL1_HOST:$OUTPUT_HOME/rubbos_conf/cpu_mem.sh
fi

# Packages for MYSQL1 configure
if true; then
scp $scp_options $SOFTWARE_HOME/$RUBBOS_DATA_TARBALL $MYSQL1_HOST:/tmp
fi

