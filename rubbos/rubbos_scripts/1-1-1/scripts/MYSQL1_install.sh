#!/bin/bash

cd /bottlenecks/rubbos/rubbos_scripts/1-1-1
source set_bottlenecks_rubbos_env.sh

echo "INSTALLING MYSQL on $HOSTNAME"

mkdir -p $BOTTLENECKS_TOP
chmod 755 $BOTTLENECKS_TOP
mkdir -p $RUBBOS_TOP
chmod 755 $RUBBOS_TOP
mkdir -p $RUBBOS_APP
chmod 755 $RUBBOS_APP

cd /root
groupadd mysql
useradd -r -g mysql $BOTTLENECKS_USER
tar xzf $SOFTWARE_HOME/$MYSQL_TARBALL --directory=$RUBBOS_APP
cd /usr/local
ln -s $MYSQL_HOME mysql
cd mysql
chown -R $BOTTLENECKS_USER .
chgrp -R mysql .
#scripts/mysql_install_db --verbose --user=$BOTTLENECKS_USER --basedir=$MYSQL_HOME --datadir=$MYSQL_DATA_DIR
scripts/mysql_install_db --user=$BOTTLENECKS_USER
chown -R root .
chown -R $BOTTLENECKS_USER data 
  
#echo "begin install mysql"
#cd $MYSQL_HOME 
#scripts/mysql_install_db --no-defaults --user=root --basedir=$MYSQL_HOME --port=$MYSQL_PORT --datadir=$MYSQL_DATA_DIR --log=$MYSQL_ERR_LOG --pid-file=$MYSQL_PID_FILE --socket=$MYSQL_SOCKET

echo "DONE INSTALLING MYSQL on $HOSTNAME" 
