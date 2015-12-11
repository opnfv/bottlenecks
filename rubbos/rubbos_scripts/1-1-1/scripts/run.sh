cd /bottlenecks/rubbos/rubbos_scripts/1-1-1
source set_bottlenecks_rubbos_env.sh
cd /bottlenecks/rubbos/rubbos_scripts/1-1-1/scripts
# Transfer all sub scripts to target hosts
echo "*** scp scripts *************************************************"

scp_options="-o StrictHostKeyChecking=no -o BatchMode=yes"

if true; then
for script in HTTPD_install.sh HTTPD_rubbos_install.sh \
              HTTPD_configure.sh HTTPD_ignition.sh \
              HTTPD_stop.sh HTTPD_rubbos_uninstall.sh \
              HTTPD_uninstall.sh
do
    scp $scp_options $script $HTTPD_HOST:/tmp
done

fi
# Prepare software packages
echo "*** prepare software packages ***"
./HTTPD_pkg_prepare.sh

# Install and Configure and run Apache, Tomcat, CJDBC, and MySQL
echo "*** install scripts & configure & execute ***********************"

ssh root@$HTTPD_HOST chmod 770 /tmp/HTTPD_install.sh
ssh $HTTPD_HOST /tmp/HTTPD_install.sh

ssh root@$HTTPD_HOST chmod 770 /tmp/HTTPD_rubbos_install.sh
ssh $HTTPD_HOST /tmp/HTTPD_rubbos_install.sh

ssh root@$HTTPD_HOST chmod 770 /tmp/HTTPD_configure.sh
ssh $HTTPD_HOST /tmp/HTTPD_configure.sh

