#!/bin/bash

cd /bottlenecks/rubbos/rubbos_scripts/1-1-1
source set_bottlenecks_rubbos_env.sh

echo "INSTALLING RUBBOS/SYSSTAT on $HOSTNAME"

mkdir -p $RUBBOS_APP

# install RUBBoS
tar xzf $SOFTWARE_HOME/$RUBBOS_TARBALL --directory=$RUBBOS_APP
#tar xzf $SOFTWARE_HOME/rubbos_html.tar.gz --directory=$RUBBOS_HOME/Servlet_HTML/
cp $SOFTWARE_HOME/flush_cache $RUBBOS_HOME/bench/.

# install sysstat
tar xzf $SOFTWARE_HOME/$SYSSTAT_TARBALL --directory=$RUBBOS_APP

cd $SYSSTAT_HOME
./configure --prefix=$SYSSTAT_HOME
make
sudo make install

# install a script to collect statistics data
cp $OUTPUT_HOME/rubbos_conf/cpu_mem.sh $RUBBOS_APP/.
chmod 755 $RUBBOS_APP/cpu_mem.sh

echo "DONE INSTALLING RUBBOS/SYSSTAT on $HOSTNAME"
