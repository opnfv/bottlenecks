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

SCRIPT_DIR=`cd ${BASH_SOURCE[0]%/*};pwd`
export BOTTLENECKS_TOP_DIR=$SCRIPT_DIR/../
export GERRIT_REFSPEC_DEBUG=$1

$SCRIPT_DIR/rubbos_docker_run.sh

set +ex

