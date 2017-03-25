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
    bash $(basename "$0") [-h|--help] [-s <test suite>] [-c <test case>]

where:
    -h|--help         show the help text
    -r|--report       push results to DB(true by default)
    -s|--teststory    run specific test story
      <test story>        one of the following:
                              (rubbos, vstf, posca_factor_test)
                      user can also define their own test story and pass as var to this file,
                      please refer to testsuites/posca/testsuite_story/ for details
    -c|--testcase     run specific test case
      <test case>         one of the following:
                              (posca_factor_system_bandwidth, posca_factor_ping)

examples:
    $(basename "$0")
    $(basename "$0") -s posca_factor_test"

Bottlenecks_key_dir="/home/opnfv/bottlenecks/utils/infra_setup"
POSCA_SCRIPT="/home/opnfv/bottlenecks/testsuites/posca"
SUITE_PREFIX="/home/opnfv/bottlenecks/testsuites/posca/testcase_cfg"

report=true

#TO-DO add auto-find for test story as for test case
all_test_story=(rubbos vstf posca_factor_test)

find $SUITE_PREFIX -name "*yaml" > /tmp/all_testcases.yaml
all_testcases_posca=`cat /tmp/all_testcases.yaml | awk -F '/' '{print $NF}' | awk -F '.' '{print $1}'`
all_test_case=(${all_testcases_posca})

function run_test(){

    test_exec=$1

    case $test_exec in
        "rubbos")
            info "After OPNFV Colorado release, Rubbos testsuite is not updating anymore.
                  This entrance for running Rubbos within Bottlenecks is no longer supported.
                  This testsuite is also not in the release plan with Bottlenecks since then.
                  If you want to run Rubbos, please refer to earlier releases."
        ;;
        "vstf")
            info "After OPNFV Colorado release, VSTF testsuite is not updating anymore.
                  This entrance for running VSTF within Bottlenecks is no longer supported.
                  This testsuite is also not in the release plan with Bottlenecks since then.
                  If you want to run VSTF, please refer to earlier releases."
        ;;
        "posca_factor_test")
            info "Composing up dockers"
            docker-compose -f /home/opnfv/bottlenecks/docker/bottleneck-compose/docker-compose.yml up -d
            info "Pulling tutum/influxdb for yardstick"
            docker pull tutum/influxdb:0.13
#            info "Copying testing scripts to docker"
#            docker cp /home/opnfv/bottlenecks/run_posca.sh bottleneckcompose_bottlenecks_1:/home/opnfv/bottlenecks
            sleep 5
            info "Running posca test story: $test_exec"
            docker exec bottleneckcompose_bottlenecks_1 python ${POSCA_SCRIPT}/run_posca.py teststory $test_exec
        ;;
        *)
            info "Composing up dockers"
            docker-compose -f /home/opnfv/bottlenecks/docker/bottleneck-compose/docker-compose.yml up -d
            info "Pulling tutum/influxdb for yardstick"
            docker pull tutum/influxdb:0.13
#            info "Copying testing scripts to docker"
#            docker cp /home/opnfv/bottlenecks/run_posca.sh bottleneckcompose_bottlenecks_1:/home/opnfv/bottlenecks
            sleep 5
            info "Running posca test story: $test_exec"
            docker exec bottleneckcompose_bottlenecks_1 python ${POSCA_SCRIPT}/run_posca.py $test_level $test_exec
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
        -s|--teststory)
            teststory="$2"
            shift
        ;;
        -c|--testcase)
            testcase="$2"
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
if [ "${teststory}" != "" ]; then
    teststory_exec=(${teststory//,/ })
    for i in "${teststory_exec[@]}"; do
        if [[ " ${all_test_story[*]} " != *" $i "* ]]; then
            error "Unkown test story: $i"
        fi
    done
fi

#check the test case name is correct
if [ "${testcase}" != "" ]; then
    testcase_exec=(${testcase//,/ })
    for i in "${testcase_exec[@]}"; do
        if [[ " ${all_test_case[*]} " != *" $i "* ]]; then
            error "Unkown test case: $i"
        fi
    done
fi

#run tests
if [ "${teststory}" != "" ]; then
    test_level="teststory"
    for i in "${teststory_exec[@]}"; do
        info "Start to run test story $i"
        run_test $i
    done
fi

if [ "${testcase}" != "" ]; then
    test_level="testcase"
    for i in "${testcase_exec[@]}"; do
        info "Start to run test case $i"
        run_test $i
    done
fi