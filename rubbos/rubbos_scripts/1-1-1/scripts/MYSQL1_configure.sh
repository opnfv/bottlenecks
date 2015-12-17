#!/bin/bash

cd /bottlenecks/rubbos/rubbos_scripts/1-1-1
source set_bottlenecks_rubbos_env.sh

echo "CONFIGURING MYSQL on $HOSTNAME"

cd $MYSQL_HOME
chown -R mysql:mysql ./
cp support-files/my-medium.cnf /etc/my.cnf
#bin/mysqld_safe --user=$BOTTLENECKS_USER &
bin/mysqld_safe&
sleep 10
#bin/mysqladmin -u root password 'new-password'
cp support-files/mysql.server /etc/init.d/mysql.server
/etc/init.d/mysql.server status

if [ -f "/usr/local/bin/mysql" ]; then
rm -rf /usr/local/bin/mysql
fi

ln -s $MYSQL_HOME/bin/mysql /usr/local/bin/mysql

sleep 20
echo "BEGIN MYSQL GIVE PRIVILEGES"
cat << EOF | mysql -uroot

CREATE DATABASE rubbos;

GRANT ALL PRIVILEGES ON rubbos.* TO 'rubbos'@'%' \
    IDENTIFIED BY 'rubbos';
    flush privileges;
GRANT ALL PRIVILEGES ON rubbos.* TO 'rubbos'@'localhost' \
    IDENTIFIED BY 'rubbos';
    flush privileges;
EOF
echo "END MYSQL GIVE PRIVILEGES"

echo "BEGIN IMPORT SQL DATA"
echo "software_home=$SOFTWARE_HOME"
tar xzf $SOFTWARE_HOME/$RUBBOS_DATA_TARBALL --directory /tmp
mysql -uroot rubbos < /tmp/$RUBBOS_DATA_SQL
echo "END IMPORT SQL DATA"
rm /tmp/$RUBBOS_DATA_SQL

echo "DONE CONFIGURING MYSQL on $HOSTNAME"

