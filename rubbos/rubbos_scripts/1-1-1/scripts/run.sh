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
for i in {1..4}
do
    for script in CLIENT${i}_rubbos_install.sh CLIENT${i}_install.sh \
                  CLIENT${i}_configure.sh CLIENT${i}_uninstall.sh \
                  CLIENT${i}_rubbos_uninstall.sh
    do
        CLIENT_HOST=`printenv CLIENT${i}_HOST`
        scp $scp_options $script $CLIENT_HOST:/tmp
    done
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
for i in {1..4}
do
    ./CLIENT${i}_pkg_prepare.sh
done

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

for i in {1..4}
do
    CLIENT_HOST=`printenv CLIENT${i}_HOST`
    ssh root@$CLIENT_HOST chmod 770 /tmp/CLIENT${i}_rubbos_install.sh
    ssh $CLIENT_HOST /tmp/CLIENT${i}_rubbos_install.sh
done

ssh root@$BENCHMARK_HOST chmod 770 /tmp/BENCHMARK_install.sh
ssh $BENCHMARK_HOST /tmp/BENCHMARK_install.sh

for i in {1..4}
do
    CLIENT_HOST=`printenv CLIENT${i}_HOST`
    ssh root@$CLIENT_HOST chmod 770 /tmp/CLIENT${i}_install.sh
    ssh $CLIENT_HOST /tmp/CLIENT${i}_install.sh
done

ssh root@$MYSQL1_HOST chmod 770 /tmp/MYSQL1_configure.sh
ssh $MYSQL1_HOST /tmp/MYSQL1_configure.sh

ssh root@$TOMCAT1_HOST chmod 770 /tmp/TOMCAT1_configure.sh
ssh $TOMCAT1_HOST /tmp/TOMCAT1_configure.sh

ssh root@$HTTPD_HOST chmod 770 /tmp/HTTPD_configure.sh
ssh $HTTPD_HOST /tmp/HTTPD_configure.sh

ssh root@$BENCHMARK_HOST chmod 770 /tmp/BENCHMARK_configure.sh
ssh $BENCHMARK_HOST /tmp/BENCHMARK_configure.sh

for i in {1..4}
do
    CLIENT_HOST=`printenv CLIENT${i}_HOST`
    ssh root@$CLIENT_HOST chmod 770 /tmp/CLIENT${i}_configure.sh
    ssh $CLIENT_HOST /tmp/CLIENT${i}_configure.sh
done

ssh root@$TOMCAT1_HOST chmod 770 /tmp/TOMCAT1_rubbosSL_configure.sh
ssh $TOMCAT1_HOST /tmp/TOMCAT1_rubbosSL_configure.sh

