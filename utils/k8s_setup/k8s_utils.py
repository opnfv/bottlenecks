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
import commands
import json
import utils.logger as log
from kubernetes import client, watch


LOG = log.Logger(__name__).getLogger()
INSTALLER_TYPE = os.getenv("INSTALLER_TYPE")
K8S_UTILS = "/home/opnfv/bottlenecks/utils/k8s_setup"


def get_config_path(INSTALLER_TYPE=None, K8S_CONFIG_PATH="/tmp/k8s_config"):
    if INSTALLER_TYPE:
        CMD = "bash " + K8S_UTILS + "/k8s_config_pre.sh -i " \
              + INSTALLER_TYPE + \
              " -c " + K8S_CONFIG_PATH
        LOG.info("Executing command: " + CMD)
        os.popen(CMD)
    else:
        if not os.path.exists(K8S_CONFIG_PATH):
            raise Exception("Must at least specify the path \
of k8s config!")
    return K8S_CONFIG_PATH


def get_core_api(version='v1'):
    if version.lower() == 'v1':
        API = client.CoreV1Api()
        LOG.info(API)
    else:
        raise Exception("Must input a valid verison!")
    return API


def get_apps_api(version='v1'):
    if version.lower() == 'v1':
        API = client.AppsV1Api()
        LOG.info(API)
    else:
        raise Exception("Must input a valid verison!")
    return API


def get_namespace_status(namespace):
    CMD = ("kubectl get ns | grep %s" % namespace)
    namespace_existed = commands.getstatusoutput(CMD)
    return namespace_existed


def get_deployment_status(name, namespace):
    CMD = ("kubectl get deployment --namespace={} | grep {}".format(
        namespace, name))
    deployment_existed = commands.getstatusoutput(CMD)
    return deployment_existed


def get_available_pods(name, namespace):
    CMD = ("kubectl get deployment --namespace={} | grep {}".format(
        namespace, name) + " | awk '{print $5}'")
    available_pods = commands.getstatusoutput(CMD)
    return int(available_pods[1])


def watch_namespace(namespace, count=3, stop=None, request_timeout=0):
    w = watch.Watch()
    LOG.debug("Watch object generated: {}".format(w))
    LOG.info("Watch stream generated: {}".format(
             w.stream(namespace, _request_timeout=request_timeout)))
    for event in w.stream(namespace, _request_timeout=request_timeout):
        LOG.info("Event: %s %s" %
                 (event['type'], event['object'].metadata.name))
        if event['object'].metadata.name == stop:
            LOG.info("Namesapce successfully added.\n")
            w.stop()
        count -= 1
        if not count:
            LOG.info("Ended.\n")
            w.stop()


def write_json(data, file_name):
    with open(file_name, "a") as f:
        f.write(json.dumps(data, f))
        f.write("\n")
