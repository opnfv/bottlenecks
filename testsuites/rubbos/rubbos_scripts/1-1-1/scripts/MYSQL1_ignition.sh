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

echo "STARTING MYSQL on $HOSTNAME $(date)"

cd $MYSQL_HOME
bin/mysqld_safe&
sleep 10
/etc/init.d/mysql.server status


echo "MYSQL IS RUNNING on $HOSTNAME $(date)"
