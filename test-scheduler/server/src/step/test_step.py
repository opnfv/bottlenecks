##############################################################################
# Copyright (c) 2018 HUAWEI TECHNOLOGIES CO.,LTD and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import os


class TestStep(object):
    def __init__(self, type, id, name, service, action, args, context):
        self._type = type
        self._id = id
        self._name = name
        self._serviceName = service['name']
        self._serviceInterface = service['interface']
        self._action = action
        self._args = args
        self._context = context

    def getId(self):
        return self._id

    def getName(self):
        return self._name

    def getServiceName(self):
        return self._serviceName

    def getCallFunction(self):
        return self._callType

    def getArgs(self):
        return self._args

    def action(self):
        f = getattr(self, self._action)
        f()

    def _argsParse(self):
        pass

    def _getCurrentDir(self):
        return os.path.dirname(__file__)

    def __str__(self):
        return str(self.__dict__)


if __name__ == "__main__":
    args = {'command': 'start'}
    stepObj = TestStep('test_cpu', 'ansible', 'REST', **args)
    print stepObj
