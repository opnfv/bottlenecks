#!/bin/bash
##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

set -x

generate_ssh_key() {
    uname -a
    whoami
    if [ ! -d ~/.ssh ]; then
        mkdir ~/.ssh
    fi

    chmod 600 ~/.ssh/id_rsa

    if [ ! -d /root/.ssh ]; then
        mkdir /root/.ssh
    fi
    
    sudo sed -ie 's/ssh-rsa/\n&/g' /root/.ssh/authorized_keys
    sudo sed -ie '/echo/d' /root/.ssh/authorized_keys
}

configue_nameserver()
{
    echo "Bottlenecks: configue nameserver"
    sudo rm /etc/resolv.conf
    sudo echo "nameserver 8.8.8.8" >> /etc/resolv.conf
    sudo echo "nameserver 8.8.4.4" >> /etc/resolv.conf

    ping -c 1 www.google.com
}

install_packages()
{
    echo "Bottlenecks: install preinstall packages in VM"
    sudo apt-get update

    for i in $@; do
        if ! apt --installed list 2>/dev/null |grep "\<$i\>"
        then
            sudo apt-get install -y --force-yes $i
        fi
    done
}

hosts_config()
{
    echo "Bottlnecks: hosts config"
    sudo echo "
$rubbos_benchmark rubbos-benchmark
$rubbos_client1 rubbos-client1
$rubbos_client2 rubbos-client2
$rubbos_client3 rubbos-client3
$rubbos_client4 rubbos-client4
$rubbos_control rubbos-control
$rubbos_httpd rubbos-httpd
$rubbos_mysql1 rubbos-mysql1
$rubbos_tomcat1 rubbos-tomcat1
" >> /etc/hosts
}

set +x

