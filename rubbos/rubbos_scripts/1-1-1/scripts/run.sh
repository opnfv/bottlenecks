cd /bottlenecks/rubbos/rubbos_scripts/1-1-1
source set_bottlenecks_rubbos_env.sh
cd /bottlenecks/rubbos/rubbos_scripts/1-1-1/scripts
# Transfer all sub scripts to target hosts
echo "*** scp scripts *************************************************"

scp_options="-o StrictHostKeyChecking=no -o BatchMode=yes"

scp $scp_options CONTROL_checkScp_exec.sh  $CONTROL_HOST:/tmp

scp $scp_options CONTROL_emulabConf_exec.sh  $CONTROL_HOST:/tmp

scp $scp_options CONTROL_rubbos_exec.sh  $CONTROL_HOST:/tmp

scp $scp_options BENCHMARK_rubbos_install.sh  $BENCHMARK_HOST:/tmp

scp $scp_options BENCHMARK_install.sh  $BENCHMARK_HOST:/tmp

scp $scp_options BENCHMARK_configure.sh  $BENCHMARK_HOST:/tmp

scp $scp_options BENCHMARK_uninstall.sh  $BENCHMARK_HOST:/tmp

scp $scp_options BENCHMARK_rubbos_uninstall.sh  $BENCHMARK_HOST:/tmp

scp $scp_options CLIENT1_rubbos_install.sh  $CLIENT1_HOST:/tmp

scp $scp_options CLIENT1_install.sh  $CLIENT1_HOST:/tmp

scp $scp_options CLIENT1_configure.sh  $CLIENT1_HOST:/tmp

scp $scp_options CLIENT1_uninstall.sh  $CLIENT1_HOST:/tmp

scp $scp_options CLIENT1_rubbos_uninstall.sh  $CLIENT1_HOST:/tmp

scp $scp_options CLIENT2_rubbos_install.sh  $CLIENT2_HOST:/tmp

scp $scp_options CLIENT2_install.sh  $CLIENT2_HOST:/tmp

scp $scp_options CLIENT2_configure.sh  $CLIENT2_HOST:/tmp

scp $scp_options CLIENT2_uninstall.sh  $CLIENT2_HOST:/tmp

scp $scp_options CLIENT2_rubbos_uninstall.sh  $CLIENT2_HOST:/tmp

scp $scp_options CLIENT3_rubbos_install.sh  $CLIENT3_HOST:/tmp

scp $scp_options CLIENT3_install.sh  $CLIENT3_HOST:/tmp

scp $scp_options CLIENT3_configure.sh  $CLIENT3_HOST:/tmp

scp $scp_options CLIENT3_uninstall.sh  $CLIENT3_HOST:/tmp

scp $scp_options CLIENT3_rubbos_uninstall.sh  $CLIENT3_HOST:/tmp

scp $scp_options CLIENT4_rubbos_install.sh  $CLIENT4_HOST:/tmp

scp $scp_options CLIENT4_install.sh  $CLIENT4_HOST:/tmp

scp $scp_options CLIENT4_configure.sh  $CLIENT4_HOST:/tmp

scp $scp_options CLIENT4_uninstall.sh  $CLIENT4_HOST:/tmp

scp $scp_options CLIENT4_rubbos_uninstall.sh  $CLIENT4_HOST:/tmp

scp $scp_options  HTTPD_install.sh  $HTTPD_HOST:/tmp

scp $scp_options HTTPD_rubbos_install.sh  $HTTPD_HOST:/tmp

scp $scp_options HTTPD_configure.sh  $HTTPD_HOST:/tmp

scp $scp_options HTTPD_ignition.sh  $HTTPD_HOST:/tmp

scp $scp_options HTTPD_stop.sh  $HTTPD_HOST:/tmp

scp $scp_options HTTPD_rubbos_uninstall.sh  $HTTPD_HOST:/tmp

scp $scp_options HTTPD_uninstall.sh  $HTTPD_HOST:/tmp

scp $scp_options TOMCAT1_install.sh  $TOMCAT1_HOST:/tmp

scp $scp_options TOMCAT1_rubbos_install.sh  $TOMCAT1_HOST:/tmp

scp $scp_options TOMCAT1_configure.sh  $TOMCAT1_HOST:/tmp

scp $scp_options TOMCAT1_rubbosSL_configure.sh  $TOMCAT1_HOST:/tmp

scp $scp_options TOMCAT1_ignition.sh  $TOMCAT1_HOST:/tmp

scp $scp_options TOMCAT1_stop.sh  $TOMCAT1_HOST:/tmp

scp $scp_options TOMCAT1_rubbos_uninstall.sh  $TOMCAT1_HOST:/tmp

scp $scp_options TOMCAT1_uninstall.sh  $TOMCAT1_HOST:/tmp

scp $scp_options MYSQL1_install.sh $MYSQL1_HOST:/tmp

scp $scp_options MYSQL1_rubbos_install.sh  $MYSQL1_HOST:/tmp

scp $scp_options MYSQL1_configure.sh  $MYSQL1_HOST:/tmp

scp $scp_options MYSQL1_reset.sh  $MYSQL1_HOST:/tmp

scp $scp_options MYSQL1_ignition.sh  $MYSQL1_HOST:/tmp

scp $scp_options MYSQL1_stop.sh  $MYSQL1_HOST:/tmp

scp $scp_options MYSQL1_rubbos_uninstall.sh  $MYSQL1_HOST:/tmp

scp $scp_options MYSQL1_uninstall.sh  $MYSQL1_HOST:/tmp


