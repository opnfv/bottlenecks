#!/usr/bin/env python
##############################################################################
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import os
import subprocess
import utils.parser as config_parser
import errno
from utils.logger import Logger
import utils.infra_setup.heat.manager as utils

LOG = Logger(__name__).getLogger()
config = config_parser.Parser()


def _prepare_env_daemon():

    installer_ip = os.environ.get('INSTALLER_IP', 'undefined')
    installer_type = os.environ.get('INSTALLER_TYPE', 'undefined')

    rc_file = config.OPENSTACK_RC_FILE

    _get_remote_rc_file(rc_file, installer_ip, installer_type)

    _source_file(rc_file)

    _append_external_network(rc_file)

    # update the external_network
    _source_file(rc_file)


def _get_remote_rc_file(rc_file, installer_ip, installer_type):

    os_fetch_script = os.path.join(config.RELENG_DIR, config.OS_FETCH_SCRIPT)

    try:
        cmd = [os_fetch_script, '-d', rc_file, '-i', installer_type,
               '-a', installer_ip]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        p.communicate()[0]

        if p.returncode != 0:
            LOG.debug('Failed to fetch credentials from installer')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def _source_file(rc_file):
    p = subprocess.Popen(". %s; env" % rc_file, stdout=subprocess.PIPE,
                         shell=True)
    output = p.communicate()[0]
    env = dict((line.split('=', 1) for line in output.splitlines()))
    os.environ.update(env)
    return env


def _append_external_network(rc_file):
    neutron_client = utils._get_neutron_client()
    networks = neutron_client.list_networks()['networks']
    try:
        ext_network = next(n['name'] for n in networks if n['router:external'])
    except StopIteration:
        LOG.warning("Can't find external network")
    else:
        cmd = 'export EXTERNAL_NETWORK=%s' % ext_network
        try:
            with open(rc_file, 'a') as f:
                f.write(cmd + '\n')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
