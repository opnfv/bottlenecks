#!/bin/bash
##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

usage="Script to run the tests in Bottlenecks.

usage:
    bash $(basename "$0") [-h|--help] [-s <test suite>] [-c <test case>] [--report] [--cleanup]

where:
    -h|--help         show the help text
    -s|--teststory    run specific test story
      <test story>        one of the following:
                              (rubbos, vstf, posca_factor_test)
                      user can also define their own test story and pass as var to this file,
                      please refer to testsuites/posca/testsuite_story/ for details
    -c|--testcase     run specific test case
      <test case>         one of the following:
                              (posca_factor_system_bandwidth, posca_factor_ping)
    --cleanup         cleanup test dockers runing when test is done (false by default)
    --report          push results to DB (false by default)

examples:
    $(basename "$0")
    $(basename "$0") -s posca_factor_test"

# Define global variables
Bottlenecks_key_dir="/home/opnfv/bottlenecks/utils/infra_setup"
POSCA_SUITE="/home/opnfv/bottlenecks/testsuites/posca"
POSCA_TESTCASE="/home/opnfv/bottlenecks/testsuites/posca/testcase_cfg"
POSCA_TESTSTORY="/home/opnfv/bottlenecks/testsuites/posca/testsuite_story"
BASEDIR=`dirname $0`

REPORT="False"
cleanup=false

# Define alias for log printing
info () {
    logger -s -t "bottlenecks.info" "$*"
}

error () {
    logger -s -t "bottlenecks.error" "$*"
    exit 1
}

# Define check_test function for test case/story list check
function check_test(){

    TEST_LEVEL="$1"
    TEST_NAME="$2"

    if [[ "${TEST_LEVEL}" == "testcase" ]]; then
        TEST_CONFIG="${POSCA_TESTCASE}"
    else
        if [[ "${TEST_LEVEL}" == "teststory" ]]; then
            TEST_CONFIG="${POSCA_TESTSTORY}"
        else
            info "Invalid name for test level: testcase or teststory"
        fi
    fi

    # Find all the test case yaml files first
    find $TEST_CONFIG -name "*yaml" > /tmp/all_tests.yaml
    all_tests_insuite=`cat /tmp/all_tests.yaml | awk -F '/' '{print $NF}' | awk -F '.' '{print $1}'`
    all_tests=(${all_tests_insuite})

    if [ "${TEST_NAME}" != "" ]; then
       TEST_EXEC=(${TEST_NAME// /})
       for i in "${TEST_EXEC[@]}"; do
           if [[ " ${all_tests[*]} " != *" $i "* ]]; then
               error "Unknown $TEST_LEVEL: $i. Available $TEST_LEVEL are: ${all_tests[@]}"
           fi
       done
       info "Tests to execute: ${TEST_NAME}."
    else
       error "Lack of $TEST_LEVEL name"
    fi
}

# Define run test function
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
        *)
            info "Composing up dockers"
            docker-compose -f /home/opnfv/bottlenecks/docker/bottleneck-compose/docker-compose.yml up -d
            info "Pulling tutum/influxdb for yardstick"
            docker pull tutum/influxdb:0.13
            sleep 5
            info "Running posca $test_level: $test_exec"
            docker exec bottleneckcompose_bottlenecks_1 python ${POSCA_SUITE}/../run_testsuite.py $test_level $test_exec $REPORT
        ;;
    esac
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
        -s|--teststory)
            teststory="$2"
            shift
        ;;
        -c|--testcase)
            testcase="$2"
            shift
        ;;
        --report)
            REPORT="True"
        ;;
        --cleanup)
            cleanup=true
        ;;
        *)
            echo "unkown option $1 $2"
            exit 1
        ;;
     esac
     shift
done

# Clean up related docker images
#bash ${BASEDIR}/docker/docker_cleanup.sh -d bottlenecks --debug
#bash ${BASEDIR}/docker/docker_cleanup.sh -d yardstick --debug
#bash ${BASEDIR}/docker/docker_cleanup.sh -d kibana --debug
#bash ${BASEDIR}/docker/docker_cleanup.sh -d elasticsearch --debug
#bash ${BASEDIR}/docker/docker_cleanup.sh -d influxdb --debug

# Run tests
if [ "${teststory}" != "" ]; then
    test_level="teststory"
    teststory_exec=(${teststory//,/ })
    check_test $test_level $teststory
    for i in "${teststory_exec[@]}"; do
        info "Start to run test story $i"
        run_test $i
    done
fi

if [ "${testcase}" != "" ]; then
    test_level="testcase"
    testcase_exec=(${testcase//,/ })
    check_test $test_level $testcase
    for i in "${testcase_exec[@]}"; do
        info "Start to run test case $i"
        run_test $i
    done
fi

# Clean up testing dockers
if [[ ${cleanup} == true ]]; then
    info "Cleaning up docker-compose images and dockers"
    docker-compose -f $BASEDIR/docker/bottleneck-compose/docker-compose.yml down --rmi all
    bash ${BASEDIR}/docker/docker_cleanup.sh -d influxdb --debug
    bash ${BASEDIR}/docker/docker_cleanup.sh -d bottlenecks --debug
fi
