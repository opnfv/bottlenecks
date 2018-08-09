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
import os
import utils.infra_setup.passwordless_SSH.ssh as ssh

LOG = logging.getLogger(__name__)
DEL_DOCKER_SCRIPT = "/home/opnfv/bottlenecks/docker/docker_cleanup.sh"


def ssh_del_docker(docker_name):
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
                        "cd /etc"
                    )
                    with open(DEL_DOCKER_SCRIPT) as stdin_file:
                        ssh_d.run("cat > /etc/docker_cleanup.sh",
                                  stdin=stdin_file)

                    ssh_d.run("cd /etc/ && bash ./docker_cleanup.sh -d " +
                              docker_name)


def local_del_docker(docker_name):
        os.system('bash ' + DEL_DOCKER_SCRIPT + ' -d ' + docker_name)


ssh_del_docker('cadvisor')
ssh_del_docker('barometer')

local_del_docker('prometheus')
local_del_docker('cadvisor')
local_del_docker('barometer')
local_del_docker('grafana')
local_del_docker('collectd')
local_del_docker('openstack-exporter')

