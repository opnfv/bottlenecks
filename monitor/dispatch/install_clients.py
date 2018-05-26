##############################################################################
# Copyright (c) 2018 Huawei Tech and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
'''
Currently supported installers are Apex, Compass...
Supported monitoring tools are Cadvisor, Collectd, Barometer...
Carefully, do not change the path or name of the configuration files which
are hard coded for docker volume mapping.
'''
import os
import logging
import yaml
import utils.infra_setup.passwordless_SSH.ssh as ssh
import argparse

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='Monitoring Clients Dispatcher')
parser.add_argument("-i", "--INSTALLER_TYPE",
                    help="The installer for the system under monitoring")
# Barometer config and installation files
# /home/opnfv/bottlenecks/monitor/dispatch/install_barometer_client.sh
# /home/opnfv/bottlenecks/monitor/config/barometer_client.conf
# Cadvisor installation file
# /home/opnfv/bottlenecks/monitor/dispatch/install_cadvisor_client.sh
# Collectd config and installation files
# /home/opnfv/bottlenecks/monitor/dispatch/install_collectd_client.sh
# /home/opnfv/bottlenecks/monitor/config/collectd_client.conf
parser.add_argument("-s", "--INSTALlATION_SCRIPT",
                    help="The path of the script to install monitoring script")
parser.add_argument("-c", "--CLIENT_CONFIG", default="",
                    help="The path of the config of monitoring client")
parser.add_argument("-p", "--POD_DISCRIPTOR", default="/tmp/pod.yaml",
                    help="The path of pod discrition file")
args = parser.parse_args()

INSTALLERS = ['apex', 'compass']
if args.INSTALLER_TYPE not in INSTALLERS:
    raise Exception("The installer is not supported.")
if not args.INSTALlATION_SCRIPT:
    raise Exception("Must specify the client installation script path!")

if "barometer" in args.INSTALlATION_SCRIPT.lower():
    CONFIG_FILE = "/etc/barometer_config/barometer_client.conf"
    CONFIG_DIR = "barometer_config"
    INSTALlATION_SCRIPT = "/etc/barometer_config/install.sh"
elif "collectd" in args.INSTALlATION_SCRIPT.lower():
    CONFIG_FILE = "/etc/collectd_config/collectd_client.conf"
    CONFIG_DIR = "collectd_config"
    INSTALlATION_SCRIPT = "/etc/collectd_config/install.sh"
elif "cadvisor" in args.INSTALlATION_SCRIPT.lower():
    CONFIG_DIR = "cadvisor_config"
    INSTALlATION_SCRIPT = "/etc/cadvisor_config/install.sh"
else:
    raise Exception("The monitor client is not supported")


def main():
    with open(args.POD_DISCRIPTOR) as f:
        dataMap = yaml.safe_load(f)
        for x in dataMap:
            for y in dataMap[x]:
                if (y['role'].lower() == 'controller') or (
                        y['role'].lower() == 'compute'):
                    ip = str(y['ip'])
                    user = str(y['user'])
                    pwd = str(y['password'])

                    ssh_d = ssh.SSH(user, host=ip, password=pwd)
                    status, stdout, stderr = ssh_d.execute(
                        "cd /etc && mkdir " + CONFIG_DIR
                    )
                    if status:
                        print Exception(
                            "Command: \"mkdir {}\".format(CONFIG_DIR) failed.")
                        logger.info(stdout.splitlines())
                    if args.CLIENT_CONFIG:
                        with open(args.CLIENT_CONFIG) as stdin_file:
                            ssh_d.run("cat > " + CONFIG_FILE,
                                      stdin=stdin_file)
                    with open(args.INSTALlATION_SCRIPT) as stdin_file:
                        ssh_d.run("cat > " + INSTALlATION_SCRIPT,
                                  stdin=stdin_file)

                    for u in os.uname():
                        if 'ubuntu' in u.lower():
                            NODE_OS = 'ubuntu'
                            break
                    if NODE_OS == 'ubuntu':
                        status, stdout, stderr = ssh_d.execute(
                            "sudo apt-get install -y docker.io"
                        )
                    else:
                        status, stdout, stderr = ssh_d.execute(
                            "sudo yum install -y docker-io"
                        )
                    if status:
                        raise Exception(
                            "Command for installing docker failed.")
                        logger.info(stdout.splitlines())

                    ssh_d.run(
                        "cd /etc/{}/ && bash ./install.sh".format(CONFIG_DIR)
                    )


if __name__ == '__main__':
    main()
