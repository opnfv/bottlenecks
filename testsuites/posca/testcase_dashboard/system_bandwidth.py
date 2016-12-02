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

config = ConfigParser.ConfigParser()
file_str = "/home/opnfv/bottlenecks/testsuites/posca/testcase_cfg/posca_factor_system_bandwidth.yaml"
with open(file_str, "rd") as cfgfile:
    config.readfp(cfgfile)
    ES_ip_a = config.get("config", "ES_ip")

with IPDB() as ip:
    GATEWAY_IP = ip.routes['default'].gateway
    if ES_ip_a is "":
        ES_ip_a = GATEWAY_IP+":9200"
        print("ES_ip is null get local ip is %s" %(ES_ip_a))

es_ip = ES_ip_a.split(':')
es = Elasticsearch([{'host':es_ip[0]}])
doc={
    "title": "bottlenecks",
    "timeFieldName": "time",
    "fields": "[{\"name\":\"runner_id\",\"type\":\"string\",\"count\":0,\"scripted\":false,\"indexed\":true,\"analyzed\":true,\"doc_values\":false},{\"name\":\"_index\",\"type\":\"string\",\"count\":0,\"scripted\":false,\"indexed\":false,\"analyzed\":false,\"doc_values\":false},{\"name\":\"tx_cache_size\",\"type\":\"number\",\"count\":0,\"scripted\":false,\"indexed\":true,\"analyzed\":false,\"doc_values\":true},{\"name\":\"task_id\",\"type\":\"string\",\"count\":0,\"scripted\":false,\"indexed\":true,\"analyzed\":true,\"doc_values\":false},{\"name\":\"scenarios\",\"type\":\"string\",\"count\":0,\"scripted\":false,\"indexed\":true,\"analyzed\":true,\"doc_values\":false},{\"name\":\"local_cpu_util\",\"type\":\"number\",\"count\":0,\"scripted\":false,\"indexed\":true,\"analyzed\":false,\"doc_values\":true},{\"name\":\"rx_cache_size\",\"type\":\"number\",\"count\":0,\"scripted\":false,\"indexed\":true,\"analyzed\":false,\"doc_values\":true},{\"name\":\"local_transport_retrans\",\"type\":\"number\",\"count\":0,\"scripted\":false,\"indexed\":true,\"analyzed\":false,\"doc_values\":true},{\"name\":\"host\",\"type\":\"string\",\"count\":0,\"scripted\":false,\"indexed\":true,\"analyzed\":true,\"doc_values\":false},{\"name\":\"throughput\",\"type\":\"number\",\"count\":0,\"scripted\":false,\"indexed\":true,\"analyzed\":false,\"doc_values\":true},{\"name\":\"throughput_units\",\"type\":\"string\",\"count\":0,\"scripted\":false,\"indexed\":true,\"analyzed\":true,\"doc_values\":false},{\"name\":\"mean_latency\",\"type\":\"number\",\"count\":0,\"scripted\":false,\"indexed\":true,\"analyzed\":false,\"doc_values\":true},{\"name\":\"tx_msg_size\",\"type\":\"number\",\"count\":0,\"scripted\":false,\"indexed\":true,\"analyzed\":false,\"doc_values\":true},{\"name\":\"version\",\"type\":\"string\",\"count\":0,\"scripted\":false,\"indexed\":true,\"analyzed\":true,\"doc_values\":false},{\"name\":\"deploy_scenario\",\"type\":\"string\",\"count\":0,\"scripted\":false,\"indexed\":true,\"analyzed\":true,\"doc_values\":false},{\"name\":\"pod_name\",\"type\":\"string\",\"count\":0,\"scripted\":false,\"indexed\":true,\"analyzed\":true,\"doc_values\":false},{\"name\":\"target\",\"type\":\"string\",\"count\":0,\"scripted\":false,\"indexed\":true,\"analyzed\":true,\"doc_values\":false},{\"name\":\"rx_msg_size\",\"type\":\"number\",\"count\":0,\"scripted\":false,\"indexed\":true,\"analyzed\":false,\"doc_values\":true},{\"name\":\"installer\",\"type\":\"string\",\"count\":0,\"scripted\":false,\"indexed\":true,\"analyzed\":true,\"doc_values\":false},{\"name\":\"_source\",\"type\":\"_source\",\"count\":0,\"scripted\":false,\"indexed\":false,\"analyzed\":false,\"doc_values\":false},{\"name\":\"time\",\"type\":\"date\",\"count\":0,\"scripted\":false,\"indexed\":true,\"analyzed\":false,\"doc_values\":true},{\"name\":\"remote_cpu_util\",\"type\":\"number\",\"count\":0,\"scripted\":false,\"indexed\":true,\"analyzed\":false,\"doc_values\":true},{\"name\":\"_id\",\"type\":\"string\",\"count\":0,\"scripted\":false,\"indexed\":false,\"analyzed\":false,\"doc_values\":false},{\"name\":\"_type\",\"type\":\"string\",\"count\":0,\"scripted\":false,\"indexed\":false,\"analyzed\":false,\"doc_values\":false},{\"name\":\"_score\",\"type\":\"number\",\"count\":0,\"scripted\":false,\"indexed\":false,\"analyzed\":false,\"doc_values\":false}]"
}

