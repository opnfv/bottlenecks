#!/bin/bash
##############################################################################
# Copyright (c) 2018 Huawei Tech and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
K8S_CONFIG="/tmp/k8s_config"

usage="Script to prepare kubenetes test configurations.

usage:
    bash $(basename "$0") [-h|--help] [-i|--installer <installer typer>] [-c|--config <k8s config>]

where:
    -h|--help         show the help text
    -i|--installer    specify the installer for the system to be monitored
      <installer type>
                      one of the following:
                              (compass)
examples:
    $(basename "$0") -i compass"


info () {
    logger -s -t "BOTTLENECKS INFO" "$*"
}

error () {
    logger -s -t "BOTTLENECKS ERROR" "$*"
    exit 1
}

# Process input variables
while [[ $# > 0 ]]
    do
    key="$1"
    case $key in
        -h|--help)
            echo "$usage"
            exit 0
            shift
        ;;
        -i|--installer)
            INSTALLER_TYPE="$2"
            shift
        ;;
        -c|--config)
            K8S_CONFIG="$2"
            shift
        ;;
        *)
            error "unkown input options $1 $2"
            exit 1
        ;;
     esac
     shift
done

if [[  ${INSTALLER_TYPE} == 'compass' ]]; then
    sshpass -p root scp root@192.16.1.222:~/.kube/config ${K8S_CONFIG}
else
    echo "BOTTLENECKS EROOR: unrecognized installer"
fi

if [[ -f ${K8S_CONFIG} ]]; then
    if [[ -d ~/.kube ]]; then
        cp ${K8S_CONFIG} ~/.kube/config
        echo "BOTTLENECKS INFO: copying k8s config to ~./kube"
    else
        mkdir ~/.kube
        cp ${K8S_CONFIG} ~/.kube/config
        echo "BOTTLENECKS INFO: copying k8s config to ~./kube"
    fi
else
    echo "BOTTLENECKS ERROR: k8s config file does no exit (${K8S_CONFIG})"
    exit 1
fi
