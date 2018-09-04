#!/bin/bash

##############################################################################
# Copyright (c) 2016 Huawei Tech and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

# Run flake8, unit, coverage test

getopts ":f" FILE_OPTION
STYLE_CHECK_DIRS="testsuites/posca/ utils/ monitor/ test-scheduler/"

run_flake8() {
    echo "========================================="
    echo "Running flake8 for python style check:   "
    echo "-----------------------------------------"
    logfile=flake8_verify.log
    if [ $FILE_OPTION == "f" ]; then
       flake8 --append-config=flake8_cfg ${STYLE_CHECK_DIRS} > $logfile
    else
       flake8 --append-config=flake8_cfg ${STYLE_CHECK_DIRS}
    fi

    if [ $? -ne 0 ]; then
        echo "FAILED"
        if [ $FILE_OPTION == "f" ]; then
            echo "Results in $logfile"
        fi
        exit 1
    else
        echo "The patch has passed python style check  "
        echo "===================END==================="
    fi
}


run_nosetests() {
    echo "========================================="
    echo "Running unit and coverage test:          "
    echo "-----------------------------------------"
    nosetests --with-coverage --cover-tests \
        --cover-min-percentage 100 \
        test/__init__.py \
        testsuites/posca/__init__.py testsuites/__init__.py \
        testsuites/posca/testcase_cfg/__init__.py \
        testsuites/posca/testcase_dashboard/__init__.py \
        testsuites/posca/testcase_script/__init__.py \
        utils/__init__.py \
        utils/dashboard/__init__.py \
        utils/env_prepare/__init__.py \
        utils/infra_setup/__init__.py \
        monitor/__init__.py \
        monitor/dashboard/__init__.py \
        monitor/dispatch/__init__.py
    echo "===================END==================="

}


for((i=1;i<=1;i++));do echo -e "\n";done
run_flake8

for((i=1;i<=1;i++));do echo -e "\n";done
run_nosetests
