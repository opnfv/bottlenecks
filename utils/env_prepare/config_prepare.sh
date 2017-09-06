#!/bin/bash
##############################################################################
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

# This file is to prepare the openstack certs and pod description that required
# for Bottlenecks tests.
usage="Script to prepare the configurations before testing.

usage:
    bash $(basename "$0") [-h|--help] [-i <installer>] [--debug]

where:
    -h|--help         show the help text
    -i|--installer    input the name of the installer
      <installer>         one of the following:
                              (compass, fuel, joid, apex)
    --debug
                      debug option switch
examples:
    $(basename "$0") -i compass"

# Debug option
redirect="/dev/null"

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
        --debug)
            redirect="/dev/stdout"
            shift
        ;;
    esac
    shift
done

# Define alias for log printing
info () {
    logger -s -t "BOTTLENECKS INFO" "$*"
}

error () {
    logger -s -t "BOTTLENECKS ERROR" "$*"
    exit 1
}

# Define Variables
echo "BOTTLENECKS INFO: Downloading Releng"
RELENG_REPO="/home/releng"
[ -d ${RELENG_REPO} ] && rm -rf ${RELENG_REPO}
git clone https://gerrit.opnfv.org/gerrit/releng ${RELENG_REPO} >${redirect}

echo "BOTTLENECKS INFO: Downloading Yardstick"
YARDSTICK_REPO="/home/yardstick"
[ -d ${YARDSTICK_REPO} ] && rm -rf ${YARDSTICK_REPO}
git clone https://gerrit.opnfv.org/gerrit/yardstick ${YARDSTICK_REPO} >${redirect}

BOTTLENECKS_CONFIG=/tmp

OPENRC=${BOTTLENECKS_CONFIG}/admin_rc.sh
OS_CACERT=${BOTTLENECKS_CONFIG}/os_cacert

# Preparing configuration files for testing
if [[ ${INSTALLER_TYPE} != "" ]]; then
    # Preparing OpenStack RC and Cacert files
    info "fetching os credentials from $INSTALLER_TYPE"
    if [[ $INSTALLER_TYPE == 'compass' ]]; then
        export BRANCH="master"
        INSTALLER_IP=192.168.200.2
        if [[ ${BRANCH} == 'master' ]]; then
            ${RELENG_REPO}/utils/fetch_os_creds.sh -d ${OPENRC} -i ${INSTALLER_TYPE} -a ${INSTALLER_IP} -o ${OS_CACERT} >${redirect}
            if [[ -f ${OS_CACERT} ]]; then
                echo "BOTTLENECKS INFO: successfully fetching os_cacert for openstack: ${OS_CACERT}"
            else
                echo "BOTTLENECKS ERROR: couldn't find os_cacert file: ${OS_CACERT}, please check if the it's been properly provided."
                exit 1
            fi
        else
            ${RELENG_REPO}/utils/fetch_os_creds.sh -d ${OPENRC} -i ${INSTALLER_TYPE} -a ${INSTALLER_IP}  >${redirect}
        fi
    else
        error "The isntaller is not specified"
        exit 1
    fi

    if [[ -f ${OPENRC} ]]; then
        echo "BOTTLENECKS INFO: openstack credentials path is ${OPENRC}"
        if [[ $INSTALLER_TYPE == 'compass' && ${BRANCH} == 'master' ]]; then
            echo "BOTTLENECKS INFO: writing ${OS_CACERT} to ${OPENRC}"
            echo "export OS_CACERT=${OS_CACERT}" >> ${OPENRC}
        fi
        cat ${OPENRC}
    else
        echo "BOTTLENECKS ERROR: couldn't find openstack rc file: ${OPENRC}, please check if the it's been properly provided."
        exit 1
    fi

    # Finding and crearting POD description files from different deployments
    ssh_options="-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"

    if [ "$INSTALLER_TYPE" == "fuel" ]; then
        echo "Fetching id_rsa file from jump_server $INSTALLER_IP..."
        sshpass -p r00tme sudo scp $ssh_options root@${INSTALLER_IP}:~/.ssh/id_rsa ${BOTTLENECKS_CONFIG}/id_rsa
    fi

    if [ "$INSTALLER_TYPE" == "apex" ]; then
        echo "Fetching id_rsa file from jump_server $INSTALLER_IP..."
        sudo scp $ssh_options stack@${INSTALLER_IP}:~/.ssh/id_rsa ${BOTTLENECKS_CONFIG}/id_rsa
    fi

    if [[ ${INSTALLER_TYPE} == compass ]]; then
        options="-u root -p root"
    elif [[ ${INSTALLER_TYPE} == fuel ]]; then
        options="-u root -p r00tme"
    elif [[ ${INSTALLER_TYPE} == apex ]]; then
        options="-u stack -k /root/.ssh/id_rsa"
    else
        echo "Don't support to generate pod.yaml on ${INSTALLER_TYPE} currently."
    fi

    if [[ ${INSTALLER_TYPE} != compass ]]; then
        cmd="sudo python ${RELENG_REPO}/utils/create_pod_file.py -t ${INSTALLER_TYPE} \
         -i ${INSTALLER_IP} ${options} -f ${BOTTLENECKS_CONFIG}/pod.yaml \
         -s ${BOTTLENECKS_CONFIG}/id_rsa"
        echo ${cmd}
        ${cmd}
    else
        cmd="sudo cp ${YARDSTICK_REPO}/etc/yardstick/nodes/compass_sclab_virtual/pod.yaml \
        ${BOTTLENECKS_CONFIG}"
        echo ${cmd}
        ${cmd}
    fi

    if [ -f ${BOTTLENECKS_CONFIG}/pod.yaml ]; then
        echo "FILE: ${BOTTLENECKS_CONFIG}/pod.yaml:"
        cat ${BOTTLENECKS_CONFIG}/pod.yaml
    else
        echo "ERROR: cannot find file ${BOTTLENECKS_CONFIG}/pod.yaml. Please check if it is existing."
        sudo ls -al ${BOTTLENECKS_CONFIG}
    fi
fi
