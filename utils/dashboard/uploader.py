##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import os
import json
import requests
import yaml

CONF = "dashboard.yaml"

class Uploader(object):

    def __init__(self):
        self.headers = {'Content-type': 'application/json'}
        self.timeout = 5
        self.result = {
            "project_name": "bottlenecks",
            "description": "bottlenecks test cases result"}

        with open(CONF) as stream:
            dashboard_conf = yaml.load(stream)
        self.result['pod_name'] = dashboard_conf['pod_name']
        self.result['installer'] = dashboard_conf['installer']
        self.result['version'] = dashboard_conf['version']
        self.target = dashboard_conf['target']


    def upload_result(self, raw_data):
        if self.target == '':
            print('No target was set, so no data will be posted.')
            return
        self.result["details"] = raw_data["details"]
        self.result["case_name"] = raw_data["case_name"]

        try:
            print('Test result:\n %s' % json.dumps(self.result))
            res = requests.post(self.target,
                                data=json.dumps(self.result),
                                headers=self.headers,
                                timeout=self.timeout)
            print('Test result posting finished with status code %d.' % res.status_code)
        except Exception as err:
            print ('Failed to record result data: %s', err)


# for local test
def _test():

    data = '{"details": [{"client": 200, "throughput": 20}, {"client": 300, "throughput": 20}], "case_name": "rubbos"}'
    Uploader().upload_result(json.loads(data))


if __name__ == "__main__":
    _test()
