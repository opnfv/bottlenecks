#!/bin/bash

cd /bottlenecks/rubbos/rubbos_scripts/1-1-1
source set_bottlenecks_rubbos_env.sh

echo "STOPPING MYSQL on $HOSTNAME"

cd $MYSQL_HOME
bin/mysqladmin --socket=$MYSQL_SOCKET  --user=root --password=$ROOT_PASSWORD shutdown

echo "MYSQL IS STOPPED on $HOSTNAME"
