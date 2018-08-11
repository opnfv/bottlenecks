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
import utils.logger as log
from kubernetes import client, watch


LOG = log.Logger(__name__).getLogger()
INSTALLER_TYPE = os.getenv("INSTALLER_TYPE")


def get_config_path(INSTALLER_TYPE=None, CONFIG_PATH="/tmp/k8s_config"):
    if INSTALLER_TYPE:
        CMD = "bash k8s_config_pre.sh -i " + INSTALLER_TYPE + \
              " -c " + CONFIG_PATH
        LOG.info("Executing command: " + CMD)
        CONFIG_PATH = os.popen(CMD)
    else:
        if not os.path.exists(CONFIG_PATH):
            raise Exception("Must at least specify the path \
of k8s config!")
    return CONFIG_PATH


def get_core_api(version='v1'):
    if version.lower() == 'v1':
        API = client.CoreV1Api()
        LOG.info(API)
    else:
        raise Exception("Must input a validate verison!")
    return API


def watch_namespace(namespace='kube-system', count=2, _request_timeout=60):
    w = watch.Watch()
    for event in w.stream(namespace, _request_timeout):
        LOG.info("Event: %s %s" %
                 (event['type'], event['object'].metadata.name))
        count -= 1
        if not count:
            w.stop()
    LOG.info("Ended.")
