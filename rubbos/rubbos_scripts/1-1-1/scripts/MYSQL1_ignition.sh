#!/bin/bash

cd /bottlenecks/rubbos/rubbos_scripts/1-1-1
source set_bottlenecks_rubbos_env.sh

echo "STARTING MYSQL on $HOSTNAME"

# TODO start mysqld here, currently mysql is started by MYSQL1_configure.sh

echo "MYSQL IS RUNNING on $HOSTNAME"
