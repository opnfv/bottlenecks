#!/usr/bin/env python
##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


import os
import commands
import utils.logger as log
import utils.infra_setup.heat.manager as client_manager

LOG = log.Logger(__name__).getLogger()

neutron_quota = {"subnet": -1,
                 "network": -1,
                 "floatingip": -1,
                 "subnetpool": -1,
                 "router": -1,
                 "port": -1,
                 "security_group": -1,
                 "security_group_rule": -1,
                 "rbac_policy": -1}

nova_quota = {"ram": -1,
              "cores": -1,
              "instances": -1,
              "key_pairs": -1,
              "fixed_ips": -1,
              "floating_ips": -1,
              "server_groups": -1,
              "injected_files": -1,
              "metadata_items": -1,
              "security_groups": -1,
              "security_group_rules": -1,
              "server_group_members": -1,
              "injected_file_content_bytes": -1,
              "injected_file_path_bytes": -1}


def check_https_enabled():
    LOG.debug("Check if https is enabled in OpenStack")
    os_auth_url = os.getenv('OS_AUTH_URL')
    if os_auth_url.startswith('https'):
        LOG.debug("https is enabled")
        return True
    LOG.debug("https is not enabled")
    return False


def quota_env_prepare():
    https_enabled = check_https_enabled()
    insecure_option = ''
    insecure = os.getenv('OS_INSECURE',)
    if https_enabled:
        LOG.info("https is enabled")
        if insecure:
            if insecure.lower() == "true":
                insecure_option = ' --insecure '
            else:
                LOG.warn("Env variable OS_INSECURE is {}: if https + no "
                         "credential used, it should be set as True."
                         .format(insecure))

    project_name = os.getenv("OS_PROJECT_NAME")
    cmd = ("openstack {} project list | grep ".format(insecure_option) +
           project_name +
           " | awk '{print $2}'")

    result = commands.getstatusoutput(cmd)
    if result[0] == 0 and 'exception' not in result[1]:
        LOG.info("Get %s project id is %s" % (project_name, result[1]))
    else:
        LOG.error("can't get openstack project id")
        return 1

    openstack_id = result[1]

    nova_client = client_manager._get_nova_client()
    neutron_client = client_manager._get_neutron_client()

    nova_q = nova_client.quotas.get(openstack_id).to_dict()
    neutron_q = neutron_client.show_quota(openstack_id)
    LOG.info(project_name + "project nova and neutron quota(previous) :")
    LOG.info(nova_q)
    LOG.info(neutron_q)

    nova_client.quotas.update(openstack_id, **nova_quota)
    neutron_client.update_quota(openstack_id,
                                {'quota': neutron_quota})
    LOG.info("Quota has been changed!")

    nova_q = nova_client.quotas.get(openstack_id).to_dict()
    neutron_q = neutron_client.show_quota(openstack_id)
    LOG.info(project_name + "project nova and neutron quota(now) :")
    LOG.info(nova_q)
    LOG.info(neutron_q)
    return 0
