#!/usr/bin/env python
##############################################################################
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
'''This file realize the function of run systembandwidth script.
for example this contain two part first run_script,
second is algorithm, this part is about how to judge the bottlenecks.
This test is using yardstick as a tool to begin test.'''

import os
import time
import utils.logger as log
import utils.infra_setup.runner.yardstick as Runner
from utils.parser import Parser as conf_parser
import testsuites.posca.testcase_dashboard.system_bandwidth as DashBoard
# --------------------------------------------------
# logging configuration
# --------------------------------------------------
LOG = log.Logger(__name__).getLogger()

test_dict = {
    "action": "runTestCase",
    "args": {
        "opts": {
            "task-args": {}
        },
        "testcase": "netperf_bottlenecks"
    }
}
testfile = os.path.basename(__file__)
testcase, file_format = os.path.splitext(testfile)


def env_pre(con_dic):
    Runner.Create_Incluxdb(con_dic['runner_config'])


def config_to_result(test_config, test_result):
    testdata = {}
    test_result["throughput"] = float(test_result["throughput"])
    test_result.update(test_config)
    testdata["data_body"] = test_result
    testdata["testcase"] = testcase
    return testdata


def do_test(test_config, con_dic):
    test_dict['args']['opts']['task-args'] = test_config
    Task_id = Runner.Send_Data(test_dict, con_dic['runner_config'])
    time.sleep(con_dic['test_config']['test_time'])
    Data_Reply = Runner.Get_Reply(con_dic['runner_config'], Task_id)
    try:
        test_date =\
            Data_Reply[con_dic['runner_config']['yardstick_testcase']][0]
    except IndexError:
        test_date = do_test(test_config, con_dic)

    save_data = config_to_result(test_config, test_date)
    if con_dic['runner_config']['dashboard'] == 'y':
        DashBoard.dashboard_send_data(con_dic['runner_config'], save_data)

    return save_data["data_body"]


def run(con_dic):
    data = {}
    rx_pkt_a = con_dic['test_config']['rx_pkt_sizes'].split(',')
    tx_pkt_a = con_dic['test_config']['tx_pkt_sizes'].split(',')
    data["rx_pkt_sizes"] = rx_pkt_a
    data["tx_pkt_sizes"] = tx_pkt_a
    con_dic["result_file"] = os.path.dirname(
        os.path.abspath(__file__)) + "/test_case/result"
    cur_role_result = 1
    pre_role_result = 1
    pre_reply = {}
    data_return = {}
    data_max = {}
    data_return["throughput"] = 1

    if con_dic["runner_config"]["yardstick_test_ip"] is None:
        con_dic["runner_config"]["yardstick_test_ip"] =\
            conf_parser.ip_parser("yardstick_test_ip")

    env_pre(con_dic)

    if con_dic["runner_config"]["dashboard"] == 'y':
        if con_dic["runner_config"]["dashboard_ip"] is None:
            con_dic["runner_config"]["dashboard_ip"] =\
                conf_parser.ip_parser("dashboard")
        LOG.info("Create Dashboard data")
        DashBoard.dashboard_system_bandwidth(con_dic["runner_config"])

    for test_x in data["tx_pkt_sizes"]:
        data_max["throughput"] = 1
        bandwidth_tmp = 1
        for test_y in data["rx_pkt_sizes"]:
            test_config = {
                "tx_msg_size": float(test_x),
                "rx_msg_size": float(test_y),
                "test_time": con_dic['test_config']['test_time']
            }
            data_reply = do_test(test_config, con_dic)
            conf_parser.result_to_file(data_reply, con_dic["out_file"])
            bandwidth = data_reply["throughput"]
            if (data_max["throughput"] < bandwidth):
                data_max = data_reply
            if (abs(bandwidth_tmp - bandwidth) / bandwidth_tmp < 0.025):
                LOG.info("this group of data has reached top output")
                break
            else:
                pre_reply = data_reply
                bandwidth_tmp = bandwidth
        cur_role_result = float(pre_reply["throughput"])
        if (abs(pre_role_result - cur_role_result) / pre_role_result < 0.025):
            LOG.info("The performance increases slowly")
        if data_return["throughput"] < data_max["throughput"]:
            data_return = data_max
        pre_role_result = cur_role_result
    LOG.info("Find bottlenecks of this config")
    LOG.info("The max data is %d", data_return["throughput"])
    return data_return
