#!/bin/bash

##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

# Install Python virtual enviroment
sudo -H  pip install virtualenv

# Create virtual enviroment
virtualenv venv

# Activate and login the virtual enviroment
. venv/bin/activate

# Install Bottlencks CLI
pip install --editable .

if [ -z $VIRTUAL_ENV ]; then
    echo "Virtual enviroment is incorrectly configured!"
    deactivate
fi
