#!/bin/bash
###############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

usage="Script to run the tests in rubbos.

usage:
    bash $(basename "$0") [-h|--help] [-s <test suite>]

where:
    -h|--help         show the help text
    -t|--test         run specifif test case scenario
      <test case>     examples:
                               rubbos_1-1-1, rubbos_1-2-1

examples:
    $(basename "$0")
    $(basename "$0") -t rubbos_1-1-1"

while [[ $# > 0 ]]
    do
    key="$1"
    case $key in
        -h|--help)
            echo "$usage"
            exit 0
            shift
        ;;
        -t|--test)
            CASE="$2"
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

#has been checked in upper layer run_tests.sh
#run tests
if [ "${CASE}" != "" ]; then
    case_exec=(${CASE//,/})
    for case_exe in "${case_exec[@]}"; do
        client_num=4
        tomcat_num=$(echo "$case_exe"| awk -F '-' '{print $2}')
        mysql_num=$(echo "$case_exe"| awk -F '-' '{print $3')

        hosts=(rubbos_control rubbos_benchmark rubbos_httpd)
        for((i=1; i <= client_num; i++)); do
             hosts=(${hosts[*]} client$i)
        done
        for((i=1; i <= tomcat_num; i++)); do
             hosts=(${hosts[*]} tomcat$i)
        done
        for((i=1; i <= mysql_num; i++)); do
             hosts=(${hosts[*]} mysql$i)
        done
        bash $BOTTLENECKS_TOP_DIR/utils/infra_setup/heat_template/rubbos_heat_template/HOT_create_instance.sh
    done
fi
