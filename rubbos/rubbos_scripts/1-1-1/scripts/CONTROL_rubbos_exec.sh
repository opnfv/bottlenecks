#!/bin/bash

set -x

cd /bottlenecks/rubbos/rubbos_scripts/1-1-1
source set_bottlenecks_rubbos_env.sh
export scp_options='-o StrictHostKeyChecking=no -o BatchMode=yes'

scp $WORK_HOME/monitors_files/oprofile_start.sh $MYSQL1_HOST:/tmp/

echo "Starting RUBBoS"

ssh $RUBBOS_RESULTS_HOST "
  mkdir -p $RUBBOS_RESULTS_DIR_BASE
"
ssh $BENCHMARK_HOST "
  mkdir -p $TMP_RESULTS_DIR_BASE/$RUBBOS_RESULTS_DIR_NAME
"

#TODO use for loop to genrate rubbos.properties file 200 ~ 1700
for i in "rubbos.properties_200"
do

  ssh $BENCHMARK_HOST "
    source /bottlenecks/rubbos/rubbos_scripts/1-1-1/set_bottlenecks_rubbos_env.sh
    rm -f $RUBBOS_HOME/Client/rubbos.properties
  "
  scp $OUTPUT_HOME/rubbos_conf/$i $BENCHMARK_HOST:$RUBBOS_HOME/Client/rubbos.properties

  #echo "Resetting all data"
  #$OUTPUT_HOME/scripts/reset_all.sh

  # Browsing Only
  echo "Start Browsing Only with $i"
  echo "Removing previous logs..."
  ssh $HTTPD_HOST "rm -f $HTTPD_HOME/logs/*log"
  ssh $TOMCAT1_HOST "rm -f $CATALINA_HOME/logs/*"
  ssh $MYSQL1_HOST "rm -f $MYSQL_HOME/run/*.log $RUBBOS_APP/mysql_mon-*"

  $OUTPUT_HOME/scripts/start_all.sh
  sleep 15

  for host in $BENCHMARK_HOST $CLIENT1_HOST $CLIENT2_HOST $CLIENT3_HOST \
              $CLIENT4_HOST $HTTPD_HOST $TOMCAT1_HOST $MYSQL1_HOST
  do
    ssh $host "rm -f $RUBBOS_APP/sar-* $RUBBOS_APP/ps-* $RUBBOS_APP/iostat-*"
  done
  ssh $MYSQL1_HOST "rm -f /tmp/*.log"
  ssh $MYSQL1_HOST chmod 777 /tmp/oprofile_start.sh
  #ssh $MYSQL1_HOST "
  #  cd /tmp
  #  ./oprofile_start.sh
  #" &

  ssh $BENCHMARK_HOST "
    source /bottlenecks/rubbos/rubbos_scripts/1-1-1/set_bottlenecks_rubbos_env.sh

    cd $RUBBOS_HOME/bench
    \rm -r 20*

    # Execute benchmark
    echo "execute benchmark"
    ./rubbos-servletsBO.sh

    # Collect results
    echo "The benchmark has finished. Now, collecting results..."
    cd 20*
    for host in $BENCHMARK_HOST $CLIENT1_HOST $CLIENT2_HOST $CLIENT3_HOST \
                $CLIENT4_HOST $HTTPD_HOST $TOMCAT1_HOST $MYSQL1_HOST
    do
      for f in sar-* ps-* iostat-* mysql_mon-* postgres_lock-*
      do
        scp $scp_options \$host:$RUBBOS_APP/\$f ./
      done
    done
    cd ..
    mv 20* $TMP_RESULTS_DIR_BASE/$RUBBOS_RESULTS_DIR_NAME/
  "

  # TODO debug the rest of sciripts
  exit 0
  #$OUTPUT_HOME/scripts/stop_all.sh
  $OUTPUT_HOME/scripts/kill_all.sh
  sleep 15
  echo "End Browsing Only with $i"

  # Read/Write

done

echo "Processing the results..."
ssh $BENCHMARK_HOST "
  cd $TMP_RESULTS_DIR_BASE
  cd $RUBBOS_RESULTS_DIR_NAME
  scp $RUBBOS_RESULTS_HOST:$RUBBOS_RESULTS_DIR_BASE/calc-sarSummary.prl ../
  ../calc-sarSummary.prl

  rm -f 20*/*.bin

  cd ../
  tar zcvf $RUBBOS_RESULTS_DIR_NAME.tgz $RUBBOS_RESULTS_DIR_NAME
  scp $RUBBOS_RESULTS_DIR_NAME.tgz $RUBBOS_RESULTS_HOST:$RUBBOS_RESULTS_DIR_BASE/
"

echo "Finish RUBBoS"

set +x

