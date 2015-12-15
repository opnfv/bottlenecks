#!/bin/bash

. ../set_bottlenecks_rubbos_env.sh

scp_options="-o StrictHostKeyChecking=no -o BatchMode=yes"

# Packages for BENCHMARK rubbos install
if true; then
ssh $BENCHMARK_HOST "mkdir -p /bottlenecks/rubbos/rubbos_scripts/1-1-1"
scp $scp_options ../set_bottlenecks_rubbos_env.sh $BENCHMARK_HOST:/bottlenecks/rubbos/rubbos_scripts/1-1-1

ssh $BENCHMARK_HOST "
    apt-get update
    apt-get install -y \
        gcc \
        gettext \
        g++ \
        make
"

ssh $BENCHMARK_HOST "mkdir -p $SOFTWARE_HOME"
scp $scp_options $SOFTWARE_HOME/$RUBBOS_TARBALL $BENCHMARK_HOST:$SOFTWARE_HOME/$RUBBOS_TARBALL
scp $scp_options $SOFTWARE_HOME/flush_cache $BENCHMARK_HOST:$SOFTWARE_HOME/flush_cache
scp $scp_options $SOFTWARE_HOME/$SYSSTAT_TARBALL $BENCHMARK_HOST:$SOFTWARE_HOME/$SYSSTAT_TARBALL
ssh $BENCHMARK_HOST "mkdir -p $OUTPUT_HOME/rubbos_conf"
scp $scp_options $OUTPUT_HOME/rubbos_conf/cpu_mem.sh $BENCHMARK_HOST:$OUTPUT_HOME/rubbos_conf/cpu_mem.sh
fi

# Packages for BENCHMARK install
if true; then
scp $scp_options $SOFTWARE_HOME/$JAVA_TARBALL $BENCHMARK_HOST:$SOFTWARE_HOME/$JAVA_TARBALL
fi

# Packages for BENCHMARK configure
if true; then
ssh $BENCHMARK_HOST "mkdir -p $WORK_HOME/rubbos_files"
scp $scp_options -r $WORK_HOME/rubbos_files/Client $BENCHMARK_HOST:$WORK_HOME/rubbos_files
scp $scp_options -r $WORK_HOME/rubbos_files/bench $BENCHMARK_HOST:$WORK_HOME/rubbos_files
ssh $BENCHMARK_HOST "mkdir -p $OUTPUT_HOME/rubbos_conf"
for i in build.properties config.mk Makefile \
         rubbos-servletsBO.sh rubbos-servletsRW.sh
do
    scp $scp_options -r $OUTPUT_HOME/rubbos_conf/$i $BENCHMARK_HOST:$OUTPUT_HOME/rubbos_conf/$i
done
fi

