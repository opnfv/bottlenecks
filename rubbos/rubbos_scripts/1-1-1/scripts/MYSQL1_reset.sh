#!/bin/bash

cd /bottlenecks/rubbos/rubbos_scripts/1-1-1
source set_bottlenecks_rubbos_env.sh

echo "RESETING MYSQL on $HOSTNAME"
# copy rubbos data files
tar xzf $RUBBOS_TOP/$RUBBOS_DATA_TARBALL --directory=$MYSQL_HOME/data/rubbos

echo "DONE RESETING MYSQL on $HOSTNAME"
sleep 5 
