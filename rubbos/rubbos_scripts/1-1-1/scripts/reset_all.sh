#!/bin/bash

cd /bottlenecks/rubbos/rubbos_scripts/1-1-1
source set_bottlenecks_rubbos_env.sh

ssh $MYSQL1_HOST  /tmp/MYSQL1_reset.sh  &
sleep 120

