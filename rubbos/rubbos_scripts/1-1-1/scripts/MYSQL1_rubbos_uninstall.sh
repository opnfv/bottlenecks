#!/bin/bash

cd /bottlenecks/rubbos/rubbos_scripts/1-1-1
source set_bottlenecks_rubbos_env.sh

cd $SYSSTAT_HOME
sudo make uninstall
sudo rm -rf $SYSSTAT_HOME
rm -rf $RUBBOS_HOME
