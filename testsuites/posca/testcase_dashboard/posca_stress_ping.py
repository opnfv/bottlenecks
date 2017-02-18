#!/usr/bin/python
##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
'''This file realize a function of creating dashboard of stress ping test'''
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
    es_ip = runner_config['dashboard_ip'].split(':')
    es = Elasticsearch([{'host': es_ip[0]}])
    res = es.index(index="bottlenecks",
                   doc_type=test_data["testcase"],
                   body=test_data["data_body"])
    if res['created'] == "False":
        LOG.error("date send to kibana have errors ", test_data["data_body"])


def posca_stress_ping(runner_config):
    global es
    es_ip = runner_config['dashboard_ip'].split(':')
    es = Elasticsearch([{'host': es_ip[0]}])
    # Create bottlenecks index
    with open(dashboard_dir + 'posca_stress_ping_index_pattern.json')\
            as index_pattern:
        doc = json.load(index_pattern)
    res = es.index(
        index=".kibana",
        doc_type="index-pattern",
        id="bottlenecks",
        body=doc)
    if res['created'] == "True":
        LOG.info("bottlenecks index-pattern has created")
    else:
        LOG.info("bottlenecks index-pattern has existed")

    with open(dashboard_dir + 'posca_system_bandwidth_config.json')\
            as index_config:
        doc = json.load(index_config)
    res = es.index(index=".kibana", doc_type="config", id="4.6.1", body=doc)
    if res['created'] == "True":
        LOG.info("bottlenecks config has created")
    else:
        LOG.info("bottlenecks config has existed")

    # Configure discover panel
    with open(dashboard_dir + 'posca_stress_ping_discover.json')\
            as index_discover:
        doc = json.load(index_discover)
    res = es.index(
        index=".kibana",
        doc_type="search",
        id="posca_stress_ping",
        body=doc)
    if res['created'] == "True":
        LOG.info("posca_stress_ping search has created")
    else:
        LOG.info("posca_stress_ping search has existed")

    # Create testing data in line graph
    with open(dashboard_dir + 'posca_stress_ping_histogram.json')\
            as line_data:
        doc = json.load(line_data)
    res = es.index(
        index=".kibana",
        doc_type="visualization",
        id="posca_stress_ping_histogram",
        body=doc)
    if res['created'] == "True":
        LOG.info("posca_stress_ping visualization has created")
    else:
        LOG.info("posca_stress_ping visualization has existed")

    # Create comparison results in line chart
    with open(dashboard_dir + 'posca_stress_ping_table.json')\
            as line_char:
        doc = json.load(line_char)
    res = es.index(
        index=".kibana",
        doc_type="visualization",
        id="posca_stress_ping_table",
        body=doc)
    if res['created'] == "True":
        LOG.info("posca_stress_ping visualization has created")
    else:
        LOG.info("posca_stress_ping visualization has existed")

    # Create dashboard
    with open(dashboard_dir + 'posca_stress_ping_dashboard.json')\
            as dashboard:
        doc = json.load(dashboard)
    res = es.index(
        index=".kibana",
        doc_type="dashboard",
        id="posca_stress_ping",
        body=doc)
    if res['created'] == "True":
        LOG.info("posca_stress_ping dashboard has created")
    else:
        LOG.info("posca_stress_ping dashboard has existed")
