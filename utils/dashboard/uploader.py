##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd. and others
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import sys
import json
import requests
import yaml


class Uploader(object):

    def __init__(self, conf):
        self.headers = {'Content-type': 'application/json'}
        self.timeout = 5
        self.result = {
            "project_name": "bottlenecks",
            "description": "bottlenecks test cases result"}

        with open(conf) as stream:
            dashboard_conf = yaml.load(stream)
        self.result['pod_name'] = dashboard_conf['pod_name']
        self.result['installer'] = dashboard_conf['installer']
        self.result['version'] = dashboard_conf['version']
        self.target = dashboard_conf['target']


    def upload_result(self, case_name, raw_data):
        if self.target == '':
            print('No target was set, so no data will be posted.')
            return
        self.result["case_name"] = case_name
        self.result["details"] = raw_data

        try:
            print('Result to be uploaded:\n %s' % json.dumps(self.result))
            res = requests.post(self.target,
                                data=json.dumps(self.result),
                                headers=self.headers,
                                timeout=self.timeout)
            print('Test result posting finished with status code %d.' % res.status_code)
        except Exception as err:
            print ('Failed to record result data: %s', err)


def _test():

    #data = '{"details": [{"client": 200, "throughput": 20}, {"client": 300, "throughput": 20}], "case_name": "rubbos"}'
    if len(sys.argv) < 2:
        print ("no argumens input!!")
        exit(1)

    with open(sys.argv[1],'r') as stream:
        data = json.load(stream)
        Uploader().upload_result(data)

if __name__ == "__main__":
    _test()

