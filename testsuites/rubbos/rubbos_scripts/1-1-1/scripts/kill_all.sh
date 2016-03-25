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

$OUTPUT_HOME/scripts/stop_all.sh

for i in "$BENCHMARK_HOST" "$CLIENT1_HOST" "$CLIENT2_HOST" "$CLIENT3_HOST" "$CLIENT4_HOST" "$HTTPD_HOST" "$TOMCAT1_HOST" "$MYSQL1_HOST"
do
  ssh $i "
    kill -9 -1
    "
done

