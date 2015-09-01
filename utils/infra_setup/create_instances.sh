##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
# matthew.lijun@huawei.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

#! /usr/bin/env bash

set -e

THIS_DIR=`pwd`

OPENRC_PATH=/opt/
CREATE_INSTANCE_PATH=$THIS_DIR

INSTANCE_NUM=3
NET_ID=531c4557-7349-4984-8d5e-cceebb77205f
FLAVOR_TYPE=m1.small
IMAGE_ID=7c2f3e2b-cf6e-44ed-83ac-e87712167f9e
SEC_GROUP=default
INSTANCE_NAME=example_

source $OPENRC_PATH/admin-openrc.sh
cd $CREATE_INSTANCE_PATH
for((count=1;count<=$INSTANCE_NUM;count++))
do
   INSTANCE_NAME_TMP=${INSTANCE_NAME}${count}
   nova boot --nic net-id=${NET_ID} --flavor=${FLAVOR_TYPE} --image=${IMAGE_ID} --security_group=${SEC_GROUP} ${INSTANCE_NAME_TMP}
done
