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
                              (apex, compass, fuel, joid)
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
        *)
            echo "unkown option $1 $2"
            exit 1
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

# Repo and configs
RELENG_REPO="/home/releng"
BOTTLENECKS_CONFIG=/tmp
OPENRC=${BOTTLENECKS_CONFIG}/admin_rc.sh
OS_CACERT=${BOTTLENECKS_CONFIG}/os_cacert


##############################################################################
# Preparing scripts for openstack and pod configs for OPNFV Installers
##############################################################################
# Define Variables
info "Downloading Releng fetch_os_creds script for openstack/pod configs of OPNFV installers"

[ -d ${RELENG_REPO} ] && rm -rf ${RELENG_REPO}
git clone https://gerrit.opnfv.org/gerrit/releng ${RELENG_REPO} >${redirect}

info "Downloading Yardstick for pod configs of OPNFV installers"
YARDSTICK_REPO="/home/yardstick"
[ -d ${YARDSTICK_REPO} ] && rm -rf ${YARDSTICK_REPO}
git clone https://gerrit.opnfv.org/gerrit/yardstick ${YARDSTICK_REPO} >${redirect}

# Preparing configuration files for testing
if [[ ${INSTALLER_TYPE} != "" ]]; then
    # Preparing OpenStack RC and Cacert files
    info "fetching os credentials from $INSTALLER_TYPE"
    if [[ $INSTALLER_TYPE == 'compass' ]]; then
        export BRANCH="master"
        INSTALLER_IP=192.168.200.2
        if [[ ${BRANCH} == 'master' ]]; then
            ${RELENG_REPO}/utils/fetch_os_creds.sh -d ${OPENRC} -i ${INSTALLER_TYPE} -a ${INSTALLER_IP} -o ${OS_CACERT} >${redirect}
        else
            ${RELENG_REPO}/utils/fetch_os_creds.sh -d ${OPENRC} -i ${INSTALLER_TYPE} -a ${INSTALLER_IP}  >${redirect}
        fi
    elif [[ $INSTALLER_TYPE == 'apex' ]]; then
        INSTALLER_IP=$(sudo virsh domifaddr undercloud | grep -Eo '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')
        ${RELENG_REPO}/utils/fetch_os_creds.sh -d ${OPENRC} -i ${INSTALLER_TYPE} -a ${INSTALLER_IP} -o ${OS_CACERT} >${redirect}
        echo ${cmd}
        ${cmd} 
    else
        error "The installer is not specified"
        exit 1
    fi

    # Finding and crearting POD description files from different deployments
    if [[ ${INSTALLER_TYPE} == 'compass' ]]; then
        cmd="sudo cp ${YARDSTICK_REPO}/etc/yardstick/nodes/compass_sclab_virtual/pod.yaml \
        ${BOTTLENECKS_CONFIG}"
        info ${cmd}
        ${cmd}
    elif [[ ${INSTALLER_TYPE} == 'apex' ]]; then
        options="-u stack -k /root/.ssh/id_rsa"
        INSTALLER_IP=$(/usr/sbin/arp -e | grep ${instack_mac} | awk {'print $1'})
        cmd="sudo python ${RELENG_REPO}/utils/create_pod_file.py -t ${INSTALLER_TYPE} \
         -i ${INSTALLER_IP} ${options} -f ${BOTTLENECKS_CONFIG}/pod.yaml"
        info ${cmd}
        ${cmd}
    fi


    ##############################################################################
    # Check the existence of the output configs for OPNFV Installers
    ##############################################################################
    # Checking the pod decription file
    if [ -f ${BOTTLENECKS_CONFIG}/pod.yaml ]; then
        info "FILE - ${BOTTLENECKS_CONFIG}/pod.yaml:"
        cat ${BOTTLENECKS_CONFIG}/pod.yaml
    else
        error "Cannot find file ${BOTTLENECKS_CONFIG}/pod.yaml. Please check if it is existing."
        sudo ls -al ${BOTTLENECKS_CONFIG}
    fi

    # Checking the openstack rc and os_cacert file
    if [[ -f ${OPENRC} ]]; then
        info "Opentack credentials path is ${OPENRC}"
        if [[ -f ${OS_CACERT} ]]; then
            info "Writing ${OS_CACERT} to ${OPENRC}"
            echo "export OS_CACERT=${OS_CACERT}" >> ${OPENRC}
            cat ${OPENRC}
        else
           error "Couldn't find openstack cacert file: ${OS_CACERT}, please check if the it's been properly provided."
       fi
    else
        error "Couldn't find openstack rc file: ${OPENRC}, please check if the it's been properly provided."
        exit 1
    fi    
fi
