#!/bin/bash
##############################################################################
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

function check_testcase(){

    check_suite="$1"
    SUITE_PREFIX="/home/opnfv/bottlenecks/testsuites/posca/testcase_cfg"

    TEST_CASE=$2

    #find all the test case yaml files first
    find $SUITE_PREFIX -name "*yaml" > /tmp/all_testcases.yaml
    all_testcases_insuite=`cat /tmp/all_testcases.yaml | awk -F '/' '{print $NF}' | awk -F '.' '{print $1}'`
    all_testcases=(${all_testcases_insuite})

    if [ "${TEST_CASE}" != "" ]; then
       testcase_exec=(${TEST_CASE// /})
       for i in "${testcase_exec[@]}"; do
           if [[ " ${all_testcases[*]} " != *" $i "* ]]; then
               error "unknown test case: $i. available test cases are: ${all_test_cases[@]}"
           fi
       done
       info "tests to execute: ${TEST_CASE}."
    else
       error "lack of testcase name"
    fi
}

SUITE_PREFIX="/home/opnfv/bottlenecks/testsuites/posca/testcase_cfg"
source /home/opnfv/bottlenecks/common.sh
test_file="/home/opnfv/bottlenecks/testsuites/posca/testsuite_story/posca_factor_test"
if [[ -f $test_file ]]; then
    testcases=($(cat $test_file))
else
    error "no posca test suite file "
fi

for i in "${testcases[@]}"; do
    #check if the testcase is legal or not
    check_testcase -posca $i
    #adjust config parameters
    #run test case
    file=${SUITE_PREFIX}/${i}.yaml
    python /home/opnfv/bottlenecks/testsuites/posca/run_posca.py -c ${i}
done