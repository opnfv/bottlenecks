#!/bin/bash

set -o allexport

# HOSTS
CONTROL_HOST=192.168.50.60
BENCHMARK_HOST=192.168.50.60
CLIENT1_HOST=192.168.50.60
CLIENT2_HOST=192.168.50.60
CLIENT3_HOST=192.168.50.60
CLIENT4_HOST=192.168.50.60
HTTPD_HOST=192.168.50.58
TOMCAT1_HOST=192.168.50.18
MYSQL1_HOST=192.168.50.19

# Experiment name on OPNFV
BOTTLNECKS_NAME=bottlenecks

# Directories from which files are copied
WORK_HOME=/bottlenecks/rubbos/rubbos_scripts/rubbosMulini6
OUTPUT_HOME=/bottlenecks/rubbos/rubbos_scripts/1-1-1
SOFTWARE_HOME=/bottlenecks/rubbos/app_tools

# Output directory for results of RUBBoS benchmark
RUBBOS_RESULTS_HOST=192.168.50.58
RUBBOS_RESULTS_DIR_BASE=/bottlenecks/rubbos/rubbos_results
RUBBOS_RESULTS_DIR_NAME=2015-01-20T081237-0700

# Target directories
BOTTLENECKS_TOP=/bottlenecks
RUBBOS_TOP=$BOTTLENECKS_TOP/rubbos
RUBBOS_APP=$RUBBOS_TOP/app
TMP_RESULTS_DIR_BASE=$RUBBOS_TOP/tmp_results
RUBBOS_HOME=$RUBBOS_APP/RUBBoS
SYSSTAT_HOME=$RUBBOS_APP/sysstat-9.0.6

HTTPD_HOME=$RUBBOS_APP/apache2
HTTPD_INSTALL_FILES=$RUBBOS_APP/httpd-2.0.64
MOD_JK_INSTALL_FILES=$RUBBOS_APP/tomcat-connectors-1.2.32-src
MOD_JK_INSTALL_CONFIGURE=$MOD_JK_INSTALL_FILES/native
CATALINA_HOME=$RUBBOS_APP/apache-tomcat-5.5.17
SERVLET_API_PATH=$CATALINA_HOME/common/lib/servlet-api.jar
CATALINA_BASE=$CATALINA_HOME
CJDBC_HOME=

MYSQL_HOME=$RUBBOS_APP/mysql-5.5.46-linux2.6-x86_64

# Java & Ant
JAVA_HOME=$RUBBOS_APP/jdk1.6.0_27
JAVA_OPTS="-Xmx1300m"
J2EE_HOME=$RUBBOS_APP/j2sdkee1.3.1
ANT_HOME=$RUBBOS_APP/apache-ant-1.6.5

# Tarballs
JAVA_TARBALL=jdk1.6.0_27.tar.gz
J2EE_TARBALL=j2sdkee1.3.1.jar.gz
ANT_TARBALL=apache-ant-1.6.5.tar.gz
SYSSTAT_TARBALL=sysstat-9.0.6.tar.gz
HTTPD_TARBALL=httpd-2.0.64.tar.gz
MOD_JK_TARBALL=tomcat-connectors-1.2.32-src.tar.gz
TOMCAT_TARBALL=apache-tomcat-5.5.17.tar.gz
CJDBC_TARBALL=
MYSQL_TARBALL=mysql-5.5.46-linux2.6-x86_64.tar.gz
RUBBOS_TARBALL=RUBBoS-servlets.tar.gz
RUBBOS_DATA_TARBALL=rubbos_data.tar.gz
RUBBOS_DATA_TEXTFILES_TARBALL=smallDB-rubbos-modified.tgz

# for MySQL
MYSQL_CONNECTOR=mysql-connector-java-5.1.7-bin.jar
MYSQL_PORT=3313
MYSQL_SOCKET=$MYSQL_HOME/mysql.sock
MYSQL_DATA_DIR=$MYSQL_HOME/data
MYSQL_ERR_LOG=$MYSQL_HOME/data/mysql.log
MYSQL_PID_FILE=$MYSQL_HOME/run/mysqld.pid

# for DBs & C-JDBC
ROOT_PASSWORD=new-password
BOTTLENECKS_USER=bottlenecks
BOTTLENECKS_PASSWORD=bottlenecks


CLASSPATH=$CLASSPATH:$JONAS_ROOT/bin/unix/registry:$JAVA_HOME:$JAVA_HOME/lib/tools.jar:$SERVLET_API_PATH:.

PATH=$JAVA_HOME/bin:$JONAS_ROOT/bin/unix:$ANT_HOME/bin:$CATALINA_HOME/bin:$PATH
set +o allexport

