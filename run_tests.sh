#!/bin/bash
##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

usage="Script to run the tests in bottlenecks auto.

usage:
    bash $(basename "$0") [-h|--help] [-s <test suite>]

where:
    -h|--help         show the help text
    -r|--report       push results to DB(true by default)
    -s|--suite        run specific test suite
      <test suite>    one of the following:
                            rubbos, vstf, posca

examples:
    $(basename "$0")
    $(basename "$0") -s posca"

report=true

arr_test_suite=(rubbos vstf posca)

Bottlenecks_key_dir="/home/opnfv/bottlenecks/utils/infra_setup"

function run_test(){

    test_suite=$1
    echo "Running test suite $test_suite"

    case $test_suite in
        "rubbos")
            info "After OPNFV Colorado release, Rubbos testsuite is not updating anymore.
This entrance for running Rubbos within Bottlenecks is no longer supported.
This testsuite is also not in the release plan with Bottlenecks since then.
If you want to run Rubbos, please refer to earlier releases.\n"
        ;;
        "vstf")
            info "After OPNFV Colorado release, VSTF testsuite is not updating anymore.
This entrance for running VSTF within Bottlenecks is no longer supported.
This testsuite is also not in the release plan with Bottlenecks since then.
If you want to run VSTF, please refer to earlier releases.\n"
        ;;
        "posca")
            POSCA_SCRIPT=/home/opnfv/bottlenecks/testsuites/posca
            TEST_CASE=posca_factor_system_bandwidth
            info "Composing up dockers"
            docker-compose -f /home/opnfv/bottlenecks/docker/bottleneck-compose/docker-compose.yml up -d
            info "Pulling tutum/influxdb for yardstick"
            docker pull tutum/influxdb:0.13
            info "Copying testing scripts to docker"
            docker cp /home/opnfv/bottlenecks/run_posca.sh bottleneckcompose_bottlenecks_1:/home/opnfv/bottlenecks
            sleep 5
            info "Running posca test suite with default testcase posca_stress_traffic"
            docker exec bottleneckcompose_bottlenecks_1 python ${POSCA_SCRIPT}/run_posca.py testcase $TEST_CASE
        ;;
    esac
}

while [[ $# > 0 ]]
    do
    key="$1"
    case $key in
        -h|--help)
            echo "$usage"
            exit 0
            shift
        ;;
        -r|--report)
            report="-r"
        ;;
        -s|--suite)
            SUITE="$2"
            shift
        ;;
        *)
            echo "unkown option $1 $2"
            exit 1
        ;;
     esac
     shift
done

BASEDIR=`dirname $0`
source ${BASEDIR}/common.sh

#Add random key generation
if [ ! -d $Bottlenecks_key_dir/bottlenecks_key ]; then
    mkdir $Bottlenecks_key_dir/bottlenecks_key
else
    rm -rf $Bottlenecks_key_dir/bottlenecks_key
    mkdir $Bottlenecks_key_dir/bottlenecks_key
fi
chmod 700 $Bottlenecks_key_dir/bottlenecks_key

ssh-keygen -t rsa -f $Bottlenecks_key_dir/bottlenecks_key/bottlenecks_key -q -N ""
chmod 600 $Bottlenecks_key_dir/bottlenecks_key/*

#check the test suite name is correct
if [ "${SUITE}" != "" ]; then
    suite_exec=(${SUITE//,/ })
    for i in "${suite_exec[@]}"; do
        if [[ " ${arr_test_suite[*]} " != *" $i "* ]]; then
            error "unkown test suite: $i"
        fi
    done
    info "Tests to execute: ${SUITE}"
fi

# Source credentials
info "Sourcing Credentials openstack.creds to run the tests.."
source /home/opnfv/bottlenecks/config/openstack.creds

#run tests
if [ "${SUITE}" != "" ]; then
    for i in "${suite_exec[@]}"; do
        run_test $i
    done
fi
