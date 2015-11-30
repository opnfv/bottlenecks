#!/bin/bash

cd /bottlenecks/rubbos/rubbos_scripts/1-1-1
source set_bottlenecks_rubbos_env.sh

$OUTPUT_HOME/scripts/stop_all.sh

for i in "$BENCHMARK_HOST" "$CLIENT1_HOST" "$CLIENT2_HOST" "$CLIENT3_HOST" "$CLIENT4_HOST" "$HTTPD_HOST" "$TOMCAT1_HOST" "$MYSQL1_HOST"
do
  ssh $i "
    kill -9 -1
    "
done

