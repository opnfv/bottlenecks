#!/usr/bin/env python
##############################################################################
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
'''This file contain all function about yardstick API.
At present, This file contain the following function:
1.Ask Yardstick to run testcase and get a task id.
2.use task id to ask yardstick for data.
3.Ask yardstick for InfluxDB create
4.how the process of task.'''

import sys
import time
import requests
import json
import utils.logger as logger

headers = {"Content-Type": "application/json"}
LOG = logger.Logger(__name__).getLogger()


def Get_Reply(test_config, task_id, time_test=1):
    reply_url = ("http://%s/yardstick/results?task_id=%s"
                 % (test_config['yardstick_test_ip'], task_id))
    reply_response = requests.get(reply_url)
    reply_data = json.loads(reply_response.text)
    LOG.info("return data is %s" % (reply_data))
    if reply_data["status"] == 1:
        return(reply_data["result"])
    if reply_data["status"] == 0:
        if time_test == 10:
            LOG.info("yardstick time out")
            sys.exit()
        time.sleep(10)
        reply_result_data = Get_Reply(
            test_config, task_id, time_test=time_test + 1)
        return(reply_result_data)
    if reply_data["status"] == 2:
        LOG.error("yardstick error exit")
        sys.exit()


def Send_Data(test_dict, test_config):
    base_url = ("http://%s/yardstick/testcases/%s/action"
                % (test_config['yardstick_test_ip'],
                   test_config['yardstick_test_dir']))
    LOG.info("test ip addr is %s" % (base_url))
    reponse = requests.post(
        base_url, data=json.dumps(test_dict), headers=headers)
    ask_data = json.loads(reponse.text)
    task_id = ask_data["result"]
    LOG.info("yardstick task id is: %s" % (task_id))
    return task_id


def Create_Incluxdb(con_dic):
    base_url = ("http://%s/yardstick/env/action"
                % (con_dic['yardstick_test_ip']))
    test_dict = {
        "action": "createInfluxDBContainer",
    }
    requests.post(
        base_url, data=json.dumps(test_dict), headers=headers)
    LOG.info("waiting for creating InfluxDB")
    time.sleep(30)
    LOG.info("Done, creating InflxDB Container")


def find_condition(con_dic):
    base_url = ("http://%s/yardstick/asynctask?%s"
                % (con_dic['yardstick_test_ip'].id))
    requests.post(
        base_url, headers=headers)
    LOG.info("check for creating InfluxDB")

