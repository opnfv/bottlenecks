#!/bin/bash
###############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
BASEDIR=`dirname $0`
source ${BASEDIR}/../common.sh

info "============ Preparing bottlenecks environment ==========="

# definition of available installer names
INSTALLERS=(fuel compass apex joid)

if [ ! -f ${BOTTLENECKS_REPO_DIR}/config/openstack.creds ]; then
    # If credentials file is not given, check if environment variables are set
    # to get the creds using fetch_os_creds.sh later on
    info "Checking environment variables INSTALLER_TYPE and INSTALLER_IP"
    if [ -z ${INSTALLER_TYPE} ]; then
        error "Environment variable 'INSTALLER_TYPE' is not defined."
    elif [[ ${INSTALLERS[@]} =~ ${INSTALLER_TYPE} ]]; then
        info "INSTALLER_TYPE env variable found: ${INSTALLER_TYPE}"
    else
        error "Invalid environment variable INSTALLER_TYPE=${INSTALLER_TYPE}"
    fi

    if [ -z ${INSTALLER_IP} ]; then
        error "Environment variable 'INSTALLER_IP' is not defined."
    fi
    info "INSTALLER_IP env variable found: ${INSTALLER_IP}"
fi

# Create Openstack credentials file
# $creds is an env varialbe in the docker container pointing to
# /home/opnfv/bottlenecks/config/openstack.creds
if [ ! -f ${creds} ]; then
    ${REPOS_DIR}/releng/utils/fetch_os_creds.sh -d ${creds} \
        -i ${INSTALLER_TYPE} -a ${INSTALLER_IP}
    retval=$?
    if [ $retval != 0 ]; then
        error "Cannot retrieve credentials file from installation. Check logs."
        exit $retval
    fi
else
    info "OpenStack credentials file given to the docker"
fi

# If we use SSL, by default use option OS_INSECURE=true which means that
# the cacert will be self-signed
if grep -Fq "OS_CACERT" ${creds}; then
    echo "OS_INSECURE=true">>${creds};
fi

# Source credentials
source ${creds}
