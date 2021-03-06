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
1. Ask storperf to configure the environment.
2. Ask Storperf to run testcase and get the job id.
3. Use Job id to ask storperf for status, metrics and metadata.
4. Query information about current jobs, environment and view logs.'''

import time
import requests
import json
import os
import utils.logger as logger

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
    }
LOG = logger.Logger(__name__).getLogger()


def storperf_env_prepare(con_dic, storperf_count, storperf_image,
                         storperf_flavor, volume_size):
    base_url = ("http://%s/api/v1.0/configurations"
                % (con_dic['storperf_test_ip']))
    test_dict = {
        "agent_count": storperf_count,
        "agent_image": storperf_image,
        "agent_flavor": storperf_flavor,
        "public_network": os.environ.get("EXTERNAL_NETWORK"),
        "volume_size": volume_size
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
        "block_sizes": con_dic['block_sizes'],
        "deadline": con_dic['deadline'],
        "steady_state_samples": con_dic['steady_state_samples'],
        "queue_depths": con_dic['queue_depths'],
        "workload": con_dic['workload']
    }
    deadline = con_dic['deadline']
    LOG.info("running the storage performance testcase")
    reponse = requests.post(
        base_url, data=json.dumps(test_dict), headers=headers)
    ask_data = json.loads(reponse.text)
    job_id = ask_data["job_id"]
    LOG.info("Done, testcase still executing for specified deadline")
    time.sleep(deadline)
    return job_id


def current_jobs(con_dic):
    base_url = ("http://%s/api/v1.0/jobs"
                % (con_dic['storperf_test_ip']))
    reply_response = requests.get(
        base_url, headers=headers)
    reply_data = json.loads(reply_response.text)
    LOG.info("current storperf jobs are %s" % (reply_data))
    return reply_data


def job_status(con_dic, job_id):
    base_url = ("http://%s/api/v1.0/jobs?id=%s&type=status"
                % (con_dic['storperf_test_ip'], job_id))
    reply_response = requests.get(
        base_url, headers=headers)
    reply_data = json.loads(reply_response.text)
    LOG.info("job status is %s" % (reply_data))
    return reply_data


def job_metrics(con_dic, job_id):
    base_url = ("http://%s/api/v1.0/jobs?id=%s&type=metrics"
                % (con_dic['storperf_test_ip'], job_id))
    reply_response = requests.get(
        base_url, headers=headers)
    reply_data = json.loads(reply_response.text)
    LOG.info("job metrics is %s" % (reply_data))
    return reply_data


def job_metadata(con_dic, job_id):
    base_url = ("http://%s/api/v1.0/jobs?id=%s&type=metadata"
                % (con_dic['storperf_test_ip'], job_id))
    reply_response = requests.get(
        base_url, headers=headers)
    reply_data = json.loads(reply_response.text)
    LOG.info("job metadata is %s" % (reply_data))
    return reply_data


def get_logs(con_dic):
    base_url = ("http://%s/api/v1.0/logs?lines=all"
                % (con_dic['storperf_test_ip']))
    reply_response = requests.get(
        base_url, headers=headers)
    reply_data = json.loads(reply_response.text)
    LOG.info("All storperf logs: %s" % (reply_data))
    return reply_data


def get_quotas(con_dic):
    base_url = ("http://%s/api/v1.0/quotas"
                % (con_dic['storperf_test_ip']))
    reply_response = requests.get(
        base_url, headers=headers)
    reply_data = json.loads(reply_response.text)
    LOG.info("current quotas is %s" % (reply_data))
    return reply_data


def get_configurations(con_dic):
    base_url = ("http://%s/api/v1.0/configurations"
                % (con_dic['storperf_test_ip']))
    reply_response = requests.get(
        base_url, headers=headers)
    reply_data = json.loads(reply_response.text)
    LOG.info("current configurations is %s" % (reply_data))
    return reply_data


def delete_configurations(con_dic):
    base_url = ("http://%s/api/v1.0/configurations"
                % (con_dic['storperf_test_ip']))
    requests.delete(
        base_url, headers=headers)
    LOG.info("delete the storperf environment")


def delete_jobs(con_dic):
    base_url = ("http://%s/api/v1.0/jobs"
                % (con_dic['storperf_test_ip']))
    requests.delete(
        base_url, headers=headers)
    LOG.info("delete current storperf jobs")
