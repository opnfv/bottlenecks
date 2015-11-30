#!/bin/bash

cd /bottlenecks/rubbos/rubbos_scripts/1-1-1
source set_bottlenecks_rubbos_env.sh

scp $WORK_HOME/monitors_files/oprofile_start.sh $MYSQL1_HOST:/tmp/

echo "Starting RUBBoS"

ssh $RUBBOS_RESULTS_HOST "
  mkdir -p $RUBBOS_RESULTS_DIR_BASE
"
ssh $BENCHMARK_HOST "
  mkdir -p $TMP_RESULTS_DIR_BASE/$RUBBOS_RESULTS_DIR_NAME
"

#for i in "rubbos.properties_200" "rubbos.properties_300" "rubbos.properties_400" "rubbos.properties_500" "rubbos.properties_600" "rubbos.properties_700" "rubbos.properties_800" "rubbos.properties_900" "rubbos.properties_1000" "rubbos.properties_1100" "rubbos.properties_1200" "rubbos.properties_1300" "rubbos.properties_1400" "rubbos.properties_1500" "rubbos.properties_1600" "rubbos.properties_1700"
for i in "rubbos.properties_200"
do

  ssh $BENCHMARK_HOST "
    source /bottlenecks/rubbos/rubbos_scripts/1-1-1/set_bottlenecks_rubbos_env.sh
    rm -f $RUBBOS_HOME/Client/rubbos.properties
  "
  scp $OUTPUT_HOME/rubbos_conf/$i $BENCHMARK_HOST:$RUBBOS_HOME/Client/rubbos.properties

  echo "Resetting all data"
  $OUTPUT_HOME/scripts/reset_all.sh

  # Browsing Only
  echo "Start Browsing Only with $i"
  echo "Removing previous logs..."
  ssh $HTTPD_HOST "rm -f $HTTPD_HOME/logs/*log"
  ssh $TOMCAT1_HOST "rm -f $CATALINA_HOME/logs/*"
  ssh $MYSQL1_HOST "rm -f $MYSQL_HOME/run/*.log $RUBBOS_APP/mysql_mon-*"

  $OUTPUT_HOME/scripts/start_all.sh
  sleep 15

  ssh $BENCHMARK_HOST "rm -f $RUBBOS_APP/sar-* $RUBBOS_APP/ps-* $RUBBOS_APP/iostat-*"
  ssh $CLIENT1_HOST "rm -f $RUBBOS_APP/sar-* $RUBBOS_APP/ps-* $RUBBOS_APP/iostat-*"
  ssh $CLIENT2_HOST "rm -f $RUBBOS_APP/sar-* $RUBBOS_APP/ps-* $RUBBOS_APP/iostat-*"
  ssh $CLIENT3_HOST "rm -f $RUBBOS_APP/sar-* $RUBBOS_APP/ps-* $RUBBOS_APP/iostat-*"
  ssh $CLIENT4_HOST "rm -f $RUBBOS_APP/sar-* $RUBBOS_APP/ps-* $RUBBOS_APP/iostat-*"
  ssh $HTTPD_HOST "rm -f $RUBBOS_APP/sar-* $RUBBOS_APP/ps-* $RUBBOS_APP/iostat-*"
  ssh $TOMCAT1_HOST "rm -f $RUBBOS_APP/sar-* $RUBBOS_APP/ps-* $RUBBOS_APP/iostat-*"
  ssh $MYSQL1_HOST "rm -f $RUBBOS_APP/sar-* $RUBBOS_APP/ps-* $RUBBOS_APP/iostat-*"
  ssh $MYSQL1_HOST "sudo rm -f /tmp/*.log"
  ssh root@$MYSQL1_HOST chmod 777 /tmp/oprofile_start.sh
  ssh $MYSQL1_HOST "
    cd /tmp
    ./oprofile_start.sh
  " &

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
    scp $BENCHMARK_HOST:$RUBBOS_APP/sar-* ./
    scp $BENCHMARK_HOST:$RUBBOS_APP/ps-* ./
    scp $BENCHMARK_HOST:$RUBBOS_APP/iostat-* ./
    scp $BENCHMARK_HOST:$RUBBOS_APP/mysql_mon-* ./
    scp $BENCHMARK_HOST:$RUBBOS_APP/postgres_lock-* ./
    scp $CLIENT1_HOST:$RUBBOS_APP/sar-* ./
    scp $CLIENT1_HOST:$RUBBOS_APP/ps-* ./
    scp $CLIENT1_HOST:$RUBBOS_APP/iostat-* ./
    scp $CLIENT1_HOST:$RUBBOS_APP/mysql_mon-* ./
    scp $CLIENT1_HOST:$RUBBOS_APP/postgres_lock-* ./
    scp $CLIENT2_HOST:$RUBBOS_APP/sar-* ./
    scp $CLIENT2_HOST:$RUBBOS_APP/ps-* ./
    scp $CLIENT2_HOST:$RUBBOS_APP/iostat-* ./
    scp $CLIENT2_HOST:$RUBBOS_APP/mysql_mon-* ./
    scp $CLIENT2_HOST:$RUBBOS_APP/postgres_lock-* ./
    scp $CLIENT3_HOST:$RUBBOS_APP/sar-* ./
    scp $CLIENT3_HOST:$RUBBOS_APP/ps-* ./
    scp $CLIENT3_HOST:$RUBBOS_APP/iostat-* ./
    scp $CLIENT3_HOST:$RUBBOS_APP/mysql_mon-* ./
    scp $CLIENT3_HOST:$RUBBOS_APP/postgres_lock-* ./
    scp $CLIENT4_HOST:$RUBBOS_APP/sar-* ./
    scp $CLIENT4_HOST:$RUBBOS_APP/ps-* ./
    scp $CLIENT4_HOST:$RUBBOS_APP/iostat-* ./
    scp $CLIENT4_HOST:$RUBBOS_APP/mysql_mon-* ./
    scp $CLIENT4_HOST:$RUBBOS_APP/postgres_lock-* ./
    scp $HTTPD_HOST:$RUBBOS_APP/sar-* ./
    scp $HTTPD_HOST:$RUBBOS_APP/ps-* ./
    scp $HTTPD_HOST:$RUBBOS_APP/iostat-* ./
    scp $HTTPD_HOST:$RUBBOS_APP/mysql_mon-* ./
    scp $HTTPD_HOST:$RUBBOS_APP/postgres_lock-* ./
    scp $TOMCAT1_HOST:$RUBBOS_APP/sar-* ./
    scp $TOMCAT1_HOST:$RUBBOS_APP/ps-* ./
    scp $TOMCAT1_HOST:$RUBBOS_APP/iostat-* ./
    scp $TOMCAT1_HOST:$RUBBOS_APP/mysql_mon-* ./
    scp $TOMCAT1_HOST:$RUBBOS_APP/postgres_lock-* ./
    scp $MYSQL1_HOST:$RUBBOS_APP/sar-* ./
    scp $MYSQL1_HOST:$RUBBOS_APP/ps-* ./
    scp $MYSQL1_HOST:$RUBBOS_APP/iostat-* ./
    scp $MYSQL1_HOST:$RUBBOS_APP/mysql_mon-* ./
    scp $MYSQL1_HOST:$RUBBOS_APP/postgres_lock-* ./
    cd ..
    mv 20* $TMP_RESULTS_DIR_BASE/$RUBBOS_RESULTS_DIR_NAME/
  "

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
