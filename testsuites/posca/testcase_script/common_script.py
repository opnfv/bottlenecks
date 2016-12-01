#!/usr/bin/env python
##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import json
import requests
import time
import subprocess as sub
from pyroute2 import IPDB
import sys

headers = {"Content-Type": "application/json"}


def posca_tran_data(ES_ip, file_name):
        p = sub.Popen(['curl', '-s', '-XPOST', "%s/_bulk" % ES_ip,
                       '--data-binary', "@" + file_name], stdout=sub.PIPE)
        for line in iter(p.stdout.readline, b''):
            ret_dict = json.loads(line)
            if not ret_dict['errors']:
                print("INFO: %6s lines no errors, total cost %d ms."
                      % (len(ret_dict['items']), ret_dict['took']))
                return len(ret_dict['items'])
            else:
                print("ERROR: %6s lines have errors, total cost %d ms."
                      % (len(ret_dict['items']), ret_dict['took']))


def posca_config_read(config_str, con_str, config):
    print("========== posca system bandwidth config read ===========")
    con_dic = {}
    print(config_str)
    idx = 0
    with open(config_str, "rd") as cfgfile:
        config.readfp(cfgfile)
        while idx < len(con_str):
            con_dic[str(con_str[idx])] = \
                            config.get("config", str(con_str[idx]))
            idx += 1
    with IPDB() as ip:
        GATEWAY_IP = ip.routes['default'].gateway
    if str(con_dic["test_ip"]) is "":
        con_dic["test_ip"] = GATEWAY_IP+":3333"
        print("test_ip is null get local ip is %s" %(con_dic["test_ip"]))
    if con_dic["ES_ip"] is "":
        con_dic["ES_ip"] = GATEWAY_IP+":9200"
        print("ES_ip is null get local ip is %s" %(con_dic["ES_ip"]))
    return con_dic


def posca_output_result(file_config, data_reply):
    data_head = {}
    data_head["index"] = {}
    data_head["index"]["_index"] = "bottlenecks"
    data_head["index"]["_type"] = file_config["test_type"]
    data_head["index"]["_id"] = file_config["test_id"]

    data_reply["throughput"] = float(data_reply["throughput"])
    data_reply["mean_latency"] = float(data_reply["mean_latency"])
    data_reply["remote_cpu_util"] = float(data_reply["remote_cpu_util"])
    data_reply["local_cpu_util"] = float(data_reply["local_cpu_util"])
    data_reply["local_transport_retrans"] =\
        float(data_reply["local_transport_retrans"])
    with open(file_config["file_path"], "a") as f:
        f.write(json.dumps(data_head, f))
        f.write("\n")
        f.write(json.dumps(data_reply, f))
        f.write("\n")
        f.close()


def posca_get_reply(con_dic, task_id, time_test=1):
    reply_url = "http://%s/yardstick/results?action=getResult&task_id=%s\
&measurement=tc100" % (con_dic["test_ip"], task_id)
    time.sleep(float(con_dic["test_time"]))
    reply_response = requests.get(reply_url)
    reply_data = json.loads(reply_response.text)
    print(reply_data)
    if reply_data["status"] == 1:
        return(reply_data["result"][0])
    if reply_data["status"] == 0:
        if time_test == 10:
            print("yardstick time out")
            sys.exit()
        posca_get_reply(con_dic, task_id, time_test=time_test+1)
    if reply_data["status"] == 2:
        print("yardstick error exit")
        sys.exit()


def posca_send_data(con_dic, test_config, file_config):
    base_url = "http://%s/yardstick/testcases/release/action" % (con_dic['test_ip'])
    print(con_dic["test_ip"])
    test_dict = {
            "action":"runTestCase",
            "args":{
                "opts": {
                    "task-args": {
                        'tx_msg_size': '%s' % str(test_config["tx_msg_size"]),
                        'rx_msg_size': '%s' % str(test_config["rx_msg_size"]),
                        'test_time': '%s' % str(int(con_dic["test_time"]) - 20),
                        'host': 'node3.LF',
                        'target': 'node4.LF'
                        }
                 },
                 "testcase":"tc100"
            }
    }
    reponse = requests.post(
                        base_url, data=json.dumps(test_dict), headers=headers)
    ask_data = json.loads(reponse.text)
    task_id = ask_data["result"]
    print(task_id)
    data_reply = posca_get_reply(con_dic, task_id)
    data_reply.update(test_config)
    posca_output_result(file_config, data_reply)
    return data_reply


def posca_create_incluxdb(con_dic):
    base_url = "http://%s/yardstick/env/action" % (con_dic['test_ip'])
    test_dict = {
            "action":"createInfluxDBContainer",
    }
    reponse = requests.post(
                        base_url, data=json.dumps(test_dict), headers=headers)

