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
import Queue
import multiprocessing
import utils.logger as log
from utils.parser import Parser as conf_parser
import utils.env_prepare.moon_prepare as moon_env
import utils.infra_setup.runner.yardstick as yardstick_task
import testsuites.posca.testcase_dashboard.posca_moon_tenants as DashBoard

# --------------------------------------------------
# logging configuration
# --------------------------------------------------
LOG = log.Logger(__name__).getLogger()

testfile = os.path.basename(__file__)
testcase, file_format = os.path.splitext(testfile)
runner_DEBUG = True
manager = multiprocessing.Manager()
switch = manager.Value('tmp', 0)


def env_pre(test_config):
    if "moon_envpre" in test_config["contexts"].keys():
        if test_config["contexts"]['moon_envpre'] is True:
            moon_env = True
            moon_environment = test_config["contexts"]['moon_environment']
            moon_env.moon_envprepare(moon_environment)
    LOG.info("yardstick environment prepare!")


def config_to_result(test_result):
    final_data = {}
    final_data["testcase"] = "posca_factor_moon_tenants"
    final_data["test_body"] = []
    final_data["test_body"].append(test_result)
    return final_data


def testcase_parser(runner_conf, out_file="yardstick.out", **parameter_info):
    cidr = "/home/opnfv/repos/yardstick/" + \
           runner_conf["yardstick_test_dir"] + "/" + \
           runner_conf["yardstick_testcase"]
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
    #stdout = docker_env.docker_exec_cmd(yardstick_container, cmd)
    #LOG.info(stdout)
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
    time.sleep(50)
    switch.value += 1
    save_date = []
    return save_date


def run(test_config):
    load_config = test_config["load_manager"]
    scenarios_conf = load_config["scenarios"]
    runner_conf = load_config["runners"]
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

    resources = scenarios_conf["resources"]
    initial = scenarios_conf["initial"]
    threshhold = scenarios_conf["steps"]
    timeout = scenarios_conf["timeout"]
    SLA = scenarios_conf["SLA"]
    case_config = {"SLA": SLA,
                   "resources": resources}

    process_queue = Queue.Queue()

    load_config["result_file"] = os.path.dirname(
        os.path.abspath(__file__)) + "/test_case/result"

    result = 0

    if initial is 0:
        tenant_number = threshhold
    else:
        tenant_number = initial
    while switch.value == 0:
        LOG.info("Start %d process", tenant_number)
        for tenant in range(0, tenant_number):
            process = multiprocessing.Process(target=do_test,
                                              args=(runner_conf,
                                                    case_config,
                                                    Use_Dashboard,
                                                    test_config["contexts"],
                                                    ))
            process.start()
            process_queue.put(process)

        result = result + tenant_number
        tenant_number = threshhold
        time.sleep(timeout)
        
    while process_queue.qsize():
        process = process_queue.get()
        process.terminate()

    if result is initial:
        result = 0
    else:
        result = result - threshhold

    testdate = {"tenant_max": result}
    testresult = config_to_result(testdate)
    print testresult
    LOG.info("Finished bottlenecks testcase")
    LOG.info("The result data is %d", result)
    print Use_Dashboard
    if Use_Dashboard is True:
        print "Use Dashboard"
        DashBoard.dashboard_send_data(test_config["contexts"], testresult)

    return testresult
