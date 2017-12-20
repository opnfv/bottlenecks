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
    # es_ip = runner_config['dashboard_ip'].split(':')
    es = Elasticsearch([{'host': "172.17.0.5"}])
    for i in test_data:
        res = es.index(index="bottlenecks",
                       doc_type="vnf_scale_out",
                       body=i)
        if res['created'] == "False":
            LOG.error("date send to kibana have errors %s",
                      test_data["data_body"])
