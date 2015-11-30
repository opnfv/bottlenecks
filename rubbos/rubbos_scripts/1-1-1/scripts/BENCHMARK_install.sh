#!/bin/bash

cd /bottlenecks/rubbos/rubbos_scripts/1-1-1
source set_bottlenecks_rubbos_env.sh

echo "INSTALLING RUBBOS CLIENT on $HOSTNAME"

if [ ! -d "$RUBBOS_APP" ]; then
mkdir -p $RUBBOS_APP
chmod 755 $RUBBOS_APP
fi

tar xzf $SOFTWARE_HOME/$JAVA_TARBALL --directory=$RUBBOS_APP

echo "DONE INSTALLING RUBBOS CLIENT on $HOSTNAME" 
