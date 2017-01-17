#!/bin/bash
##############################################################################
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
# bottlenecks: this file is copied from yardstick and slightly modified
##############################################################################

# installs required packages
# must be run from inside the image (either chrooted or running)

set -ex

if [ $# -eq 1 ]; then
    nameserver_ip=$1

    # /etc/resolv.conf is a symbolic link to /run, restore at end
    rm /etc/resolv.conf
    echo "nameserver $nameserver_ip" > /etc/resolv.conf
    echo "nameserver 8.8.8.8" >> /etc/resolv.conf
    echo "nameserver 8.8.4.4" >> /etc/resolv.conf
fi

# Add hostname to /etc/hosts.
# Allow console access via pwd
cat <<EOF >/etc/cloud/cloud.cfg.d/10_etc_hosts.cfg
manage_etc_hosts: True
password: RANDOM
chpasswd: { expire: False }
ssh_pwauth: True
EOF

#install some software
apt-get update
apt-get install -y \
    netperf \
    sysstat

# restore symlink
ln -sf /run/resolvconf/resolv.conf /etc/resolv.conf
