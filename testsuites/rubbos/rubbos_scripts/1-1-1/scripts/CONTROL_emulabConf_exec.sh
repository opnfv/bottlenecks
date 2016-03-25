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

# Limit pc3000 Memory Capacity

sleep 10

# Make and mount new partiton
echo "*** make FS on a partition and mount it *************************"

for i in "$BENCHMARK_HOST" "$CLIENT1_HOST" "$CLIENT2_HOST" "$CLIENT3_HOST" "$CLIENT4_HOST" "$HTTPD_HOST" "$TOMCAT1_HOST" "$MYSQL1_HOST"
do
ssh $i "
  sudo mkdir -p $ELBA_TOP
  sudo chmod 777 $ELBA_TOP
"
scp $WORK_HOME/emulab_files/limits.conf $i:$ELBA_TOP
scp $WORK_HOME/emulab_files/login $i:$ELBA_TOP
scp $WORK_HOME/emulab_files/file-max $i:$ELBA_TOP

ssh $i "
  sudo mv $ELBA_TOP/limits.conf /etc/security/
  sudo mv $ELBA_TOP/login  /etc/pam.d/
"
done


for i in "$BENCHMARK_HOST" "$CLIENT1_HOST" "$CLIENT2_HOST" "$CLIENT3_HOST" "$CLIENT4_HOST" "$HTTPD_HOST" "$TOMCAT1_HOST" "$MYSQL1_HOST"
do
  ssh $i "
   sudo /sbin/mkfs /dev/sda4 
   sudo mount /dev/sda4 $ELBA_TOP 
   sudo chmod 777 $ELBA_TOP
   mkdir -p $RUBBOS_TOP
   sudo cp $SOFTWARE_HOME/sdparm-1.03.tgz /tmp
   cd /tmp
   sudo tar -zxvf ./sdparm-1.03.tgz
   cd sdparm-1.03
   sudo ./configure
   sudo make
   sudo make install
   sudo sdparm -c WCE /dev/sda
  " &
done

echo "sleep 420"
sleep 420
echo "wake up from sleeping 420"


# Turning off Swap Partition

sleep 10 