# Install and Configure and run Apache, Tomcat, CJDBC, and MySQL
echo "*** install scripts & configure & execute ***********************"

#ssh root@$CONTROL_HOST chmod 777 /tmp/CONTROL_checkScp_exe.sh  
#ssh $CONTROL_HOST /tmp/CONTROL_checkScp_exec.sh
#ssh root@$CONTROL_HOST chmod 777 /tmp/CONTROL_emulabConf_exec.sh
#ssh $CONTROL_HOST /tmp/CONTROL_emulabConf_exec.sh 

ssh root@$MYSQL1_HOST chmod 770 /tmp/MYSQL1_install.sh
ssh $MYSQL1_HOST /tmp/MYSQL1_install.sh 

ssh root@$TOMCAT1_HOST chmod 770 /tmp/TOMCAT1_install.sh
ssh $TOMCAT1_HOST /tmp/TOMCAT1_install.sh 

ssh root@$HTTPD_HOST chmod 770 /tmp/HTTPD_install.sh
ssh $HTTPD_HOST /tmp/HTTPD_install.sh 

ssh root@$MYSQL1_HOST chmod 770 /tmp/MYSQL1_rubbos_install.sh
ssh $MYSQL1_HOST /tmp/MYSQL1_rubbos_install.sh 

ssh root@$TOMCAT1_HOST chmod 770 /tmp/TOMCAT1_rubbos_install.sh
ssh $TOMCAT1_HOST /tmp/TOMCAT1_rubbos_install.sh 

ssh root@$HTTPD_HOST chmod 770 /tmp/HTTPD_rubbos_install.sh
ssh $HTTPD_HOST /tmp/HTTPD_rubbos_install.sh 

ssh root@$BENCHMARK_HOST chmod 770 /tmp/BENCHMARK_rubbos_install.sh
ssh $BENCHMARK_HOST /tmp/BENCHMARK_rubbos_install.sh 

ssh root@$CLIENT1_HOST chmod 770 /tmp/CLIENT1_rubbos_install.sh 
ssh $CLIENT1_HOST /tmp/CLIENT1_rubbos_install.sh

ssh root@$CLIENT2_HOST chmod 770 /tmp/CLIENT2_rubbos_install.sh
ssh $CLIENT2_HOST /tmp/CLIENT2_rubbos_install.sh

ssh root@$CLIENT3_HOST chmod 770 /tmp/CLIENT3_rubbos_install.sh
ssh $CLIENT3_HOST /tmp/CLIENT3_rubbos_install.sh 

ssh root@$CLIENT4_HOST chmod 770 /tmp/CLIENT4_rubbos_install.sh
ssh $CLIENT4_HOST /tmp/CLIENT4_rubbos_install.sh 

ssh root@$BENCHMARK_HOST chmod 770 /tmp/BENCHMARK_install.sh
ssh $BENCHMARK_HOST /tmp/BENCHMARK_install.sh 

ssh root@$CLIENT1_HOST chmod 770 /tmp/CLIENT1_install.sh
ssh $CLIENT1_HOST /tmp/CLIENT1_install.sh 

#ssh root@$CLIENT2_HOST chmod 777 /tmp/CLIENT2_install.sh
#ssh $CLIENT2_HOST /tmp/CLIENT2_install.sh 

#ssh root@$CLIENT3_HOST chmod 777 /tmp/CLIENT3_install.sh
#ssh $CLIENT3_HOST /tmp/CLIENT3_install.sh 

#ssh root@$CLIENT4_HOST chmod 777 /tmp/CLIENT4_install.sh
#ssh $CLIENT4_HOST /tmp/CLIENT4_install.sh 

ssh root@$MYSQL1_HOST chmod 770 /tmp/MYSQL1_configure.sh
ssh $MYSQL1_HOST /tmp/MYSQL1_configure.sh  &
sleep 60

ssh root@$TOMCAT1_HOST chmod 770 /tmp/TOMCAT1_configure.sh
ssh $TOMCAT1_HOST /tmp/TOMCAT1_configure.sh 

ssh root@$HTTPD_HOST chmod 770 /tmp/HTTPD_configure.sh
ssh $HTTPD_HOST /tmp/HTTPD_configure.sh 

ssh root@$BENCHMARK_HOST chmod 770 /tmp/BENCHMARK_configure.sh
ssh $BENCHMARK_HOST /tmp/BENCHMARK_configure.sh 

ssh root@$CLIENT1_HOST chmod 770 /tmp/CLIENT1_configure.sh
ssh $CLIENT1_HOST /tmp/CLIENT1_configure.sh 

#ssh root@$CLIENT2_HOST chmod 777 /tmp/CLIENT2_configure.sh
#ssh $CLIENT2_HOST /tmp/CLIENT2_configure.sh 

#ssh root@$CLIENT3_HOST chmod 777 /tmp/CLIENT3_configure.sh
#ssh $CLIENT3_HOST /tmp/CLIENT3_configure.sh 

#ssh root@$CLIENT4_HOST chmod 777 /tmp/CLIENT4_configure.sh
#ssh $CLIENT4_HOST /tmp/CLIENT4_configure.sh 

ssh root@$TOMCAT1_HOST chmod 770 /tmp/TOMCAT1_rubbosSL_configure.sh
ssh $TOMCAT1_HOST /tmp/TOMCAT1_rubbosSL_configure.sh


#ssh $CONTROL_HOST /tmp/CONTROL_rubbos_exec.sh 

