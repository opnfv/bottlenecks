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

echo "RESETING MYSQL on $HOSTNAME"
# copy rubbos data files
#tar xzf $RUBBOS_TOP/$RUBBOS_DATA_TARBALL --directory=$MYSQL_HOME/data/rubbos
cd $MYSQL_HOME
bin/mysqld_safe&
sleep 10
/etc/init.d/mysql.server status

echo "BEGIN RUBBOS DATABASE GIVE PRIVILEGES"
cat << EOF | mysql -uroot

DROP DATABASE IF EXISTS rubbos;

CREATE DATABASE rubbos;

GRANT ALL PRIVILEGES ON rubbos.* TO 'rubbos'@'%' \
    IDENTIFIED BY 'rubbos';
    flush privileges;
GRANT ALL PRIVILEGES ON rubbos.* TO 'rubbos'@'localhost' \
    IDENTIFIED BY 'rubbos';
    flush privileges;
EOF
echo "END RUBBOS DATABASE GIVE PRIVILEGES"

echo "BEGIN IMPORT SQL DATA $(date)"
echo "software_home=$SOFTWARE_HOME"
tar xzf $SOFTWARE_HOME/$RUBBOS_DATA_TARBALL --directory /tmp
mysql -uroot rubbos < /tmp/$RUBBOS_DATA_SQL
echo "END IMPORT SQL DATA $(date)"
rm /tmp/$RUBBOS_DATA_SQL

bin/mysqladmin shutdown

echo "DONE RESETING MYSQL on $HOSTNAME"
sleep 5 

