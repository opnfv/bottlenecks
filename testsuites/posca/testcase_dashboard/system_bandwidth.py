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
from pyroute2 import IPDB
import json

config = ConfigParser.ConfigParser()

dashboard_dir = "/home/opnfv/bottlenecks/testsuites/posca\
/testcase_dashboard/"
file_str = "/home/opnfv/bottlenecks/testsuites/posca/\
testcase_cfg/posca_factor_system_bandwidth.yaml"

with open(file_str, "rd") as cfgfile:
    config.readfp(cfgfile)
    ES_ip_a = config.get("config", "ES_ip")

with IPDB() as ip:
    GATEWAY_IP = ip.routes['default'].gateway
    if ES_ip_a is "":
        ES_ip_a = GATEWAY_IP + ":9200"
        print("ES_ip is null get local ip is %s" % (ES_ip_a))

es_ip = ES_ip_a.split(':')
es = Elasticsearch([{'host': es_ip[0]}])

# Create bottlenecks index
with open(dashboard_dir + 'posca_system_bandwidth\
_index_pattern.json') as index_pattern:
    doc = json.load(index_pattern)
res = es.index(
    index=".kibana",
    doc_type="index-pattern",
    id="bottlenecks",
    body=doc)
if res['created'] == "True":
    print("bottlenecks index-pattern has created")
else:
    print("bottlenecks index-pattern has existed")

with open(dashboard_dir + 'posca_system_bandwidth\
_config.json') as index_config:
    doc = json.load(index_config)
res = es.index(index=".kibana", doc_type="config", id="4.6.1", body=doc)
if res['created'] == "True":
    print("bottlenecks config has created")
else:
    print("bottlenecks config has existed")

# Configure discover panel
with open(dashboard_dir + 'posca_system_bandwidth\
_discover.json') as index_discover:
    doc = json.load(index_discover)
res = es.index(
    index=".kibana",
    doc_type="search",
    id="system_bandwidth",
    body=doc)
if res['created'] == "True":
    print("system_bandwidth search has created")
else:
    print("system_bandwidth search has existed")

# Create testing data in line graph
with open(dashboard_dir + 'posca_system_bandwidth\
_line_data.json') as line_data:
    doc = json.load(line_data)
res = es.index(
    index=".kibana",
    doc_type="visualization",
    id="system_bandwidth_line-date",
    body=doc)
if res['created'] == "True":
    print("system_bandwidth_line-date visualization has created")
else:
    print("system_bandwidth_line-date visualization has existed")

# Create comparison results in line chart
with open(dashboard_dir + 'posca_system_bandwidth\
_line_char.json') as line_char:
    doc = json.load(line_char)
res = es.index(
    index=".kibana",
    doc_type="visualization",
    id="system_bandwidth_line-char",
    body=doc)
if res['created'] == "True":
    print("system_bandwidth_line-char visualization has created")
else:
    print("system_bandwidth_line-char visualization has existed")

# Create monitoring data in table
with open(dashboard_dir + 'posca_system_bandwidth\
_terms_data.json') as terms_char:
    doc = json.load(terms_char)
res = es.index(index=".kibana", doc_type="visualization",
               id="system_bandwidth_terms_data", body=doc)
if res['created'] == "True":
    print("system_bandwidth_terms_data visualization has created")
else:
    print("system_bandwidth_terms_data visualization has existed")

# Create dashboard
with open(dashboard_dir + 'posca_system_bandwidth\
_dashboard.json') as dashboard:
    doc = json.load(dashboard)
res = es.index(
    index=".kibana",
    doc_type="dashboard",
    id="system_bandwidth_dashboard",
    body=doc)
if res['created'] == "True":
    print("system_bandwidth dashboard has created")
else:
    print("system_bandwidth dashboard has existed")
