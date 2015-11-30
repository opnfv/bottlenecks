#!/bin/bash

cd /bottlenecks/rubbos/rubbos_scripts/1-1-1
source set_bottlenecks_rubbos_env.sh

echo "INSTALLING APACHE on $HOSTNAME"

mkdir -p $BOTTLENECKS_TOP
chmod 755 $BOTTLENECKS_TOP
mkdir -p $RUBBOS_TOP
chmod 755 $RUBBOS_TOP
mkdir -p $RUBBOS_APP
chmod 755 $RUBBOS_APP

# apache
tar zxf $SOFTWARE_HOME/$HTTPD_TARBALL --directory=$RUBBOS_APP
cd $HTTPD_INSTALL_FILES 
./configure --prefix=$HTTPD_HOME --enable-module=so --enable-so --with-mpm=worker
make 
make install 

# mod jk
tar zxf $SOFTWARE_HOME/$MOD_JK_TARBALL --directory=$RUBBOS_APP
tar zxf $SOFTWARE_HOME/$JAVA_TARBALL --directory=$RUBBOS_APP
cd $MOD_JK_INSTALL_CONFIGURE
./configure --with-apxs=$HTTPD_HOME/bin/apxs --enable-jni --with-java-home=$JAVA_HOME
make
make install 

echo "APACHE IS INSTALLED on $HOSTNAME"
