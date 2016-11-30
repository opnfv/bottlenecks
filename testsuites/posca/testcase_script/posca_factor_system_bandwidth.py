#!/usr/bin/env python
##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import os
import argparse
import time
import logging
import ConfigParser
import common_script
import datetime
import subprocess

# ------------------------------------------------------
# parser for configuration files in each test case
# ------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--conf",
                    help="configuration files for the testcase,\
                        in yaml format",
                    default="/home/opnfv/bottlenecks/testsuites/posca\
/testcase_cfg/posca_factor_system_bandwidth.yaml")
args = parser.parse_args()
headers = {"Content-Type": "application/json"}
INTERPRETER = "/usr/bin/python"


# --------------------------------------------------
# logging configuration
# --------------------------------------------------
logger = logging.getLogger(__name__)


def posca_env_check():
    print("========== posca system bandwidth env check ===========")
    filepath = r"/home/opnfv/bottlenecks/testsuites/posca/test_result/"
    if os.path.exists(filepath):
        return True
    else:
        os.mkdir(r'/home/opnfv/bottlenecks/testsuites/posca/test_result/')


def system_pkt_bandwidth(test_id, data, file_config, con_dic):
    date_id = test_id
    print("package test is is begin from %d" % test_id)
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
                    }
            date_id = date_id + 1
            file_config["test_id"] = date_id
            data_reply = common_script.posca_send_data(
                   con_dic, test_config, file_config)
            bandwidth = data_reply["throughput"]
            if (data_max["throughput"] < bandwidth):
                data_max = data_reply
            if (abs(bandwidth_tmp - bandwidth)/bandwidth_tmp < 0.025):
                print(pre_reply)
                break
            else:
                pre_reply = data_reply
                bandwidth_tmp = bandwidth
        cur_role_result = pre_reply["throughput"]
        if (abs(pre_role_result - cur_role_result)/pre_role_result < 0.025):
            print("date_id is %d,package return at line 111\n" % date_id)
            # return data_return
        if data_return["throughput"] < data_max["throughput"]:
            data_return = data_max
        pre_role_result = cur_role_result
    print("date_id is %d,id return success\n" % date_id)
    return data_return


def posca_run(con_dic):
    print("========== run posca system bandwidth ===========")
    test_con_id = 0
    file_config = {}
    data = {}
    rx_pkt_s_a = con_dic['rx_pkt_sizes'].split(',')
    tx_pkt_s_a = con_dic['tx_pkt_sizes'].split(',')
    time_new = time.strftime('%H_%M', time.localtime(time.time()))
    file_config["file_path"] = "/home/opnfv/bottlenecks/testsuites/posca/\
test_result/factor_system_system_bandwidth_%s.json" % (time_new)
    file_config["test_type"] = "system_bandwidth_biggest"
    data["rx_pkt_sizes"] = rx_pkt_s_a
    data["tx_pkt_sizes"] = tx_pkt_s_a
    print("######test package begin######")
    pkt_reply = system_pkt_bandwidth(
        test_con_id, data, file_config, con_dic)

    print("######find system bandwidth######")
    print("rx_msg_size:%d  tx_msg_size:%d\n" %
          (pkt_reply["rx_msg_size"], pkt_reply["tx_msg_size"]))
    date_tran = common_script.posca_tran_data(
                            con_dic['ES_ip'], file_config["file_path"])
    return True


def main():
    if not (args.conf):
        logger.error("Configuration files do not exist for \
                    the specified testcases")
        os.exit(-1)
    else:
        testcase_cfg = args.conf

    con_str = [
            'test_ip', 'tool', 'test_time', 'protocol',
            'tx_pkt_sizes', 'rx_pkt_sizes', 'cpu_load',
            'latency', 'ES_ip', 'dashboard'
    ]
    starttime = datetime.datetime.now()
    config = ConfigParser.ConfigParser()
    con_dic = common_script.posca_config_read(testcase_cfg, con_str, config)
    common_script.posca_create_incluxdb(con_dic)
    posca_env_check()
    posca_run(con_dic)
    endtime = datetime.datetime.now()
    if con_dic["dashboard"] == "y":
        cmd = '/home/opnfv/bottlenecks/testsuites/posca/testcase_dashboard/\
system_bandwidth.py'
        pargs = [INTERPRETER, cmd]
        print("Begin to establish dashboard, False means already exist.\n")
        sub_result = subprocess.Popen(pargs)
        sub_result.wait()
    print("System Bandwidth testing time : %s" %(endtime - starttime))
    time.sleep(5)

if __name__ == '__main__':
    main()

