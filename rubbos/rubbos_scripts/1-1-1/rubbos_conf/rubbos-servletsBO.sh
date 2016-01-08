#!/bin/bash

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

set -x

# Go back to RUBBoS root directory
cd ..

export scp_options='-o StrictHostKeyChecking=no -o BatchMode=yes'

# Browse only

cp -fin ./workload/browse_only_transitions.txt ./workload/user_transitions.txt
cp -fin ./workload/browse_only_transitions.txt ./workload/author_transitions.txt

for host in ${CLIENT1_HOST} ${CLIENT2_HOST} ${CLIENT3_HOST} ${CLIENT4_HOST}
do
    scp ${scp_options} ./workload/browse_only_transitions.txt ${host}:${RUBBOS_HOME}/workload/user_transitions.txt
    scp ${scp_options} ./workload/browse_only_transitions.txt ${host}:${RUBBOS_HOME}/workload/author_transitions.txt
    scp ${scp_options} Client/rubbos.properties ${host}:${RUBBOS_HOME}/Client/rubbos.properties
done

#bench/flush_cache 490000
#ssh $HTTPD_HOST "$RUBBOS_HOME/bench/flush_cache 880000"       # web server
#ssh $MYSQL1_HOST "$RUBBOS_HOME/bench/flush_cache 880000"       # database server
#ssh $TOMCAT1_HOST "$RUBBOS_HOME/bench/flush_cache 780000"       # servlet server
#ssh $CLIENT1_HOST "$RUBBOS_HOME/bench/flush_cache 490000"       # remote client
#ssh $CLIENT2_HOST "$RUBBOS_HOME/bench/flush_cache 490000"       # remote client
#ssh $CLIENT3_HOST "$RUBBOS_HOME/bench/flush_cache 490000"       # remote client
#ssh $CLIENT4_HOST "$RUBBOS_HOME/bench/flush_cache 490000"       # remote client

RAMPUP=48000
MI=72000
current_seconds=`date +%s`
start_seconds=`echo \( $RAMPUP / 1000 \) + $current_seconds - 60 | bc`
SMI=`date -d "1970-01-01 $start_seconds secs UTC" +%Y%m%d%H%M%S`
end_seconds=`echo \( $RAMPUP / 1000 + $MI / 1000 + 30 \) + $current_seconds | bc`
EMI=`date -d "1970-01-01 $end_seconds secs UTC" +%Y%m%d%H%M%S`

for host in $BENCHMARK_HOST $CLIENT1_HOST $CLIENT2_HOST $CLIENT3_HOST \
            $CLIENT4_HOST $HTTPD_HOST $TOMCAT1_HOST $MYSQL1_HOST
do
    ssh $scp_options $host "sudo nice -n -1 $RUBBOS_APP/cpu_mem.sh $SMI $EMI" &
done

make emulator

set -x