res = es.index(index=".kibana",doc_type="index-pattern",id="bottlenecks",body=doc)
print(res['created'])

doc={
    "buildNum": 10146,
    "defaultIndex": "bottlenecks"
}
res = es.index(index=".kibana",doc_type="config",id="4.6.1",body=doc)
print(res['created'])
doc={
"title": "system_bandwidth",
    "description": "",
    "version": 1,
}
res = es.index(index=".kibana",doc_type="search",id="system_bandwidth",body=doc)
print(res['created'])

doc = {
    "title": "system_bandwidth_line-date",
    "visState": "{\"title\":\"system_bandwidth_line-date\",\"type\":\"line\",\"params\":{\"shareYAxis\":true,\"addTooltip\":true,\"addLegend\":true,\"showCircles\":true,\"smoothLines\":false,\"interpolate\":\"linear\",\"scale\":\"linear\",\"drawLinesBetweenPoints\":true,\"radiusRatio\":9,\"times\":[],\"addTimeMarker\":false,\"defaultYExtents\":false,\"setYExtents\":false,\"yAxis\":{}},\"aggs\":[{\"id\":\"1\",\"type\":\"sum\",\"schema\":\"metric\",\"params\":{\"field\":\"throughput\"}},{\"id\":\"2\",\"type\":\"terms\",\"schema\":\"segment\",\"params\":{\"field\":\"time\",\"size\":100,\"order\":\"asc\",\"orderBy\":\"_term\"}},{\"id\":\"3\",\"type\":\"sum\",\"schema\":\"metric\",\"params\":{\"field\":\"rx_msg_size\"}}],\"listeners\":{}}",
    "uiStateJSON": "{}",
    "description": "",
    "version": 1,
    "kibanaSavedObjectMeta": {
      "searchSourceJSON": "{\"index\":\"bottlenecks\",\"query\":{\"query_string\":{\"query\":\"*\",\"analyze_wildcard\":true}},\"filter\":[]}"
    }
}
res = es.index(
    index=".kibana", doc_type="visualization", id="system_bandwidth_line-date", body=doc)
print(res['created'])

doc = {
    "title": "system_bandwidth_line-char",
    "visState": "{\"title\":\"system_bandwidth_line-char\",\"type\":\"line\",\"params\":{\"shareYAxis\":true,\"addTooltip\":true,\"addLegend\":true,\"showCircles\":true,\"smoothLines\":false,\"interpolate\":\"linear\",\"scale\":\"linear\",\"drawLinesBetweenPoints\":true,\"radiusRatio\":9,\"times\":[],\"addTimeMarker\":false,\"defaultYExtents\":false,\"setYExtents\":false,\"yAxis\":{}},\"aggs\":[{\"id\":\"1\",\"type\":\"sum\",\"schema\":\"metric\",\"params\":{\"field\":\"throughput\"}},{\"id\":\"2\",\"type\":\"terms\",\"schema\":\"segment\",\"params\":{\"field\":\"rx_msg_size\",\"size\":30,\"order\":\"asc\",\"orderBy\":\"_term\"}},{\"id\":\"3\",\"type\":\"terms\",\"schema\":\"group\",\"params\":{\"field\":\"tx_msg_size\",\"size\":30,\"order\":\"desc\",\"orderBy\":\"_term\"}}],\"listeners\":{}}",
    "uiStateJSON": "{}",
    "description": "",
    "version": 1,
    "kibanaSavedObjectMeta": {
      "searchSourceJSON": "{\"index\":\"bottlenecks\",\"query\":{\"query_string\":{\"query\":\"*\",\"analyze_wildcard\":true}},\"filter\":[]}"
    }
}

