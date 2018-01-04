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
    echo "Running flake8 for python style check... "
    logfile=flake8_verify.log
    if [ $FILE_OPTION == "f" ]; then
       flake8 --append-config=flake8_cfg testsuites/posca/ utils/ > $logfile
    else
       flake8 --append-config=flake8_cfg testsuites/posca/ utils/
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

run_nosetests() {
    echo "Running unit and coverage test ... "
    nosetests --with-coverage --cover-tests \
        --cover-min-percentage 100 \
        test/
}


run_flake8
run_nosetests
