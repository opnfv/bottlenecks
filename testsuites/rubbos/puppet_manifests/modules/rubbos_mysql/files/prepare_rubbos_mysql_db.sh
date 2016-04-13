#!/bin/bash
#############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


## Usage: prepare_rubbos_mysql_db.sh rubbos_data_sql.tar.gz rubbos_data_sql_dir
##   It is used for loading data into mysql database.
if [ ! -d '/usr/local/mysql' ] || [ $# -ne 2 ] || [ ! -f $1 ];then
    echo "It requires: Mysql is installed, two arguments, and the second points to a data_sql file."
    exit 1;
fi

rubbos_mysql_db_compressed_file=$1
rubbos_mysql_db_uncompressed_dir=$2

# clear database
echo "BEGIN RUBBOS DATABASE GIVE PRIVILEGES"
cat << EOF | /usr/local/mysql/bin/mysql -uroot

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

# import sql data
echo "BEGIN IMPORT SQL DATA"
if [ -d '${rubbos_mysql_db_uncompressed_dir}' ]; then
   rm -rf ${rubbos_mysql_db_uncompressed_dir}
fi
mkdir -p ${rubbos_mysql_db_uncompressed_dir}
tar zxvf ${rubbos_mysql_db_compressed_file} --directory ${rubbos_mysql_db_uncompressed_dir}
/usr/local/mysql/bin/mysql -uroot rubbos < ${rubbos_mysql_db_uncompressed_dir}/rubbos_data_sql
echo "END IMPORT SQL DATA"

rm -rf ${rubbos_mysql_db_uncompressed_dir}
