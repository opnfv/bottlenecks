#!/usr/bin/env python
##############################################################################
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
'''This file contain all functions about storperf API.
At present, This file contain the following function:
1. Ask storperf to configure the environment (create a new stack and cinder volume)
2. Ask Storperf to run testcase and get the job id.
3. Use Job id to ask storperf for status, metrics and metadata.
4. Query information about current jobs, environment and view logs.'''

import sys
import time
import requests
import json
import utils.logger as logger

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
    }
LOG = logger.Logger(__name__).getLogger()


def storperf_env_prepare(con_dic):
    base_url = ("http://%s/api/v1.0/configurations"
                % (con_dic['storperf_test_ip']))
    test_dict = {
        "agent_count": 1,
        "agent_image": "Ubuntu 16.04 x86_64",
        "agent_flavor": "storperf",
        "public_network": "external",
        "volume_size": 10
    }
    LOG.info("waiting for storperf environment to prepare")
    reponse = requests.post(
        base_url, data=json.dumps(test_dict), headers=headers)
    ask_data = json.loads(reponse.text)
    stack_id = ask_data["stack_id"]
    LOG.info("Done, storperf environment prepare complete!")
    time.sleep(30)
    return stack_id


def warmup(con_dic):
    base_url = ("http://%s/api/v1.0/jobs"
                % (con_dic['storperf_test_ip']))
    test_dict = {
        "workload": "_warm_up"
    }
    LOG.info("filling the cinder volume with random data")
    reponse = requests.post(
        base_url, data=json.dumps(test_dict), headers=headers)
    ask_data = json.loads(reponse.text)
    job_id = ask_data["job_id"]
    LOG.info("Done, filled the cinder volume with random data!")
    time.sleep(600)
    return job_id


def job(con_dic):
    base_url = ("http://%s/api/v1.0/jobs"
                % (con_dic['storperf_test_ip']))
    test_dict = {
        "block_sizes": "2048,4096",
        "deadline": 30,
        "queue_depths": "2,4",
        "workload": "rr, rs, rw, wr, ws"
    }
    LOG.info("running the storage performance testcase")
    reponse = requests.post(
        base_url, data=json.dumps(test_dict), headers=headers)
    ask_data = json.loads(reponse.text)
    job_id = ask_data["job_id"]
    LOG.info("Done, testcase still executing for duration mentioned in deadline param")
    time.sleep(1800)
    return job_id


def current_jobs(con_dic):
    base_url = ("http://%s/api/v1.0/jobs"
                % (con_dic['storperf_test_ip']))
    requests.post(
        base_url, headers=headers)
    LOG.info("check for current jobs")


def job_status(con_dic):
    base_url = ("http://%s/api/v1.0/jobs?id=%s&type=status"
                % (con_dic['storperf_test_ip'].id))
    requests.post(
        base_url, headers=headers)
    LOG.info("check for job status")


def job_metrics(con_dic):
    base_url = ("http://%s/api/v1.0/jobs?id=%s&type=metrics"
                % (con_dic['storperf_test_ip'].id))
    requests.post(
        base_url, headers=headers)
    LOG.info("check for job metrics")


def job_metadata(con_dic):
    base_url = ("http://%s/api/v1.0/jobs?id=%s&type=metadata"
                % (con_dic['storperf_test_ip'].id))
    requests.post(
        base_url, headers=headers)
    LOG.info("check for job metadata")


def get_logs(con_dic):
    base_url = ("http://%s/api/v1.0/logs?lines=all"
                % (con_dic['storperf_test_ip']))
    requests.post(
        base_url, headers=headers)
    LOG.info("check for logs")


def get_quotas(con_dic):
    base_url = ("http://%s/api/v1.0/quotas"
                % (con_dic['storperf_test_ip']))
    requests.post(
        base_url, headers=headers)
    LOG.info("check for current quotas")


def get_configurations(con_dic):
    base_url = ("http://%s/api/v1.0/configurations"
                % (con_dic['storperf_test_ip']))
    requests.post(
        base_url, headers=headers)
    LOG.info("check for current configurations")

