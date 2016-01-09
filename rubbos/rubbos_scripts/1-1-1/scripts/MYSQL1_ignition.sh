#!/bin/bash

cd /bottlenecks/rubbos/rubbos_scripts/1-1-1
source set_bottlenecks_rubbos_env.sh

echo "STARTING MYSQL on $HOSTNAME $(date)"

cd $MYSQL_HOME
bin/mysqld_safe&
sleep 10
/etc/init.d/mysql.server status


echo "MYSQL IS RUNNING on $HOSTNAME $(date)"
