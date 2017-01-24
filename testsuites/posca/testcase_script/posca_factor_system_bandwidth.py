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
# --------------------------------------------------
# logging configuration
# --------------------------------------------------
LOG = log.Logger(__name__)

test_dict = {
    "action": "runTestCase",
    "args": {
        "opts": {
            "task-args": {}
        },
        "testcase": "netperf_bottlenecks"
    }
}


def env_pre():
    Runner.Create_Incluxdb()


def do_test(test_config, con_dic):
    test_dict['args']['opts']['task-args'] = test_config
    Task_id = Runner.Send_Data(test_dict, con_dic['runner_config'])
    time.sleep(con_dic['test_config']['test_time'])
    Data_Reply = Runner.Get_Reply(con_dic['runner_config'], Task_id)
    test_date = Data_Reply[con_dic['runner_config']['testcase']][0]
    return test_date


def run(con_dic):
    data = {}
    rx_pkt_a = con_dic['test_config']['rx_pkt_sizes'].split(',')
    tx_pkt_a = con_dic['test_config']['tx_pkt_sizes'].split(',')
    data["rx_pkt_sizes"] = rx_pkt_a
    data["tx_pkt_sizes"] = tx_pkt_a
    con_dic["result_file"] = os.path.dirname(
        os.path.abspath(__file__)) + "/test_case/result"
    date_id = 0
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
            test_config = {
                "tx_msg_size": float(test_x),
                "rx_msg_size": float(test_y),
                "test_time": con_dic['test_config']['test_time']
            }
            date_id = date_id + 1
            data_reply = do_test(test_config, con_dic)
            bandwidth = float(data_reply["throughput"])
            if (data_max["throughput"] < bandwidth):
                data_max = data_reply
            if (abs(bandwidth_tmp - bandwidth) / bandwidth_tmp < 0.025):
                print(pre_reply)
                break
            else:
                pre_reply = data_reply
                bandwidth_tmp = bandwidth
        cur_role_result = float(pre_reply["throughput"])
        if (abs(pre_role_result - cur_role_result) / pre_role_result < 0.025):
            print("date_id is %d,package return at line 111\n" % date_id)
        if data_return["throughput"] < data_max["throughput"]:
            data_return = data_max
        pre_role_result = cur_role_result
    print("date_id is %d,id return success\n" % date_id)
    return data_return


def main():
    run(con_dic)


if __name__ == '__main__':
    main()

