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
import json

#------------------------------------------------------
# parser for configuration files in each test case
# ------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--conf",
                    help="configuration files for the testcase, in yaml format",
                    default="/home/opnfv/bottlenecks/testsuites/posca/testcase_cfg/posca_factor_system_bandwidth.yaml")
args = parser.parse_args()

cmd="curl -i"
order_arg="-H \"Content-Type: application/json\" -X POST -d \'{\"cmd\": \"start\", \"opts\":{\"output-file\": \"/tem/yardstick.out\"}, \"args\": \"../samples/netperf.yaml\"}'"

#--------------------------------------------------
# logging configuration
#--------------------------------------------------
logger = logging.getLogger(__name__)

def posca_env_check():
    print "========== posca system bandwidth env check ==========="
    if os.path.exists(r'/home/opnfv/bottlenecks/testsuites/posca/test_result/'):
        return True 
    else:
        os.mkdirs(r'/home/opnfv/bottlenecks/testsuites/posca/test_result/')

def posca_output_result(time_new,input_1,input_2,input_3,input_4,input_5,input_6):
    save_dic={}
    save_dic['tx_pkt_size']=input_1
    save_dic['rx_cache_size']=input_2
    save_dic['tx_cache_size']=input_3
    save_dic['throughput ']=input_4
    save_dic['latency']=input_5
    save_dic['cpu_load']=input_6
    with open("/home/opnfv/bottlenecks/testsuites/posca/test_result/factor_system_bandwidth_%s.json"%(time_new),"a") as f:
        f.write(json.dumps(save_dic,f))
        f.write("\n")

def posca_config_read(config_str):
    print "========== posca system bandwidth config read ==========="
    
    con_dic = {}
    config = ConfigParser.ConfigParser()
    with open(config_str,"rd") as cfgfile:
        config.readfp(cfgfile)
        con_dic['test_ip']=config.get("config","test_ip")
        con_dic['test_tool']=config.get("config","tool")
        con_dic['test_time']=config.get("config","test_time")
        con_dic['test_protocol']=config.get("config","protocol")
        con_dic['test_tx_pkt_s']=config.get("config","tx pkt sizes")
        con_dic['test_rx_pkt_s']=config.get("config","rx pkt sizes")
        con_dic['test_tx_cache_s']=config.get("config","tx cache sizes")
        con_dic['test_rx_cache_s']=config.get("config","rx cache sizes")
        con_dic['test_cpu_load']=config.get("config","cpu load")
        con_dic['test_latency']=config.get("config","latency")

    return con_dic

def posca_run(con_dic):
    print "========== run posca system bandwidth ==========="

    test_tx_pkt_s_a = con_dic['test_tx_pkt_s'].split(',')
 #   test_rx_pkt_s_a = con_dic['test_rx_pkt_s'].split(',')
    test_tx_cache_s_a = con_dic['test_tx_cache_s'].split(',')
    test_rx_cache_s_a = con_dic['test_rx_cache_s'].split(',')
    time_new = time.strftime('%H_%M',time.localtime(time.time()))
    bandwidth_tmp = 1
    
    for test_rx_cache_s_e in test_rx_cache_s_a:
        for test_tx_cache_s_e in test_tx_cache_s_a:
            for test_tx_pkt_s_e in test_tx_pkt_s_a:
                print "%s,%s,%s"%(test_tx_pkt_s_e,test_rx_cache_s_e,test_tx_cache_s_e)
                order_excute = os.popen("%s %s http://%s/api/v3/yardstick/tasks/task %s %s %s"%(cmd,order_arg,con_dic['test_ip'],test_tx_pkt_s_e,test_rx_cache_s_e,test_tx_cache_s_e))
                order_result = order_excute.read()
                test_id = order_result.find("task_id")
                time.sleep(con_dic['test_time'])                
                cmd_excute = os.popen( "%s http://%s/api/v3/yardstick/testresults?task_id=%s"%(cmd,con_dic['test_ip'],test_id))
                test_result = cmd_excute.read()
                bandwidth = test_result.find("bandwidth")
                cpu_load = test_result.find("cpu_load")
                latency = test_result.find("latency")
                posca_output_result(time_new,test_tx_pkt_s_e,test_rx_cache_s_e,test_tx_cache_s_e,bandwidth,latency,cpu_load)
                if (cpu_load < con_dic['test_cpu_load']) and (latency < con_dic['test_latency']):
                    if (abs(bandwidth_tmp-bandwidth)/bandwidth <0.05):
                        print "%s,%s,%s,%s,%s,%s"%(test_tx_pkt_s_e,test_rx_cache_s_e,test_tx_cache_s_e,bandwidth,latency,cpu_load)
                        return True
                    else:
                        bandwidth_tmp = bandwidth
                        return False
                else:
                    print "%s,%s,%s,%s,%s,%s"%(test_tx_pkt_s_e,test_rx_cache_s_e,test_tx_cache_s_e,bandwidth,latency,cpu_load)
                    return True


def main():
    if not (args.conf):
       logger.error("Configuration files do not exist for the specified testcases")
       exit(-1)
    else:
       testcase_cfg = args.conf

    con_dic=posca_config_read(testcase_cfg)
    posca_env_check()
    posca_run(con_dic)

    time.sleep(5)

if __name__=='__main__':
    main()
