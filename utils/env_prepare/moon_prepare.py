#!/usr/bin/env python
##############################################################################
# Copyright (c) 2018 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import os
import subprocess
import utils.infra_setup.passwordless_SSH.ssh as localssh

def moon_envprepare(host_info):
    if host_info.has_key("password"):
        client = localssh.SSH(user=host_info["user"],
                              host=host_info["ip"],
                              password=host_info["password"])
    else:
        client = localssh.SSH(user=host_info["user"],
                              host=host_info["ip"],
                              key_filename=host_info["keyfile"])
    with open("/home/opnfv/bottlenecks/utils/env_prepare/moon_prepare.bash", "rb") as stdin_file:
        client.run("cat > ~/bottlenecks_envprepare.bash", stdin=stdin_file)
    client.execute("sudo bash ~/bottlenecks_envprepare.bash")
