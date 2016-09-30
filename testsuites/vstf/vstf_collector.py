##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd. and others
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import os
import argparse
import json
import requests
import logging

LOG = logging.getLogger(__name__)


class Uploader(object):

    def __init__(self, conf):
        self.headers = {'Content-type': 'application/json'}
        self.timeout = 5
        self.result = {
            "project_name": "bottlenecks",
            "description": "bottlenecks test cases result"}

        with open(conf) as stream:
            dashboard_conf = json.load(stream)
        self.result['pod_name'] = dashboard_conf['pod_name']
        self.result['installer'] = dashboard_conf['installer']
        self.result['version'] = dashboard_conf['version']
        self.target = dashboard_conf['target']

    def upload_result(self, case_name, raw_data):
        if self.target == '':
            LOG.error('No target was set, so no data will be posted.')
            return
        self.result["case_name"] = case_name
        self.result["details"] = raw_data
        try:
            LOG.debug(
                'Result to be uploaded:\n %s' %
                json.dumps(
                    self.result,
                    indent=4))
            res = requests.post(self.target,
                                data=json.dumps(self.result),
                                headers=self.headers,
                                timeout=self.timeout)
            print(
                'Test result posting finished with status code %d.' %
                res.status_code)
        except Exception as err:
            LOG.error('Failed to record result data: %s', err)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config',
        required=True,
        help="basic config file for uploader, json format.")
    parser.add_argument(
        '--dir',
        required=True,
        help="result files for test cases")
    args = parser.parse_args()
    realpath = os.path.realpath(args.dir)
    for filename in os.listdir(args.dir):
        filepath = os.path.join(realpath, filename)
        LOG.debug("uploading test result from file:%s", filepath)
        with open(filepath) as stream:
            result = eval(stream.read())
            Uploader(
                args.config).upload_result(
                filename.lower().replace(
                    '-',
                    ''),
                result)
