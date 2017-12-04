#!/usr/bin/python
##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import ConfigParser
from elasticsearch import Elasticsearch
import json
import os
import utils.logger as log
from utils.parser import Parser as conf_parser

LOG = log.Logger(__name__).getLogger()
config = ConfigParser.ConfigParser()
es = Elasticsearch()
dashboard_path = os.path.join(conf_parser.test_dir,
                              "posca",
                              "testcase_dashboard")
dashboard_dir = dashboard_path + "/"


def dashboard_send_data(runner_config, test_data):
    global es
    test_data=[{"number": 4, 'sequence': 1}, {"number": 4, 'DropPercentage': 45.42038, 'RxThroughput': 4894.3, 'TxThroughput': 8967.266666666666, 'sequence': 2}, {"number": 4, 'DropPercentage': 80.3581, 'RxThroughput': 5738.0, 'TxThroughput': 29213.066666666666, 'sequence': 3}, {"number": 4, 'DropPercentage': 89.28239, 'RxThroughput': 2330.266666666667, 'TxThroughput': 21742.4, 'sequence': 4}, {"number": 4, 'DropPercentage': 25.33739, 'RxThroughput': 5336.833333333333, 'TxThroughput': 7147.933333333333, 'sequence': 5}, {"number": 4, 'DropPercentage': 72.1948, 'RxThroughput': 3380.0, 'TxThroughput': 12156.0, 'sequence': 6}, {"number": 4, 'DropPercentage': 73.75576, 'RxThroughput': 6177.5, 'TxThroughput': 23538.5, 'sequence': 7}, {"number": 4, 'DropPercentage': 84.61534, 'RxThroughput': 8082.9, 'TxThroughput': 52538.7, 'sequence': 8}, {"number": 4, 'DropPercentage': 86.94804, 'RxThroughput': 14515.033333333333, 'TxThroughput': 111209.56666666667, 'sequence': 9}, {"number": 4, 'DropPercentage': 84.45409, 'RxThroughput': 15608.933333333332, 'TxThroughput': 100405.43333333333, 'sequence': 10}]
    # es_ip = runner_config['dashboard_ip'].split(':')
    es = Elasticsearch([{'host': "172.17.0.5"}])
    for i in test_data:
        res = es.index(index="bottlenecks",
                       doc_type="vnf_scale_out",
                       body=i)
        if res['created'] == "False":
            LOG.error("date send to kibana have errors ", test_data["data_body"])

