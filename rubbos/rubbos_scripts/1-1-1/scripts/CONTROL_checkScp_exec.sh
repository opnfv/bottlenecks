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

# Check scp to all servers
echo "*** checking scp to all servers *********************************"

ssh -o StrictHostKeyChecking=no -o BatchMode=yes $CONTROL_HOST "hostname"
ssh -o StrictHostKeyChecking=no -o BatchMode=yes $BENCHMARK_HOST "hostname"
ssh -o StrictHostKeyChecking=no -o BatchMode=yes $CLIENT1_HOST "hostname"
ssh -o StrictHostKeyChecking=no -o BatchMode=yes $CLIENT2_HOST "hostname"
ssh -o StrictHostKeyChecking=no -o BatchMode=yes $CLIENT3_HOST "hostname"
ssh -o StrictHostKeyChecking=no -o BatchMode=yes $CLIENT4_HOST "hostname"
ssh -o StrictHostKeyChecking=no -o BatchMode=yes $HTTPD_HOST "hostname"
ssh -o StrictHostKeyChecking=no -o BatchMode=yes $TOMCAT1_HOST "hostname"
ssh -o StrictHostKeyChecking=no -o BatchMode=yes $MYSQL1_HOST "hostname"

#ssh -o StrictHostKeyChecking=no -o BatchMode=yes bonn.cc.gt.atl.ga.us "hostname"
ssh -o StrictHostKeyChecking=no -o BatchMode=yes localhost "hostname"
