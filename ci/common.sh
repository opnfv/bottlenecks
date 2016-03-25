#!/bin/bash
##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

mkdir -p /home/opnfv/bottlenecks/config
config_file=/home/opnfv/bottlenecks/config/bottlenecks_cfg.yaml

if [ ! -f ${config_file} ]; then
    default_config_file=$(find /home/opnfv/repos -name bottlenecks_cfg.yaml)
    cp $default_config_file $config_file
    echo "bottlenecks_cfg.yaml not provided. Using default one"
fi

SUITE_PREFIX_CONFIG=$(cat $config_file | grep -w suite_prefix_config | awk 'END {print $NF}')

info () {
    logger -s -t "bottlenecks.info" "$*"
}

error () {
    logger -s -t "bottlenecks.error" "$*"
    exit 1
}
