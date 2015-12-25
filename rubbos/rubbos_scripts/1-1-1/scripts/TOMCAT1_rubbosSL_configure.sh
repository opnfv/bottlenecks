#!/bin/bash

cd /bottlenecks/rubbos/rubbos_scripts/1-1-1
source set_bottlenecks_rubbos_env.sh

echo "CONFIGURING RUBBOS SERVLET on $HOSTNAME"

\cp $OUTPUT_HOME/rubbos_conf/build.properties $RUBBOS_HOME/

\cp -r $WORK_HOME/rubbos_files/Servlets $RUBBOS_HOME/
\cp $OUTPUT_HOME/rubbos_conf/mysql.properties $RUBBOS_HOME/Servlets/
\cp $OUTPUT_HOME/rubbos_conf/build.xml $RUBBOS_HOME/Servlets/
\cp $OUTPUT_HOME/rubbos_conf/Config.java $RUBBOS_HOME/Servlets/edu/rice/rubbos/servlets/
\cp $OUTPUT_HOME/rubbos_conf/web.xml $RUBBOS_HOME/Servlet_HTML/WEB-INF/

cd $RUBBOS_HOME/Servlets/edu/rice/rubbos/servlets
sed 's/public static final int    BrowseCategoriesPoolSize      = 6;/public static final int    BrowseCategoriesPoolSize      = 12;/g' Config.java > Config.java.tmp
mv Config.java.tmp Config.java

cd $RUBBOS_HOME/Servlets
/bottlenecks/rubbos/app/apache-ant-1.6.5/bin/ant clean >/dev/null
/bottlenecks/rubbos/app/apache-ant-1.6.5/bin/ant dist >/dev/null
make >/dev/null
cp rubbos.war $CATALINA_HOME/webapps/

echo "DONE CONFIGURING RUBBOS SERVLET on $HOSTNAME" 
