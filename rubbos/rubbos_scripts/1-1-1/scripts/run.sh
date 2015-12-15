cd /bottlenecks/rubbos/rubbos_scripts/1-1-1
source set_bottlenecks_rubbos_env.sh
cd /bottlenecks/rubbos/rubbos_scripts/1-1-1/scripts
# Transfer all sub scripts to target hosts
echo "*** scp scripts *************************************************"

scp_options="-o StrictHostKeyChecking=no -o BatchMode=yes"

if true; then
for script in BENCHMARK_rubbos_install.sh BENCHMARK_install.sh \
              BENCHMARK_configure.sh BENCHMARK_uninstall.sh \
              BENCHMARK_rubbos_uninstall.sh
do
    scp $scp_options $script $BENCHMARK_HOST:/tmp
done
fi

if true; then
for script in HTTPD_install.sh HTTPD_rubbos_install.sh \
              HTTPD_configure.sh HTTPD_ignition.sh \
              HTTPD_stop.sh HTTPD_rubbos_uninstall.sh \
              HTTPD_uninstall.sh
do
    scp $scp_options $script $HTTPD_HOST:/tmp
done
fi

if true; then
for script in TOMCAT1_install.sh TOMCAT1_rubbos_install.sh \
              TOMCAT1_configure.sh TOMCAT1_rubbosSL_configure.sh \
              TOMCAT1_ignition.sh TOMCAT1_stop.sh \
              TOMCAT1_rubbos_uninstall.sh TOMCAT1_uninstall.sh
do
    scp $scp_options $script $TOMCAT1_HOST:/tmp
done
fi

if true; then
for script in MYSQL1_install.sh MYSQL1_rubbos_install.sh \
              MYSQL1_configure.sh MYSQL1_reset.sh \
              MYSQL1_ignition.sh MYSQL1_stop.sh \
              MYSQL1_rubbos_uninstall.sh \
              MYSQL1_uninstall.sh
do
    scp $scp_options $script $MYSQL1_HOST:/tmp
done
fi

# Prepare software packages
echo "*** prepare software packages ***"
./MYSQL1_pkg_prepare.sh
./TOMCAT1_pkg_prepare.sh
./HTTPD_pkg_prepare.sh
./BENCHMARK_pkg_prepare.sh

# Install and Configure and run Apache, Tomcat, CJDBC, and MySQL
echo "*** install scripts & configure & execute ***********************"

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

ssh root@$BENCHMARK_HOST chmod 770 /tmp/BENCHMARK_install.sh
ssh $BENCHMARK_HOST /tmp/BENCHMARK_install.sh

ssh root@$MYSQL1_HOST chmod 770 /tmp/MYSQL1_configure.sh
ssh $MYSQL1_HOST /tmp/MYSQL1_configure.sh

ssh root@$TOMCAT1_HOST chmod 770 /tmp/TOMCAT1_configure.sh
ssh $TOMCAT1_HOST /tmp/TOMCAT1_configure.sh

ssh root@$HTTPD_HOST chmod 770 /tmp/HTTPD_configure.sh
ssh $HTTPD_HOST /tmp/HTTPD_configure.sh

ssh root@$BENCHMARK_HOST chmod 770 /tmp/BENCHMARK_configure.sh
ssh $BENCHMARK_HOST /tmp/BENCHMARK_configure.sh

ssh root@$TOMCAT1_HOST chmod 770 /tmp/TOMCAT1_rubbosSL_configure.sh
ssh $TOMCAT1_HOST /tmp/TOMCAT1_rubbosSL_configure.sh

