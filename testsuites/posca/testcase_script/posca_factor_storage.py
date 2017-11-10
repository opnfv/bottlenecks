#!/usr/bin/env python
##############################################################################
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
'''This file realize the function of run posca storage bottlenecks test script.
for example this contain two part first run_script,
second is algorithm, this part is about how to judge the bottlenecks.
This test is using storperf as a tool to begin test.'''

import os
import time
import utils.logger as log
from utils.parser import Parser as conf_parser
import utils.env_prepare.stack_prepare as stack_prepare
import utils.infra_setup.runner.storperf_usage as storperf_usage
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
        "testcase": "storage_bottlenecks"
    }
}
testfile = os.path.basename(__file__)
testcase, file_format = os.path.splitext(testfile)


def env_pre(con_dic, test_config):
    LOG.info("storperf environment prepare!")
    stack_prepare._prepare_storperf_env_daemon(True)
    LOG.info("Storperf environment prepare, done!")

    con_dic = test_config["load_manager"]
    storperf_usage.storperf_env_prepare(
              con_dic,
              con_dic['load_manager']['agent_count'],
              con_dic['load_manager']['agent_image'],
              con_dic['load_manager']['agent_flavor'],
              con_dic['load_manager']['volume_size']
    )
    LOG.info("Storperf stack prepared!")


def config_to_result(test_config, test_result):
    testdata = {}
    parser_result = test_result["benchmark"]["data"]
    test_result.update(test_config)
    test_result.update(parser_result)
    test_result["iops"] = float(test_result["iops"])
    test_result["bandwidth"] = float(test_result["bandwidth"])
    test_result["latency"] = float(test_result["latency"])
    testdata["data_body"] = test_result
    testdata["testcase"] = testcase
    return testdata


def do_test(test_config, Use_Dashboard, context_conf):
    storperf_container = docker_env.storperf_info['container']
    con_dic = test_config["load_manager"]
    cmd = storperf_usage.job(con_dic)
    print(cmd)
    stdout = docker_env.docker_exec_cmd(storperf_container, cmd)
    LOG.info(stdout)

    status_data = storperf_usage.job_status(con_dic, stdout)
    loop_value = 0
    while loop_value < 60:
        time.sleep(30)
        loop_value = loop_value + 1
        if status_data["status"] == "Completed":
            LOG.info("storperf run success")
            break
        elif status_data["status"] == "Pending":
            LOG.error("storperf error exit")
            exit()

    save_data = config_to_result(test_config, status_data)
    if Use_Dashboard is True:
        print("Use Dashboard")
        # DashBoard.dashboard_send_data(context_conf, save_data)

    return save_data


def run(test_config):
    con_dic = test_config["load_manager"]
    Use_Dashboard = False

    env_pre(None)
    if test_config["contexts"]["storperf_ip"] is None:
        con_dic["contexts"]["storperf_ip"] =\
            conf_parser.ip_parser("storperf_test_ip")

    if "dashboard" in test_config["contexts"].keys():
        if test_config["contexts"]["dashboard_ip"] is None:
            test_config["contexts"]["dashboard_ip"] =\
                conf_parser.ip_parser("dashboard")
        LOG.info("Create Dashboard data")
        Use_Dashboard = True
        # DashBoard.dashboard_storage_bottlenecks(test_config["contexts"])

    data = {}
    data["bs"] = conf_parser.str_to_list(con_dic['scenarios']['block_sizes'])
    data["wl"] = conf_parser.str_to_list(con_dic['scenarios']['workload'])
    data["qd"] = conf_parser.str_to_list(con_dic['scenarios']['queue_depths'])

    con_dic["result_file"] = os.path.dirname(
        os.path.abspath(__file__)) + "/test_case/result"
    cur_role_result = 1
    pre_role_result = 1
    pre_reply = {}
    data_return = {}
    data_max = {}
    data_return["throughput"] = 1

    for test_x in data["wl"]:
        data_max["throughput"] = 1
        bandwidth_tmp = 1
        for test_y in data["bs"]:
            for test_z in data["qd"]:
                case_config = {
                    "workload": float(test_x),
                    "block_sizes": float(test_y),
                    "queue_depths": float(test_z),
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
