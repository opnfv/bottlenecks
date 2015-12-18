#!/bin/bash
###############################################################################
# Copyright (c) 2015 Huawei Tech.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

set -e

RELENG_REPO=https://gerrit.opnfv.org/gerrit/releng
RELENG_REPO_DIR=/home/opnfv/repos/releng
RELENG_BRANCH=master # branch, tag, sha1 or refspec

INSTALLER_TYPE=fuel
INSTALLER_IP=10.20.0.2

POD_NAME=opnfv-jump-2
EXTERNAL_NET=net04_ext

echo "INFO: Creating openstack credentials .."

# Create openstack credentials
$RELENG_REPO_DIR/utils/fetch_os_creds.sh \
    -d /tmp/openrc \
    -i ${INSTALLER_TYPE} -a ${INSTALLER_IP}

source /tmp/openrc

# FIXME: Temporary OPNFV playground hack
if [ "$INSTALLER_TYPE" == "fuel" ]; then
    ssh_opts="-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
    if sshpass -p r00tme ssh 2>/dev/null $ssh_opts root@${INSTALLER_IP} \
        fuel environment --env 1 | grep opnfv-virt; then
        echo "INFO: applying OPNFV playground hack"
        export OS_ENDPOINT_TYPE='publicURL'
    fi
fi

export EXTERNAL_NET INSTALLER_TYPE POD_NAME
