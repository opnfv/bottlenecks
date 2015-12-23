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


class Uploader(object):

    def __init__(self):
        self.headers = {'Content-type': 'application/json'}
        self.timeout = 5
        self.target = "http://127.0.0.1/results"
        self.raw_result = []
        self.result = {
            "project_name": "bottlenecks",
            "description": "bottlenecks test cases result",
            "pod_name": os.environ.get('POD_NAME', 'unknown-pod'),
            "installer": os.environ.get('INSTALLER_TYPE', 'fuel'),
            "version": os.environ.get('BOTTLENECKS_VERSION', 'unknown')
        }

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
