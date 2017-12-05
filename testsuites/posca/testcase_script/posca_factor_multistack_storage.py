#!/usr/bin/env python
##############################################################################
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
'''This file realize the function of run posca multistack storage stress test
This file contain several part:
First is create a script to realize several threading run'''

import utils.logger as log
import uuid
import json
import os
import time
import threading
import datetime
import Queue
from utils.parser import Parser as conf_parser
import utils.env_prepare.quota_prepare as quota_prepare
import utils.env_prepare.stack_prepare as stack_prepare
import utils.infra_setup.runner.yardstick as yardstick_task

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
        "testcase": "multistack_storage_bottlenecks"
    }
}
testfile = os.path.basename(__file__)
testcase, file_format = os.path.splitext(testfile)
cidr = "/home/opnfv/repos/yardstick/samples/storage_bottlenecks.yaml"
runner_DEBUG = True
q = Queue.Queue()
final_result = Queue.Queue()


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


def testcase_parser(out_file="yardstick.out", **parameter_info):
    cmd = yardstick_task.yardstick_command_parser(debug=runner_DEBUG,
                                                  cidr=cidr,
                                                  outfile=out_file,
                                                  parameter=parameter_info)
    return cmd


def do_test(test_config):
    out_file = ("/tmp/yardstick_" + str(uuid.uuid4()) + ".out")
    yardstick_container = docker_env.yardstick_info['container']
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
                LOG.info("%s" % data["result"]["testcases"])
                break
            elif data["status"] == 2:
                LOG.error("yardstick error exit")
                break

    save_data = final_config_to_result(test_config, data)
    return save_data


def config_to_result(num, out_num, during_date, date, result):
    testdata = {}
    test_result = {}
    final_data = {}

    final_data["read_iops"] = 0
    final_data["read_bw"] = 0
    final_data["read_lat"] = 0
    final_data["write_iops"] = 0
    final_data["write_bw"] = 0
    final_data["write_lat"] = 0

    test_result["number_of_stacks"] = float(num)
    test_result["success_times"] = out_num
    test_result["success_rate"] = out_num / num
    test_result["duration_time"] = during_date
    test_result["current_date"] = date
    test_result["result"] = result
    testdata["data_body"] = test_result
    testdata["testcase"] = testcase

    while(final_result.fsize()):
        data = final_result.get()
        final_data["read_iops"] += data["read_iops"]
        final_data["read_bw"] += data["read_bw"]
        final_data["read_lat"] += data["read_lat"]
        final_data["write_iops"] += data["write_iops"]
        final_data["write_bw"] += data["read_iops"]
        final_data["write_lat"] += data["read_iops"]

    testdata["test_value"] = final_data
    LOG.info("Final testdata is %s" % testdata)
    return testdata


def final_config_to_result(test_config, test_result):
    print(test_result)
    out_data = test_result["result"]["testcases"]
    test_data = out_data["storage_bottlenecks"]["tc_data"]
    for result in test_data:
        testdata = {}
        testdata["read_iops"] = result["data"]["read_iops"]
        testdata["read_bw"] = result["data"]["read_bw"]
        testdata["read_lat"] = result["data"]["read_lat"]
        testdata["write_iops"] = result["data"]["write_iops"]
        testdata["write_bw"] = result["data"]["write_bw"]
        testdata["write_lat"] = result["data"]["write_lat"]
        final_result.put(testdata)
    return testdata


def func_run(con_dic):
    test_date = do_test(con_dic)
    return test_date


def run(test_config):
    con_dic = test_config["load_manager"]
    scenarios_conf = con_dic["scenarios"]

    if test_config["contexts"]["yardstick_ip"] is None:
        con_dic["contexts"]["yardstick_ip"] =\
            conf_parser.ip_parser("yardstick_test_ip")

    env_pre(test_config)
    LOG.info("yardstick environment prepare done!")

    test_num = conf_parser.str_to_list(scenarios_conf["num_stack"])
    rw = conf_parser.str_to_list(scenarios_conf["rw"])
    bs = conf_parser.str_to_list(scenarios_conf["bs"])
    size = scenarios_conf["size"]
    rwmixwrite = scenarios_conf["rwmixwrite"]
    numjobs = scenarios_conf["num_jobs"]
    direct = scenarios_conf["direct"]

    for value in test_num:
        result = []
        out_num = 0
        num = int(value)
        # pool = multiprocessing.Pool(processes=num)
        threadings = []
        LOG.info("begin to run %s thread" % num)

        starttime = datetime.datetime.now()

        for i in xrange(0, num):
            case_config = {"stack_num": value,
                           "volume_num": 1,
                           "rw": rw,
                           "bs": bs,
                           "size": size,
                           "rwmixwrite": rwmixwrite,
                           "numjobs": numjobs,
                           "direct": direct}
            tmp_thread = threading.Thread(target=func_run, args=(case_config,))
            threadings.append(tmp_thread)
            tmp_thread.start()

        for one_thread in threadings:
            one_thread.join()
        while not q.empty():
            result.append(q.get())
        for item in result:
            out_num = out_num + float(item[0])

        endtime = datetime.datetime.now()
        LOG.info("%s thread success %d times" % (num, out_num))
        during_date = (endtime - starttime).seconds
        current_date = datetime.datetime.now()

        if out_num >= con_dic["scenarios"]['threshhold']:
            criteria_result = "PASS"
        else:
            criteria_result = "FAIL"

        data_reply = config_to_result(num, out_num, during_date,
                                      current_date, criteria_result)
        conf_parser.result_to_file(data_reply, test_config["out_file"])

        if criteria_result is "FAIL":
            break
    LOG.info('END POSCA stress multistack storage test')
    return criteria_result
