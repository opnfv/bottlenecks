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
for i in {2..17..5}
do
  echo "Start Browsing Only with rubbos.properties_$((100*i)) $(date)"

  ssh $BENCHMARK_HOST "
    source /bottlenecks/rubbos/rubbos_scripts/1-1-1/set_bottlenecks_rubbos_env.sh
    rm -f $RUBBOS_HOME/Client/rubbos.properties
  "

  sed -e "s/REPLACE_HTTPD_HOST/$HTTPD_HOST/g" \
      -e "s/REPLACE_TOMCAT1_HOST/$TOMCAT1_HOST/g" \
      -e "s/REPLACE_MYSQL1_HOST/$MYSQL1_HOST/g" \
      -e "s#REPLACE_CLIENT1_HOST#$CLIENT1_HOST#g" \
      -e "s#REPLACE_CLIENT2_HOST#$CLIENT2_HOST#g" \
      -e "s#REPLACE_CLIENT3_HOST#$CLIENT3_HOST#g" \
      -e "s#REPLACE_CLIENT4_HOST#$CLIENT4_HOST#g" \
      -e "s/REPLACE_NUMBER_OF_CLIENTS_PER_NODE/$((20*i))/g" \
      $OUTPUT_HOME/rubbos_conf/rubbos.properties_template \
      > $OUTPUT_HOME/rubbos_conf/rubbos.properties
  scp $OUTPUT_HOME/rubbos_conf/rubbos.properties $BENCHMARK_HOST:$RUBBOS_HOME/Client/rubbos.properties
  rm -rf $OUTPUT_HOME/rubbos_conf/rubbos.properties

  echo "Resetting all data"
  $OUTPUT_HOME/scripts/reset_all.sh

  # Browsing Only
  echo "Start Browsing Only with rubbos.properties_$((100*i))"
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
    set -x
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
      for f in 'sar-*' 'ps-*' 'iostat-*' 'mysql_mon-*' 'postgres_lock-*'
      do
        scp $scp_options \$host:$RUBBOS_APP/\$f ./
      done
    done
    cd ..
    find -type f
    find -type f | grep stat_client | xargs grep throughput
    mv 20* $TMP_RESULTS_DIR_BASE/$RUBBOS_RESULTS_DIR_NAME/
  "

  $OUTPUT_HOME/scripts/stop_all.sh
  $OUTPUT_HOME/scripts/kill_all.sh
  sleep 15

  echo "End Browsing Only with rubbos.properties_$((100*i)) $(date)"
done

echo "Processing the results..."
ssh $BENCHMARK_HOST "
  cd $TMP_RESULTS_DIR_BASE
  #cd $RUBBOS_RESULTS_DIR_NAME
  #scp $RUBBOS_RESULTS_HOST:$RUBBOS_RESULTS_DIR_BASE/calc-sarSummary.prl ../
  #../calc-sarSummary.prl

  #rm -f 20*/*.bin

  #cd ../
  tar zcf $RUBBOS_RESULTS_DIR_NAME.tgz $RUBBOS_RESULTS_DIR_NAME
  scp $scp_options $RUBBOS_RESULTS_DIR_NAME.tgz $RUBBOS_RESULTS_HOST:$RUBBOS_RESULTS_DIR_BASE/
"

echo "Push the results to DB..."
cd $RUBBOS_RESULTS_DIR_BASE

ls $RUBBOS_RESULTS_DIR_NAME.tgz
tar zxf $RUBBOS_RESULTS_DIR_NAME.tgz
ls $RUBBOS_RESULTS_DIR_NAME

echo "Fetch POD env parameters"
source /tmp/vm_dev_setup/hosts.conf
sed -i -e "s/REPLACE_POD_NAME/$POD_NAME/g" \
       -e "s/REPLACE_INSTALLER_TYPE/$INSTALLER_TYPE/g" \
       -e "s/REPLACE_VERSION/$BOTTLENECKS_VERSION/g" \
       -e "s#REPLACE_TARGET_IP_PORT#$BOTTLENECKS_DB_TARGET#g" \
          $BOTTLENECKS_TOP/utils/dashboard/dashboard.yaml

cat $BOTTLENECKS_TOP/utils/dashboard/dashboard.yaml

python $BOTTLENECKS_TOP/utils/dashboard/process_data.py \
           $RUBBOS_RESULTS_DIR_BASE/$RUBBOS_RESULTS_DIR_NAME \
           $BOTTLENECKS_TOP/utils/dashboard/dashboard.yaml
cd -

echo "Finish RUBBoS"
touch /tmp/rubbos_finished

set +x

