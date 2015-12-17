#!/bin/bash

. ../set_bottlenecks_rubbos_env.sh

scp_options="-o StrictHostKeyChecking=no -o BatchMode=yes"

# Packages for MYSQL1 install
if true; then
ssh $MYSQL1_HOST "mkdir -p /bottlenecks/rubbos/rubbos_scripts/1-1-1"
scp $scp_options ../set_bottlenecks_rubbos_env.sh $MYSQL1_HOST:/bottlenecks/rubbos/rubbos_scripts/1-1-1

ssh $MYSQL1_HOST "mkdir -p $SOFTWARE_HOME"
scp $scp_options $SOFTWARE_HOME/$MYSQL_TARBALL $MYSQL1_HOST:$SOFTWARE_HOME/$MYSQL_TARBALL

ssh $MYSQL1_HOST "
    apt-get update
    apt-get install -y \
        gcc \
        gettext \
        g++ \
        libaio1 \
        libaio-dev \
        make
"

fi

# Packages for MYSQL1 rubbos install
if true; then
scp $scp_options $SOFTWARE_HOME/$RUBBOS_TARBALL $MYSQL1_HOST:$SOFTWARE_HOME/$RUBBOS_TARBALL
scp $scp_options $SOFTWARE_HOME/flush_cache $MYSQL1_HOST:$SOFTWARE_HOME/flush_cache
scp $scp_options $SOFTWARE_HOME/$SYSSTAT_TARBALL $MYSQL1_HOST:$SOFTWARE_HOME/$SYSSTAT_TARBALL
ssh $MYSQL1_HOST "mkdir -p $OUTPUT_HOME/rubbos_conf"
scp $scp_options $OUTPUT_HOME/rubbos_conf/cpu_mem.sh $MYSQL1_HOST:$OUTPUT_HOME/rubbos_conf/cpu_mem.sh
fi

# Packages for MYSQL1 configure
if true; then
scp $scp_options $SOFTWARE_HOME/$RUBBOS_DATA_TARBALL $MYSQL1_HOST:/tmp
fi

