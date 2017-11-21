##############################################################################
# Copyright (c) 2017 Huawei Tech and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import logging
import socket
import requests
from oslo_serialization import jsonutils


logger = logging.getLogger(__name__)


def _create_dashboard(ip, port, path):
    url = 'http://admin:admin@{}:{}/api/dashboards/db'.format(ip, port)
    logger.info("Fetched IP for dashboard creation!")
    with open(path) as f:
        data = jsonutils.load(f)
    try:
        post(url, {"dashboard": data})
        logger.info( "Trying to post dashboard json!")
    except Exception:
        logger.info("Create dashboard failed")
        raise


def _create_data_source(ip, port):
    url = 'http://admin:admin@{}:{}/api/datasources'.format(ip, port)
    logger.info("Fetched URL for datasource")
    data = {
        "name": "automated-ds",
        "type": "prometheus",
        "access": "direct",
        "url": "http://{}:9090".format(ip),
    }
    try:
        post(url, data)
        logger.info("Trying to post datasource")

    except Exception:
        logger.info("Create Datasources failed")
        raise


def post(url, data):
    data = jsonutils.dump_as_bytes(data)
    logger.info("In post method for dumping data")
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, data=data, headers=headers)
        result = response.json()
        logger.debug('The result is: %s', result)
        logger.info("Trying to post")
        return result
    except Exception as e:
        logger.info("Failed post" + str(e))
        raise


ip_address = socket.gethostbyname(socket.gethostname())
_create_data_source(ip_address, 3000)
_create_dashboard(ip_address, 3000, '/home/opnfv/bottlenecks/monitor/'+
                  'prototype_prometheus_dashboard.json')
