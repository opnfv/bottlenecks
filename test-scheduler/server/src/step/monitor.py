##############################################################################
# Copyright (c) 2018 HUAWEI TECHNOLOGIES CO.,LTD and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import json
import os
from src.step.test_step import TestStep


class MonitorStep(TestStep):
    __step_type__ = 'monitor'

    def __init__(self, name, service, action, args):
        super(MonitorStep, self).__init__(name, service, action, args)
        self._argsParse()
        self.action()

    def _argsParse(self):
        if self._call == "REST":
            currentDirPath = os.path.dirname(os.path.abspath(__file__))
            envDirPath = os.path.abspath(os.path.join(
                currentDirPath, os.pardir, os.pardir, 'env'))
            envFilePath = os.path.join(
                envDirPath, "%s.json" % self._service['name'])
            with open(envFilePath) as f:
                propDict = json.load(f)
                self._args['ip'] = propDict['ip']
                self._args['port'] = propDict['port']
                self._args['api'] = "%s/%s" % (
                    propDict['api_map']['workload'], self._args['command'])
                exclude = {'ip', 'port', 'api', 'command', 'method'}
                self._args['req_body'] = {
                    key: value for key, value in
                    self._args.items() if key not in exclude}

    def setUp(self):
        print "monitor setUp"

    def uninstall(self):
        print "monitor uninstall"

    def start(self):
        print "monitor start...."

    def stop(self):
        print "monitor stop"


if __name__ == "__main__":
    service = {"name": "ansible", "call": "REST"}
    monitor = MonitorStep(
        "monitor_cpu", service, "start", **{"target": "abc:qq"})
