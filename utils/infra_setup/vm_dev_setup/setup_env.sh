#!/bin/bash

set -x

wait_vm_ok() {
    ip=$1

    retry=0
    until timeout 10s ssh $ssh_args ec2-user@$ip "exit" >/dev/null 2>&1
    do
        echo "retry connect rubbos vm ip $ip $retry"
        sleep 1
        let retry+=1
        if [[ $retry -ge $2 ]];then
            echo "rubbos control start timeout !!!"
            #exit 1
        fi
    done
}

bottlenecks_prepare_env()
{
    echo "Bottlenecks prepare env in VMs"

    # configue rubbos control ssh key
    generate_ssh_key

    # wait all other VMs ok
    for i in $rubbos_benchmark $rubbos_client1 $rubbos_client2 \
             $rubbos_client3 $rubbos_client4 $rubbos_httpd $rubbos_mysql1 $rubbos_tomcat1
    do
        wait_vm_ok $i 360
    done

    # configue other VMs
    for i in $rubbos_benchmark $rubbos_client1 $rubbos_client2 \
             $rubbos_client3 $rubbos_client4 $rubbos_httpd $rubbos_mysql1 $rubbos_tomcat1
    do
          scp $ssh_args -r $SCRIPT_DIR ec2-user@$i:/tmp
          ssh $ssh_args ec2-user@$i "sudo bash $SCRIPT_DIR/vm_prepare_setup.sh" &
    done

    # ugly use ssh execute script to fix ec2-user previlege issue
    ssh $ssh_args ec2-user@$rubbos_control "sudo bash $SCRIPT_DIR/vm_prepare_setup.sh"

    # test root access
    for i in $rubbos_control $rubbos_benchmark $rubbos_client1 $rubbos_client2 \
             $rubbos_client3 $rubbos_client4 $rubbos_httpd $rubbos_mysql1 $rubbos_tomcat1
    do
          ssh $ssh_args root@$i "uname -a"
    done
}

bottlenecks_download_repo()
{
    echo "Bottlenecks: download bottlenecks repo"

    sudo git config --global http.sslVerify false
    if [ -d $BOTTLENECKS_REPO_DIR/.git ]; then
        cd $BOTTLENECKS_REPO_DIR
        sudo git pull origin master
        if [ x"$GERRIT_REFSPEC_DEBUG" != x ]; then
            sudo git fetch $BOTTLENECKS_REPO $GERRIT_REFSPEC_DEBUG && sudo git checkout FETCH_HEAD
        fi
        cd -
    else
        sudo rm -rf $BOTTLENECKS_REPO_DIR
        sudo git clone $BOTTLENECKS_REPO $BOTTLENECKS_REPO_DIR
        if [ x"$GERRIT_REFSPEC_DEBUG" != x ]; then
            cd $BOTTLENECKS_REPO_DIR
            echo "fetch $GERRIT_REFSPEC_DEBUG"
            sudo git fetch $BOTTLENECKS_REPO $GERRIT_REFSPEC_DEBUG && sudo git checkout FETCH_HEAD
            cd -
        fi

    fi
}

bottlenecks_config_hosts_ip()
{
    sudo sed -i -e "s/REPLACE_CONTROL_HOST/$rubbos_control/g" \
           -e "s/REPLACE_HTTPD_HOST/$rubbos_httpd/g" \
           -e "s/REPLACE_MYSQL1_HOST/$rubbos_mysql1/g" \
           -e "s/REPLACE_TOMCAT1_HOST/$rubbos_tomcat1/g" \
           -e "s/REPLACE_CLIENT1_HOST/$rubbos_client1/g" \
           -e "s/REPLACE_CLIENT2_HOST/$rubbos_client2/g" \
           -e "s/REPLACE_CLIENT3_HOST/$rubbos_client3/g" \
           -e "s/REPLACE_CLIENT4_HOST/$rubbos_client4/g" \
           -e "s/REPLACE_BENCHMARK_HOST/$rubbos_benchmark/g" \
           $BOTTLENECKS_REPO_DIR/rubbos/rubbos_scripts/1-1-1/set_bottlenecks_rubbos_env.sh
}

bottlenecks_download_packages()
{
    echo "Bottlenecks: download rubbos dependent packages from artifacts"

    curl --connect-timeout 10 -o /tmp/app_tools.tar.gz $RUBBOS_APP_TOOLS_URL 2>/dev/null
    sudo tar zxf /tmp/app_tools.tar.gz -C $RUBBOS_DIR
    rm -rf /tmp/app_tools.tar.gz
    curl --connect-timeout 10 -o /tmp/rubbosMulini6.tar.gz $RUBBOS_MULINI6_URL 2>/dev/null
    sudo tar zxf /tmp/rubbosMulini6.tar.gz -C $RUBBOS_MULINI6_DIR
    rm -rf /tmp/rubbosMulini6.tar.gz
}

bottlenecks_rubbos_install_exe()
{
    echo "Bottlenecks: install and run rubbos"

    cd $RUBBOS_RUN_DIR
    sudo ./run.sh
}

main()
{
    SCRIPT_DIR=`cd ${BASH_SOURCE[0]%/*};pwd`

    ssh_args="-o StrictHostKeyChecking=no -o BatchMode=yes"
    source $SCRIPT_DIR/package.conf
    source $SCRIPT_DIR/hosts.conf
    source $SCRIPT_DIR/common.sh

    bottlenecks_prepare_env
    set -x
    bottlenecks_download_repo
    bottlenecks_config_hosts_ip
    bottlenecks_download_packages
    bottlenecks_rubbos_install_exe
}

main
set +x