res = es.index(
    index=".kibana", doc_type="visualization", id="system_bandwidth_line-char", body=doc)
print(res['created'])

doc = {
    "title": "system_bandwidth_terms_data",
    "visState": "{\"title\":\"system_bandwidth_terms_data\",\"type\":\"table\",\"params\":{\"perPage\":80,\"showPartialRows\":false,\"showMeticsAtAllLevels\":false},\"aggs\":[{\"id\":\"1\",\"type\":\"sum\",\"schema\":\"metric\",\"params\":{\"field\":\"throughput\"}},{\"id\":\"4\",\"type\":\"terms\",\"schema\":\"bucket\",\"params\":{\"field\":\"tx_msg_size\",\"size\":200,\"order\":\"asc\",\"orderBy\":\"_term\"}},{\"id\":\"5\",\"type\":\"terms\",\"schema\":\"bucket\",\"params\":{\"field\":\"rx_msg_size\",\"size\":200,\"order\":\"asc\",\"orderBy\":\"_term\"}},{\"id\":\"6\",\"type\":\"terms\",\"schema\":\"bucket\",\"params\":{\"field\":\"mean_latency\",\"size\":5,\"order\":\"asc\",\"orderBy\":\"_term\"}},{\"id\":\"7\",\"type\":\"terms\",\"schema\":\"bucket\",\"params\":{\"field\":\"local_cpu_util\",\"size\":20,\"order\":\"desc\",\"orderBy\":\"_term\"}},{\"id\":\"8\",\"type\":\"terms\",\"schema\":\"bucket\",\"params\":{\"field\":\"remote_cpu_util\",\"size\":5,\"order\":\"desc\",\"orderBy\":\"_term\"}}],\"listeners\":{}}",
    "uiStateJSON": "{}",
    "description": "",
    "version": 1,
    "kibanaSavedObjectMeta": {
      "searchSourceJSON": "{\"index\":\"bottlenecks\",\"query\":{\"query_string\":{\"query\":\"*\",\"analyze_wildcard\":true}},\"filter\":[]}"
    }
}

res = es.index(
    index=".kibana", doc_type="visualization", id="system_bandwidth_terms_data", body=doc)
print(res['created'])

doc = {
    "title": "system_bandwidth_dashboard",
    "hits": 0,
    "description": "",
    "panelsJSON": "[{\"id\":\"system_bandwidth_line-char\",\"type\":\"visualization\",\"panelIndex\":3,\"size_x\":7,\"size_y\":4,\"col\":1,\"row\":1},{\"id\":\"system_bandwidth_line-date\",\"type\":\"visualization\",\"panelIndex\":4,\"size_x\":7,\"size_y\":4,\"col\":1,\"row\":5},{\"id\":\"system_bandwidth_terms_data\",\"type\":\"visualization\",\"panelIndex\":5,\"size_x\":5,\"size_y\":8,\"col\":8,\"row\":1}]",
    "optionsJSON": "{\"darkTheme\":false}",
    "uiStateJSON": "{}",
    "version": 1,
    "kibanaSavedObjectMeta": {
      "searchSourceJSON": "{\"filter\":[{\"query\":{\"query_string\":{\"query\":\"*\",\"analyze_wildcard\":true}}}]}"
    }
}

res = es.index(
    index=".kibana", doc_type="dashboard", id="system_bandwidth_dashboard", body=doc)
print(res['created'])
