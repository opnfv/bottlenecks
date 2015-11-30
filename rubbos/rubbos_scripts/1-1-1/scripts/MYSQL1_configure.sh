#!/bin/bash

cd /bottlenecks/rubbos/rubbos_scripts/1-1-1
source set_bottlenecks_rubbos_env.sh

echo "CONFIGURING MYSQL on $HOSTNAME"

cd $MYSQL_HOME
cp support-files/my-medium.cnf /etc/my.cnf
bin/mysqld_safe --user=$BOTTLENECKS_USER &
sleep 10
#bin/mysqladmin -u root password 'new-password'
cp support-files/mysql.server /etc/init.d/mysql.server
/etc/init.d/mysql.server status

if [ -f "/usr/local/bin/mysql" ]; then
rm -rf /usr/local/bin/mysql
fi

ln -s $MYSQL_HOME/bin/mysql /usr/local/bin/mysql

echo "DONE CONFIGURING MYSQL on $HOSTNAME"
