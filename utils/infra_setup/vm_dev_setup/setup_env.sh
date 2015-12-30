#!/bin/bash

set -ex

bottlenecks_prepare_env()
{
    echo "Bottlenecks: install preinstall packages in VM"

    for i in $PreInstall_Packages; do
        if ! apt --installed list 2>/dev/null |grep "\<$i\>"
        then
            sudo apt-get install  -y --force-yes  $i
        fi
    done
}

bottlenecks_download_repo()
{
    echo "Bottlenecks: download bottlenecks repo"

    if [ -d $BOTTELENECKS_REPO_DIR/.git ]; then
        cd $BOTTLENECKS_REPO_DIR
        git pull origin master
        cd -
    else
        rm -rf $BOTTLENECKS_REPO_DIR
        git clone $BOTTLENECKS_REPO $BOTTLENECKS_REPO_DIR
    fi
}

bottlenecks_config_hosts_ip()
{
    sed -i -e "s/REPLACE_CONTROL_HOST/$rubbos_control/g" \
           -e "s/REPLACE_HTTPD_HOST/$rubbos_httpd/g" \
           -e "s/REPLACE_MYSQL1_HOST/$rubbos_mysql1/g" \
           -e "s/REPLACE_TOMCAT1_HOST/$rubbos_tomcat1/g" \
           -e "s/REPLACE_CLIENT1_HOST/$rubbos_client1/g" \
           -e "s/REPLACE_CLIENT2_HOST/$rubbos_client2/g" \
           -e "s/REPLACE_CLIENT3_HOST/$rubbos_client3/g" \
           -e "s/REPLACE_CLIENT4_HOST/$rubbos_client4/g" \
           -e "s/REPLACE_BENCHMARK_HOST/$rubbos_benchmark/g" \
           $BOTTELENECKS_REPO_DIR/rubbos/rubbos_scripts/1-1-1/set_bottlenecks_rubbos_env.sh
}

bottlenecks_download_packages()
{
    echo "Bottlenecks: download rubbos dependent packages from artifacts"

    curl --connect-timeout 10 -o /tmp/app_tools.tar.gz $RUBBOS_APP_TOOLS_URL 2>/dev/null
    tar zxvf /tmp/app_tools.tar.gz -C $RUBBOS_DIR
    rm -rf /tmp/app_tools.tar.gz
    curl --connect-timeout 10 -o /tmp/rubbosMulini6.tar.gz $RUBBOS_MULINI6_URL 2>/dev/null
    tar zxvf /tmp/rubbosMulini6.tar.gz -C $RUBBOS_MULINI6_DIR
    rm -rf /tmp/rubbosMulini6.tar.gz
}

bottlenecks_rubbos_install_exe()
{
    echo "Bottlenecks: install and run rubbos"

    cd $RUBBOS_RUN_DIR
    ./run.sh
    cd $RUBBOS_EXE_DIR
    ./CONTROL_rubbos_exec.sh
}

main()
{
    PreInstall_Packages="git gcc gettext g++ libaio1 libaio-dev make"
    SCRIPT_DIR=`cd ${BASH_SOURCE[0]%/*};pwd`

    source $SCRIPT_DIR/package.conf
    source $SCRIPT_DIR/hosts.conf

    bottlenecks_prepare_env
    bottlenecks_download_repo
    bottlenecks_download_packages
    bottlenecks_rubbos_install_exe
}

main
set +ex
