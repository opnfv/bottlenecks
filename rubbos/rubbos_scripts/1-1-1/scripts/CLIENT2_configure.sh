#!/bin/bash

cd /bottlenecks/rubbos/rubbos_scripts/1-1-1
source set_bottlenecks_rubbos_env.sh

echo "CONFIGURING RUBBOS CLIENT on $HOSTNAME"

cp -r $WORK_HOME/rubbos_files/Client $RUBBOS_HOME/
cp -r $WORK_HOME/rubbos_files/bench $RUBBOS_HOME/

cp $OUTPUT_HOME/rubbos_conf/build.properties $RUBBOS_HOME/
cp $OUTPUT_HOME/rubbos_conf/config.mk $RUBBOS_HOME/
cp $OUTPUT_HOME/rubbos_conf/Makefile $RUBBOS_HOME/

cp $OUTPUT_HOME/rubbos_conf/rubbos-servletsBO.sh $RUBBOS_HOME/bench/
cp $OUTPUT_HOME/rubbos_conf/rubbos-servletsRW.sh $RUBBOS_HOME/bench/

chmod ug+x $RUBBOS_HOME/bench/*.sh

#build clients
echo "COMPILING RUBBOS CLIENT on $HOSTNAME"
cd $RUBBOS_HOME/Client
make clean
make

echo "DONE CONFIGURING RUBBOS CLIENT on $HOSTNAME"
