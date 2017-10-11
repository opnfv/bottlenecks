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
# import threading
# import datetime
import Queue
# from utils.parser import Parser as conf_parser
import utils.env_prepare.quota_prepare as quota_prepare
import utils.env_prepare.stack_prepare as stack_prepare

# import testsuites.posca.testcase_dashboard.posca_factor_throughputs as DashBoard # noqa
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

q = Queue.Queue()


def env_pre(test_config):
    test_yardstick = False
    if "yardstick" in test_config["contexts"].keys():
        test_yardstick = True
    stack_prepare._prepare_env_daemon(test_yardstick)
    quota_prepare.quota_env_prepare()
    cmd = ('yardstick env prepare')
    LOG.info("yardstick environment prepare!")
    if(test_config["contexts"]['yardstick_envpre']):
        yardstick_container = docker_env.yardstick_info['container']
        stdout = docker_env.docker_exec_cmd(yardstick_container, cmd)
        LOG.debug(stdout)


def do_test():
    func_name = sys._getframe().f_code.co_name
    out_file = ("/tmp/yardstick_" + str(uuid.uuid4()) + ".out")
    yardstick_container = docker_env.yardstick_info['container']
    cmd = ('yardstick task start /home/opnfv/repos/yardstick/'
           'samples/netperf_bottlenecks.yaml --output-file ' + out_file)
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
                LOG.info("Success run yardstick netperf_bottlenecks test!")
                out_value = 1
                break
            elif data["status"] == 2:
                LOG.error("Failed run yardstick netperf_bottlenecks test!")
                out_value = 0
                break
    q.put((out_value, func_name))
    return out_value


def config_to_result(num, out_num, during_date, result):
    testdata = {}
    test_result = {}
    test_result["number_of_stacks"] = float(num)
    test_result["success_times"] = out_num
    test_result["success_rate"] = out_num / num
    test_result["duration_time"] = during_date
    test_result["result"] = result
    testdata["data_body"] = test_result
    testdata["testcase"] = testcase
    return testdata


def func_run(condic):
    test_date = do_test()
    return test_date


def run(test_config):
    # con_dic = test_config["load_manager"]
    # test_num = con_dic['scenarios']['num_stack'].split(',')
    # if test_config["contexts"]["yardstick_ip"] is None:
    #     con_dic["contexts"]["yardstick_ip"] =\
    #         conf_parser.ip_parser("yardstick_test_ip")

    # if "dashboard" in test_config["contexts"].keys():
    #     if test_config["contexts"]["dashboard_ip"] is None:
    #         test_config["contexts"]["dashboard_ip"] =\
    #             conf_parser.ip_parser("dashboard")
    #     LOG.info("Create Dashboard data")
    #     DashBoard.posca_stress_ping(test_config["contexts"])

    env_pre(test_config)
    LOG.info("yardstick environment prepare done!")

    # for value in test_num:
    #     result = []
    #     out_num = 0
    #     num = int(value)
    #     # pool = multiprocessing.Pool(processes=num)
    #     threadings = []
    #     LOG.info("begin to run %s thread" % num)

    #     starttime = datetime.datetime.now()

    #     for i in xrange(0, num):
    #         temp_thread = threading.Thread(target=func_run, args=(str(i),))
    #         threadings.append(temp_thread)
    #         temp_thread.start()
    #     for one_thread in threadings:
    #         one_thread.join()
    #     while not q.empty():
    #         result.append(q.get())
    #     for item in result:
    #         out_num = out_num + float(item[0])

    #     endtime = datetime.datetime.now()
    #     LOG.info("%s thread success %d times" % (num, out_num))
    #     during_date = (endtime - starttime).seconds

    #     if out_num >= con_dic["scenarios"]['threshhold']:
    #         criteria_result = "PASS"
    #     else:
    #         criteria_result = "FAIL"

    #     data_reply = config_to_result(num, out_num, during_date,
    #                                   criteria_result)
    #     if "dashboard" in test_config["contexts"].keys():
    #         DashBoard.dashboard_send_data(test_config['contexts'],
    # data_reply)
    #     conf_parser.result_to_file(data_reply, test_config["out_file"])

    #     if criteria_result is "FAIL":
    #         break
    LOG.info('END POSCA life-cycle throuphputs test')
    # return criteria_result
