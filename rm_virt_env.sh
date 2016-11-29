#!/bin/bash

##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

CLI_BASE="/home/opnfv/bottlenecks/"

# Logout the virtual enviroment
if [ ! -z ${VIRTUAL_ENV} ]; then
    deactivate
fi

# Delete the virtual enviroment
rm -rf $CLI_BASE/venv/

# Delete CLI python package
if [ -d $CLI_BASE/bottlenecks.egg-info ]; then
    rm -rf $CLI_BASE/bottlenecks.egg-info
fi

if [ -f $CLI_BASE/cli/bottlenecks_cli.pyc ]; then
    rm -f $CLI_BASE/cli/bottlenecks_cli.pyc
fi

if [ -f $CLI_BASE/cli/__init__.pyc ]; then
    rm -f $CLI_BASE/cli/__init__.pyc
fi

if [ -f $CLI_BASE/cli/command_group/testcase.pyc ]; then
    rm -f $CLI_BASE/cli/command_group/testcase.pyc
fi

if [ -f $CLI_BASE/cli/command_group/__init__.pyc ]; then
    rm -f $CLI_BASE/cli/command_group/__init__.pyc
fi

# Delete SSH key
if [ -d $CLI_BASE/utils/infra_setup/bottlenecks_key/ ]; then
    rm -rf $CLI_BASE/utils/infra_setup/bottlenecks_key/
fi
