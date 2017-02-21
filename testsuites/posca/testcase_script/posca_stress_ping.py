#!/usr/bin/env python
##############################################################################
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
'''This file realize the function of run posca ping stress test script
This file contain several part:
Frist is create a script to realize several threading run'''

import utils.logger as log
import uuid
import json
import os
import multiprocessing
import docker
import datetime
from utils.parser import Parser as conf_parser
import utils.env_prepare.quota_prepare as quota_prepare
import utils.env_prepare.stack_prepare as stack_prepare
import testsuites.posca.testcase_dashboard.posca_stress_ping as DashBoard
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
        "testcase": "ping_bottlenecks"
    }
}
testfile = os.path.basename(__file__)
testcase, file_format = os.path.splitext(testfile)


def env_pre(con_dic):
    stack_prepare._prepare_env_daemon()
    quota_prepare.quota_env_prepare()
    client = docker.from_env()
    con = client.containers.get('bottleneckcompose_yardstick_1')
    cmd = ('yardstick env prepare')
    LOG.info("yardstick envrionment prepare!")
    stdout = con.exec_run(cmd)
    LOG.debug(stdout)


def do_test(test_config, con_dic):
    out_file = ("/tmp/yardstick_" + str(uuid.uuid4()) + ".out")
    client = docker.from_env()
    con = client.containers.get('bottleneckcompose_yardstick_1')
    cmd = ('yardstick task start /home/opnfv/repos/yardstick/'
           'samples/ping_bottlenecks.yaml --output-file ' + out_file)
    stdout = con.exec_run(cmd)
    LOG.debug(stdout)
    with open(out_file) as f:
        data = json.load(f)
        if data["status"] == 1:
            LOG.info("yardstick run success")
            out_value = 1
        else:
            LOG.error("yardstick error exit")
            out_value = 0
    os.remove(out_file)
    return out_value


def config_to_result(num, out_num, during_date):
    testdata = {}
    test_result = {}
    test_result["number_of_users"] = float(num)
    test_result["success_times"] = out_num
    test_result["success_rate"] = out_num / num
    test_result["duration_time"] = during_date
    testdata["data_body"] = test_result
    testdata["testcase"] = testcase
    return testdata


def func_run(condic):
    test_config = {}
    test_date = do_test(test_config, condic)
    return test_date


def run(test_config):
    con_dic = test_config["load_manager"]
    test_num = con_dic['scenarios']['num_stack'].split(',')
    if con_dic["contexts"]["yardstick_test_ip"] is None:
        con_dic["contexts"]["yardstick_test_ip"] =\
            conf_parser.ip_parser("yardstick_test_ip")

    if test_config["dashboard"]["dashboard"] == 'y':
        if test_config["dashboard"]["dashboard_ip"] is None:
            test_config["dashboard"]["dashboard_ip"] =\
                conf_parser.ip_parser("dashboard")
        LOG.info("Create Dashboard data")
        DashBoard.posca_stress_ping(test_config["dashboard"])

    LOG.info("bottlenecks envrionment prepare!")
    env_pre(con_dic)
    LOG.info("yardstick envrionment prepare done!")

    for value in test_num:
        result = []
        out_num = 0
        num = int(value)
        pool = multiprocessing.Pool(processes=num)
        LOG.info("begin to run %s thread" % num)

        starttime = datetime.datetime.now()
        for i in range(0, int(num)):
            result.append(pool.apply_async(func_run, (con_dic, )))
        pool.close()
        pool.join()
        for res in result:
            out_num = out_num + float(res.get())

        endtime = datetime.datetime.now()
        LOG.info("%s thread success %d times" % (num, out_num))
        during_date = (endtime - starttime).seconds

        data_reply = config_to_result(num, out_num, during_date)
        if test_config['dashboard']['dashboard'] == 'y':
            DashBoard.dashboard_send_data(test_config['dashboard'], data_reply)
        conf_parser.result_to_file(data_reply, test_config["out_file"])

        if out_num < num:
            success_rate = ('%d/%d' % (out_num, num))
            LOG.error('error thread: %d '
                      'the successful rate is %s'
                      % (num - out_num, success_rate))
            break
    LOG.info('END POSCA stress ping test')
