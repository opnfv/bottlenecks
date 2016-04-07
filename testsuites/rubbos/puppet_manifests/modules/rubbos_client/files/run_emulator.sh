#!/bin/bash
##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

## Usage: run_emulator.sh
echo "==> Rubbos emulator start $(date)"

REPLACED_RUBBOS_APP_TOOLS/jdk1.6.0_27/bin/java -classpath .:REPLACED_RUBBOS_HOME/Client:REPLACED_RUBBOS_HOME/Client/rubbos_client.jar -Xms512m -Xmx2048m -Dhttp.keepAlive=true -Dhttp.maxConnections=1000000 edu.rice.rubbos.client.ClientEmulator

echo "==> Rubbos emulator end $(date)"
