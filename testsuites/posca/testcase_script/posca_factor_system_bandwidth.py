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
import uuid
import json
import utils.logger as log
from utils.parser import Parser as conf_parser
import utils.env_prepare.stack_prepare as stack_prepare
import testsuites.posca.testcase_dashboard.system_bandwidth as DashBoard
import utils.infra_setup.runner.docker_env as docker_env
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
    LOG.info("yardstick environment prepare!")
    stack_prepare._prepare_env_daemon(True)


def config_to_result(test_config, test_result):
    testdata = {}
    parser_result = test_result["benchmark"]["data"]
    test_result.update(test_config)
    test_result.update(parser_result)
    test_result["throughput"] = float(test_result["throughput"])
    test_result["remote_cpu_util"] = float(test_result["remote_cpu_util"])
    test_result["local_cpu_util"] = float(test_result["local_cpu_util"])
    test_result["mean_latency"] = float(test_result["mean_latency"])
    testdata["data_body"] = test_result
    testdata["testcase"] = testcase
    return testdata


def testcase_parser(out_file="yardstick.out", **parameter_info):
    cmd = ('yardstick task start /home/opnfv/repos/yardstick/'
           'samples/netperf_bottlenecks.yaml --output-file ' + out_file)
    cmd = cmd + " --task-args " + '"' + str(parameter_info) + '"'
    LOG.info("yardstick test cmd is: %s" % cmd)
    return cmd


def do_test(test_config, Use_Dashboard, context_conf):
    yardstick_container = docker_env.yardstick_info['container']
    out_file = ("/tmp/yardstick_" + str(uuid.uuid4()) + ".out")
    cmd = testcase_parser(out_file=out_file, **test_config)
    stdout = docker_env.docker_exec_cmd(yardstick_container, cmd)
    LOG.info(stdout)
    loop_value = 0
    while loop_value < 60:
        time.sleep(2)
        loop_value = loop_value + 1
        with open(out_file) as f:
            data = json.load(f)
            if data["status"] == 1:
                LOG.info("yardstick run success")
                break
            elif data["status"] == 2:
                LOG.error("yardstick error exit")
                exit()

    save_data = config_to_result(test_config, data['result'][1])
    if Use_Dashboard is True:
        DashBoard.dashboard_send_data(context_conf, save_data)

    return save_data["data_body"]


def run(test_config):
    con_dic = test_config["load_manager"]
    Use_Dashboard = False
    env_pre(None)
    if test_config["contexts"]["yardstick_ip"] is None:
        con_dic["contexts"]["yardstick_ip"] =\
            conf_parser.ip_parser("yardstick_test_ip")

    if "dashboard" in test_config["contexts"].keys():
        if test_config["contexts"]["dashboard_ip"] is None:
            test_config["contexts"]["dashboard_ip"] =\
                conf_parser.ip_parser("dashboard")
        LOG.info("Create Dashboard data")
        Use_Dashboard = True
        DashBoard.dashboard_system_bandwidth(test_config["contexts"])

    data = {}
    rx_pkt_a = con_dic['scenarios']['rx_pkt_sizes'].split(',')
    tx_pkt_a = con_dic['scenarios']['tx_pkt_sizes'].split(',')
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

    for test_x in data["tx_pkt_sizes"]:
        data_max["throughput"] = 1
        bandwidth_tmp = 1
        for test_y in data["rx_pkt_sizes"]:
            case_config = {
                "tx_msg_size": float(test_x),
                "rx_msg_size": float(test_y),
                "test_time": con_dic['scenarios']['test_times'],
                "pod_info": conf_parser.bottlenecks_config["pod_info"]
            }
            data_reply = do_test(case_config, Use_Dashboard,
                                 test_config["contexts"])

            conf_parser.result_to_file(data_reply, test_config["out_file"])
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
