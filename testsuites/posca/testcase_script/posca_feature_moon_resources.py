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
import testsuites.posca.testcase_dashboard.posca_moon_resources as DashBoard
import utils.infra_setup.runner.yardstick as yardstick_task

# --------------------------------------------------
# logging configuration
# --------------------------------------------------
LOG = log.Logger(__name__).getLogger()

testfile = os.path.basename(__file__)
testcase, file_format = os.path.splitext(testfile)
runner_DEBUG = True


def env_pre():
    if "moon_envpre" in test_config["contexts"].keys():
        if test_config["contexts"]['moon_envpre'] is True:
            moon_env = True
            moon_environment = test_config["contexts"]['moon_environment']
            moon_env.moon_envprepare(moon_environment)
    LOG.info("yardstick environment prepare!")


def config_to_result(test_config, test_result):
    final_data = {}
    final_data["testcase"] = "posca_factor_moon_resources"
    final_data["test_body"] = []
    print(test_result)
    out_data = test_result["result"]["testcases"]
    test_data = out_data["moon_resource"]["tc_data"]
    for result in test_data:
        testdata = {}
        testdata["tenant_number"] = int(test_config["tenants"])
        testdata["max_user"] = result["data"]["user_number"]
        print testdata
        final_data["test_body"].append(testdata)
    return final_data


def testcase_parser(runner_conf, out_file="yardstick.out", **parameter_info):
    cidr = "/home/opnfv/repos/yardstick/" + \
           runner_conf["yardstick_test_dir"] + "/" + \
           runner_conf["yardstick_testcase"] + ".yaml"
    cmd = yardstick_task.yardstick_command_parser(debug=runner_DEBUG,
                                                  cidr=cidr,
                                                  outfile=out_file,
                                                  parameter=parameter_info)
    return cmd


def do_test(runner_conf, test_config, Use_Dashboard, context_conf):
    yardstick_container = docker_env.yardstick_info['container']
    out_file = ("/tmp/yardstick_" + str(uuid.uuid4()) + ".out")
    cmd = testcase_parser(runner_conf, out_file=out_file, **test_config)
    print(cmd)
    # stdout = docker_env.docker_exec_cmd(yardstick_container, cmd)
    stdout = "mock yardstick out"
    LOG.info(stdout)
    #loop_value = 0
    #while loop_value < 60:
    #    time.sleep(2)
    #    loop_value = loop_value + 1
    #    with open(out_file) as f:
    #        data = json.load(f)
    #        if data["status"] == 1:
    #            LOG.info("yardstick run success")
    #            break
    #        elif data["status"] == 2:
    #            LOG.error("yardstick error exit")
    #            exit()
    # data = json.load(output)
    data={"result":{"testcases":{"moon_resource":{"tc_data":[{"data":{"user_number": 20}}]}}}}

    save_data = config_to_result(test_config, data)
    if Use_Dashboard is True:
        print("use dashboard")
        DashBoard.dashboard_send_data(context_conf, save_data)

    # return save_data["data_body"]
    return save_data


def run(test_config):
    load_config = test_config["load_manager"]
    scenarios_conf = load_config["scenarios"]
    runner_conf = load_config["runners"]
    Use_Dashboard = False
    env_pre()
    if test_config["contexts"]["yardstick_ip"] is None:
        load_config["contexts"]["yardstick_ip"] =\
            conf_parser.ip_parser("yardstick_test_ip")

    if "dashboard" in test_config["contexts"].keys():
        if test_config["contexts"]["dashboard_ip"] is None:
            test_config["contexts"]["dashboard_ip"] =\
                conf_parser.ip_parser("dashboard")
        LOG.info("Create Dashboard data")
        Use_Dashboard = True
        # DashBoard.dashboard_system_bandwidth(test_config["contexts"])

    tenants_conf = conf_parser.str_to_list(scenarios_conf["tenants"])

    load_config["result_file"] = os.path.dirname(
        os.path.abspath(__file__)) + "/test_case/result"

    result = []

    for tenants in tenants_conf:
        case_config = {"tenants": tenants}

        data_reply = do_test(runner_conf, case_config,
                             Use_Dashboard, test_config["contexts"])
        result.append(data_reply)

    LOG.info("Finished bottlenecks testcase")
    LOG.info("The result data is %s", result)
    return result

