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
                            rubbos, vstf

examples:
    $(basename "$0")
    $(basename "$0") -s rubbos"

report=true

arr_test_suite=(rubbos vstf)

function check_testcase(){

    check_suite="$1"
    case $check_suite in
         "-rubbos")
             $SUITE_PREFIX=$SUITE_PREFIX_CONFIG/rubbos/testcase_cfg
         ;;
         "-vstf")
             $SUITE_PREFIX=$SUITE_PREFIX_CONFIG/vstf/testcase_cfg
         ;;
    esac

    TEST_CASE=$2

    #find all the test case yaml files first
    find $SUITE_PREFIX -name "*yaml" > /tmp/all_testcases.yaml
    all_testcases_insuite=`cat /tmp/all_testcases.yaml | awk -F '/' '{print $NF}' | awk -F '.' '{print $1}'`
    all_testcases=(${all_testcases_insuite})

    if ["${TEST_CASE}" != ""]; then
       testcase_exec=(${TEST_CASE// /})
       for i in "${testcase_exec[@]}"; do
           if [[ " ${all_test_cases[*]} " != *" $i "* ]]; then
               error "unknown test case: $i. available test cases are: ${all_test_cases[@]}"
           fi
       done
       info "tests to execute: ${TEST_CASE}."
    else
       error "lack of testcase name"
    fi
}
function run_test(){

    test_suite=$1
    echo "Running test suite $test_suite"

    case $test_suite in
        "rubbos")
            info "Running rubbos test suite"
            test_file="/home/opnfv/bottlenecks/testsuite/rubbos/testsuite_story/rubbos_story1"
            if [[ -f $test_file ]]; then
                testcases=($(cat $test_file))
            else
                error("no rubbos test suite file ")
            fi
            for i in "${testcases[@]}"; do
                #check if the testcase is legal or not
                check_testcase -rubbos $i
                #adjust config parameters, different test suite has different methods, take rubbos as an example
                #run test case, different test suite has different methods

            done
        ;;
        "vstf")
            info "Running vstf test suite"
            test_file="/home/opnfv/bottlenecks/testsuite/vstf/testsuite_story/vstf_story1"
            if [[ -f $test_file ]]; then
                testcases=($(cat $test_file))
            else
                error("no vstf test suite file ")
            fi
            for i in "${testcases[@]}"; do
                #check if the testcase is legal or not
                check_testcase -vstf $i
                #adjust config parameters
                #run test case
            done
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

#run tests
if [ "${SUITE}" != "" ]; then
    for i in "${suite_exec[@]}"; do
        run_test $i
    done
fi
