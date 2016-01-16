#!/bin/bash
##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

set -ex

BOTTLENECKS_REPO=https://gerrit.opnfv.org/gerrit/bottlenecks

SCRIPT_DIR=`cd ${BASH_SOURCE[0]%/*};pwd`
GERRIT_REFSPEC_DEBUG=$1

if [ x"$GERRIT_REFSPEC_DEBUG" != x ]; then
    git fetch $BOTTLENECKS_REPO $GERRIT_REFSPEC_DEBUG && git checkout FETCH_HEAD
fi

cd $SCRIPT_DIR/../utils/infra_setup/heat_template/vstf_heat_template/
./vstf_HOT_create_instance.sh $GERRIT_REFSPEC_DEBUG
cd -

set +ex
