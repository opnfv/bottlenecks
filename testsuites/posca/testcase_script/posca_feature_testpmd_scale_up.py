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
import utils.infra_setup.runner.docker_env as docker_env
import utils.infra_setup.runner.yardstick as yardstick_task

# --------------------------------------------------
# logging configuration
# --------------------------------------------------
LOG = log.Logger(__name__).getLogger()

testfile = os.path.basename(__file__)
testcase, file_format = os.path.splitext(testfile)
cidr = "/home/opnfv/repos/yardstick/samples/pvp_throughput_bottlenecks.yaml"
runner_DEBUG = True


def env_pre(con_dic):
    LOG.info("yardstick environment prepare!")
    stack_prepare._prepare_env_daemon(True)


def config_to_result(test_config, test_result):
    final_data = []
    print(test_result)
    out_data = test_result["result"]["testcases"]
    test_data = out_data["pvp_throughput_bottlenecks"]["tc_data"]
    for result in test_data:
        testdata = {}
        testdata["vcpu"] = test_config["vcpu"]
        testdata["memory"] = test_config["memory"]
        testdata["nrFlows"] = result["data"]["nrFlows"]
        testdata["packet_size"] = result["data"]["packet_size"]
        testdata["throughput"] = result["data"]["throughput_rx_mbps"]
        final_data.append(testdata)
    return final_data


def testcase_parser(out_file="yardstick.out", **parameter_info):
    cmd = yardstick_task.yardstick_command_parser(debug=runner_DEBUG,
                                                  cidr=cidr,
                                                  outfile=out_file,
                                                  parameter=parameter_info)
    return cmd


def do_test(test_config, Use_Dashboard, context_conf):
    yardstick_container = docker_env.yardstick_info['container']
    out_file = ("/tmp/yardstick_" + str(uuid.uuid4()) + ".out")
    cmd = testcase_parser(out_file=out_file, **test_config)
    print(cmd)
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

    save_data = config_to_result(test_config, data)
    if Use_Dashboard is True:
        print("use dashboard")
    return save_data


def run(test_config):
    load_config = test_config["load_manager"]
    scenarios_conf = load_config["scenarios"]
    Use_Dashboard = False

    env_pre(None)
    if test_config["contexts"]["yardstick_ip"] is None:
        load_config["contexts"]["yardstick_ip"] =\
            conf_parser.ip_parser("yardstick_test_ip")

    if "dashboard" in test_config["contexts"].keys():
        if test_config["contexts"]["dashboard_ip"] is None:
            test_config["contexts"]["dashboard_ip"] =\
                conf_parser.ip_parser("dashboard")
        LOG.info("Create Dashboard data")
        Use_Dashboard = True

    cpus = conf_parser.str_to_list(scenarios_conf["cpus"])
    mems = conf_parser.str_to_list(scenarios_conf["mems"])
    pkt_size = conf_parser.str_to_list(scenarios_conf["pkt_size"])
    multistream = conf_parser.str_to_list(scenarios_conf["multistream"])
    search_interval = scenarios_conf["search_interval"]

    load_config["result_file"] = os.path.dirname(
        os.path.abspath(__file__)) + "/test_case/result"

    if len(cpus) != len(mems):
        LOG.error("the cpus and mems config data number is not same!")
        os._exit()

    result = []

    for i in range(0, len(cpus)):
        case_config = {"vcpu": cpus[i],
                       "memory": int(mems[i]) * 1024,
                       "multistreams": multistream,
                       "pktsize": pkt_size,
                       "search_interval": search_interval}

        data_reply = do_test(case_config, Use_Dashboard,
                             test_config["contexts"])
        result.append(data_reply)

    LOG.info("Finished bottlenecks testcase")
    LOG.info("The result data is %s", result)
    return result
