#!/bin/bash

cd /bottlenecks/rubbos/rubbos_scripts/1-1-1
source set_bottlenecks_rubbos_env.sh

echo "INSTALLING RUBBOS CLIENT on $HOSTNAME"

tar xzf $SOFTWARE_HOME/$JAVA_TARBALL --directory=$RUBBOS_APP

echo "DONE INSTALLING RUBBOS CLIENT on $HOSTNAME"
