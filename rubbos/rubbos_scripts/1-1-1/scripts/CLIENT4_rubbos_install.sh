#!/bin/bash
##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

cd /bottlenecks/rubbos/rubbos_scripts/1-1-1
source set_bottlenecks_rubbos_env.sh

echo "INSTALLING RUBBOS/SYSSTAT on $HOSTNAME"

if [ ! -d "$RUBBOS_APP" ]; then
mkdir -p $RUBBOS_APP
chmod 755 $RUBBOS_APP
fi

# install RUBBoS
tar xzf $SOFTWARE_HOME/$RUBBOS_TARBALL --directory=$RUBBOS_APP
#tar xzf $SOFTWARE_HOME/rubbos_html.tar.gz --directory=$RUBBOS_HOME/Servlet_HTML/
cp $SOFTWARE_HOME/flush_cache $RUBBOS_HOME/bench/.

# install sysstat
tar xzf $SOFTWARE_HOME/$SYSSTAT_TARBALL --directory=$RUBBOS_APP

cd $SYSSTAT_HOME
./configure --prefix=$SYSSTAT_HOME >/dev/null
make >/dev/null 2>&1
sudo make install >/dev/null

# install a script to collect statistics data
cp $OUTPUT_HOME/rubbos_conf/cpu_mem.sh $RUBBOS_APP/.
chmod 755 $RUBBOS_APP/cpu_mem.sh

echo "DONE INSTALLING RUBBOS/SYSSTAT on $HOSTNAME"
