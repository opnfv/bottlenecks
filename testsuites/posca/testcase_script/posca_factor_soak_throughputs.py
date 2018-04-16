#!/usr/bin/env python
##############################################################################
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
'''This file is to do data-plane baseline test for
VM pair life-cycle events using netperf.
Testing steps are summarized below:
1. run_test load testcase configuration
2. Bottlenecks eliminates the environments limits/constraints
3. Bottlenecks tells Yardstick to prepare environment
4. Bottlenecks tells Yardstick to run test
   3.1 to create stack
   3.2 to install netperf
   3.3 to send/forward packets for t2 seconds
   3.4 record results and detroy stack
   3.4 after every t1 seconds goto 3.1 and repeat the workflow
5. Bottlenecks collects testing results from Yardstick
6. Bottlenecks tells Yardstick to stop when time ends
   or system fails the test
7. Bottlenecks sends testing data to bottlenecks-elk'''

import utils.logger as log
import uuid
import json
import os
import sys
import time
import threading
import datetime
import Queue
from utils.parser import Parser as conf_parser
import utils.env_prepare.quota_prepare as quota_prepare
import utils.env_prepare.stack_prepare as stack_prepare
import utils.infra_setup.runner.yardstick as runner_yardstick
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
cidr = "/home/opnfv/repos/yardstick/samples/netperf_soak.yaml"
runner_DEBUG = True

q = Queue.Queue()


def env_pre(test_config):
    test_yardstick = False
    if "yardstick" in test_config["contexts"].keys():
        test_yardstick = True
    stack_prepare._prepare_env_daemon(test_yardstick)
    quota_prepare.quota_env_prepare()
    LOG.info("yardstick environment prepare!")
    if(test_config["contexts"]['yardstick_envpre']):
        stdout = runner_yardstick.yardstick_image_prepare()
        LOG.debug(stdout)


def do_test(con_dic):
    func_name = sys._getframe().f_code.co_name
    out_file = ("/tmp/yardstick_" + str(uuid.uuid4()) + ".out")
    parameter_info = dict(test_time=con_dic["scenarios"]["vim_pair_ttl"])
    yardstick_container = docker_env.yardstick_info['container']
    cmd = runner_yardstick.yardstick_command_parser(debug=runner_DEBUG,
                                                    cidr=cidr,
                                                    outfile=out_file,
                                                    parameter=parameter_info)
    stdout = docker_env.docker_exec_cmd(yardstick_container, cmd)
    LOG.info(stdout)
    out_value = 0
    loop_value = 0
    while loop_value < 60:
        time.sleep(2)
        loop_value = loop_value + 1
        with open(out_file) as f:
            data = json.load(f)
            if data["status"] == 1:
                LOG.info("Success run yardstick netperf_soak test!")
                out_value = 1
                break
            elif data["status"] == 2:
                LOG.error("Failed run yardstick netperf_soak test!")
                out_value = 0
                break
    q.put((out_value, func_name))
    return out_value


def config_to_result(
        test_duration, added_duration, vim_pair_ttl,
        vim_pair_lazy_cre_delay,
        vim_pair_num, vim_pair_success_num, result):
    testdata = {}
    test_result = {}
    test_result["test_duration"] = test_duration
    test_result["sum_duration"] = added_duration
    test_result["vim_pair_ttl"] = vim_pair_num
    test_result["vim_pair_cre_interval"] = vim_pair_lazy_cre_delay
    test_result["result"] = result
    testdata["data_body"] = test_result
    testdata["testcase"] = testcase
    return testdata


def func_run(con_dic):
    test_date = do_test(con_dic)
    return test_date


def run(test_config):
    con_dic = test_config["load_manager"]

    env_pre(test_config)
    LOG.info("yardstick environment prepare done!")

    test_duration = float(
        con_dic["scenarios"]["test_duration_hours"]) * 3600
    vim_pair_ttl = float(
        con_dic["scenarios"]["vim_pair_ttl"])
    vim_pair_lazy_cre_delay = float(
        con_dic["scenarios"]["vim_pair_lazy_cre_delay"])
    vim_pair_num = int(
        ((test_duration - vim_pair_ttl) / vim_pair_lazy_cre_delay) + 1
    )

    threadings = []
    result = []
    vim_pair_success_num = 0

    start_time = datetime.datetime.now()

    LOG.info("Data-path test duration are %i seconds", test_duration)
    LOG.info("TTL of each VM pair are %i seconds", vim_pair_ttl)
    LOG.info("Creation delay between VM pairs are %i seconds",
             vim_pair_lazy_cre_delay)
    LOG.info("Number of VM pairs to be created are %i", vim_pair_num)

    for vim_pair_index in xrange(0, vim_pair_num - 1):
        index_thread = threading.Thread(target=func_run,
                                        args=(str(vim_pair_index),))
        threadings.append(index_thread)
        index_thread.start()
        vim_pair_error = False
        for wait_time in xrange(0, int(vim_pair_lazy_cre_delay) - 1):
            time.sleep(1)
            while not q.empty():
                result.append(q.get())
            if ('0', 'do_test') in result:
                vim_pair_error = True
                break
        for item in result:
            vim_pair_success_num += int(item[0])
        if vim_pair_error:
            break

    end_time = datetime.datetime.now()
    added_duration = (start_time - end_time).seconds
    LOG.info("Number of success VM pairs/threads are %s: ",
             vim_pair_success_num)

    return_result = config_to_result(
        test_duration, added_duration, vim_pair_ttl,
        vim_pair_lazy_cre_delay,
        vim_pair_num, vim_pair_success_num, result
    )

    conf_parser.result_to_file(return_result, test_config["out_file"])

    return vim_pair_error
