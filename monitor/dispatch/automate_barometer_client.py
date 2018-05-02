##############################################################################
# Copyright (c) 2018 Huawei Tech and others.
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
barometer_client_install_sh =\
    "/home/opnfv/bottlenecks/monitor/barometer_install_client.sh"
barometer_client_install_conf =\
    "/home/opnfv/bottlenecks/monitor/barometer_client.conf"

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
                    "cd /etc && mkdir barometer_config"
                )
                if status:
                    raise Exception("Command failed with non-zero status.")
                    logger.info(stdout.splitlines())
                with open(barometer_client_install_conf) as stdin_file:
                    ssh_d.run("cat > /etc/barometer_config/\
                        barometer_client.conf",
                              stdin=stdin_file)
                with open(barometer_client_install_sh) as stdin_file:
                    ssh_d.run("cat > /etc/barometer_config/install.sh",
                              stdin=stdin_file)

                ssh_d.run("cd /etc/barometer_config/ && bash ./install.sh")
