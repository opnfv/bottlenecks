##############################################################################
# Copyright (c) 2017 Huawei Tech and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import logging
import yaml
import utils.infra_setup.passwordless_SSH.ssh as ssh

logger = logging.getLogger(__name__)
collectd_client_install_sh =\
    "/home/opnfv/bottlenecks/monitor/dispatch/install_collectd_client.sh"
collectd_client_install_conf =\
    "/home/opnfv/bottlenecks/monitor/config/collectd_client.conf"

with open('/tmp/pod.yaml') as f:
    dataMap = yaml.safe_load(f)
    for x in dataMap:
        for y in dataMap[x]:
            if (y['role'] == 'Controller') or (y['role'] == 'Compute'):
                ip = str(y['ip'])
                user = str(y['user'])
                pwd = str(y['password'])
                ssh_d = ssh.SSH(user, host=ip, password=pwd)
                status, stdout, stderr = ssh_d.execute(
                    "cd /etc && mkdir collectd_config"
                )
                if status:
                    print Exception(
                        "Command: \"mkdir collectd_config\" failed.")
                    logger.info(stdout.splitlines())
                with open(collectd_client_install_sh) as stdin_file:
                    ssh_d.run("cat > /etc/collectd_config/install.sh",
                              stdin=stdin_file)
                with open(collectd_client_install_conf) as stdin_file:
                    ssh_d.run(
                        "cat > /etc/collectd_config/collectd_client.conf",
                        stdin=stdin_file
                    )
                status, stdout, stderr = ssh_d.execute(
                    "sudo apt-get install -y docker.io"
                )
                if status:
                    raise Exception("Command for installing docker failed.")
                    logger.info(stdout.splitlines())
                ssh_d.run("cd /etc/collectd_config/ && bash ./install.sh")