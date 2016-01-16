#!/bin/bash
##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

###############################################################################
#
# This script runs first the RUBBoS browsing mix, then the read/write mix 
# for each rubbos.properties_XX specified where XX is the number of emulated
# clients. Note that the rubbos.properties_XX files must be configured
# with the corresponding number of clients.
# In particular set the following variables in rubis.properties_XX:
# httpd_use_version = Servlets
# workload_number_of_clients_per_node = XX/number of client machines
# workload_transition_table = yourPath/RUBBoS/workload/transitions.txt 
#
# This script should be run from the RUBBoS/bench directory on the local 
# client machine. 
# Results will be generated in the RUBBoS/bench directory.
#
################################################################################

#setenv SERVLETDIR $RUBBOS_HOME/Servlets

# Go back to RUBBoS root directory
cd ..

# Read/write mix

cp --fi ./workload/user_default_transitions.txt ./workload/user_transitions.txt
cp --fi ./workload/author_default_transitions.txt ./workload/author_transitions.txt

scp ./workload/user_default_transitions.txt ${CLIENT1_HOST}:${RUBBOS_HOME}/workload/user_transitions.txt
scp ./workload/author_default_transitions.txt ${CLIENT1_HOST}:${RUBBOS_HOME}/workload/author_transitions.txt

scp ./workload/user_default_transitions.txt ${CLIENT2_HOST}:${RUBBOS_HOME}/workload/user_transitions.txt
scp ./workload/author_default_transitions.txt ${CLIENT2_HOST}:${RUBBOS_HOME}/workload/author_transitions.txt

scp ./workload/user_default_transitions.txt ${CLIENT3_HOST}:${RUBBOS_HOME}/workload/user_transitions.txt
scp ./workload/author_default_transitions.txt ${CLIENT3_HOST}:${RUBBOS_HOME}/workload/author_transitions.txt

scp ./workload/user_default_transitions.txt ${CLIENT4_HOST}:${RUBBOS_HOME}/workload/user_transitions.txt
scp ./workload/author_default_transitions.txt ${CLIENT4_HOST}:${RUBBOS_HOME}/workload/author_transitions.txt

scp Client/rubbos.properties ${CLIENT1_HOST}:${RUBBOS_HOME}/Client/rubbos.properties
scp Client/rubbos.properties ${CLIENT2_HOST}:${RUBBOS_HOME}/Client/rubbos.properties
scp Client/rubbos.properties ${CLIENT3_HOST}:${RUBBOS_HOME}/Client/rubbos.properties
scp Client/rubbos.properties ${CLIENT4_HOST}:${RUBBOS_HOME}/Client/rubbos.properties


bench/flush_cache 490000
ssh $HTTPD_HOST "$RUBBOS_HOME/bench/flush_cache 880000"       # web server
ssh $MYSQL1_HOST "$RUBBOS_HOME/bench/flush_cache 880000"       # database server
ssh $TOMCAT1_HOST "$RUBBOS_HOME/bench/flush_cache 780000"       # servlet server
ssh $CLIENT1_HOST "$RUBBOS_HOME/bench/flush_cache 490000"       # remote client
ssh $CLIENT2_HOST "$RUBBOS_HOME/bench/flush_cache 490000"       # remote client
ssh $CLIENT3_HOST "$RUBBOS_HOME/bench/flush_cache 490000"       # remote client
ssh $CLIENT4_HOST "$RUBBOS_HOME/bench/flush_cache 490000"       # remote client

RAMPUP=480000
MI=720000
current_seconds=`date +%s`
start_seconds=`echo \( $RAMPUP / 1000 \) + $current_seconds - 60 | bc`
SMI=`date -d "1970-01-01 $start_seconds secs UTC" +%Y%m%d%H%M%S`
end_seconds=`echo \( $RAMPUP / 1000 + $MI / 1000 + 30 \) + $current_seconds | bc`
EMI=`date -d "1970-01-01 $end_seconds secs UTC" +%Y%m%d%H%M%S`
ssh $BENCHMARK_HOST "sudo nice -n -1 $RUBBOS_APP/cpu_mem.sh $SMI $EMI" &
ssh $CLIENT1_HOST "sudo nice -n -1 $RUBBOS_APP/cpu_mem.sh $SMI $EMI" &
ssh $CLIENT2_HOST "sudo nice -n -1 $RUBBOS_APP/cpu_mem.sh $SMI $EMI" &
ssh $CLIENT3_HOST "sudo nice -n -1 $RUBBOS_APP/cpu_mem.sh $SMI $EMI" &
ssh $CLIENT4_HOST "sudo nice -n -1 $RUBBOS_APP/cpu_mem.sh $SMI $EMI" &
ssh $HTTPD_HOST "sudo nice -n -1 $RUBBOS_APP/cpu_mem.sh $SMI $EMI" &
ssh $TOMCAT1_HOST "sudo nice -n -1 $RUBBOS_APP/cpu_mem.sh $SMI $EMI" &
ssh $MYSQL1_HOST "sudo nice -n -1 $RUBBOS_APP/cpu_mem.sh $SMI $EMI" &


make emulator

