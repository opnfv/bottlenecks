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

run_flake8() {
    echo "Running flake8 ... "
    logfile=test_results.log
    if [ $FILE_OPTION == "f" ]; then
        flake8 ../bottlenecks > $logfile
    else
        flake8 ../bottlenecks
    fi

    if [ $? -ne 0 ]; then
        echo "FAILED"
        if [ $FILE_OPTION == "f" ]; then
            echo "Results in $logfile"
        fi
        exit 1
    else
        echo "OK"
    fi
}

run_tests() {
    echo "Running unittest ... "
    #will add future
}

run_coverage() {
    echo "Running coverage ..."
    #source tests/ci/cover.sh
    #run_coverage_test
    #will add future
}

run_flake8
run_tests
run_coverage
