##############################################################################
# Copyright (c) 2018 HUAWEI TECHNOLOGIES CO.,LTD and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from src.step.test_step import TestStep
import os
import yaml
import re


class GeneralTestStep(TestStep):
    __step_type__ = "test"

    def __init__(self, id, name, service, action, args, context):
        super(GeneralTestStep, self).__init__(
            self.__step_type__, id, name, service, action, args, context)
        self._stepParse()
        self.action()

    def _contextTransform(self, argsDict):
        for (k, v) in argsDict.items():
            if isinstance(v, str):
                if re.match('^\(\(context\..*\)\)', v):
                    v = v[10:-2]
                    layers = v.split(".")
                    contextData = self._context
                    for layer in layers:
                        contextData = contextData[layer]
                    argsDict[k] = contextData
            elif isinstance(v, dict):
                self._contextTransform(v)

    def _stepParse(self):
        self._args_temp = self._args
        self._args = {}

        # transform the service config
        envFilePath = os.path.join(
            self._getCurrentDir(), "..", "env",
            "service", self._serviceName + ".yaml")
        requestParam = {}
        with open(envFilePath, 'r') as f:
            conf = yaml.load(f)
            conf = conf[self._serviceName]
        for apiItem in conf["apis"]:
            if apiItem['name'] == self._serviceInterface:
                interfaceConf = apiItem
        if interfaceConf is None:
            return

        # transform the args config
        self._contextTransform(self._args_temp)

        interfaceUri = interfaceConf['baseuri'] +  \
            interfaceConf['template']['uri'][11:]
        interfaceUri = "http://%s:%s/%s" % (
            conf['ip'], conf['port'], interfaceUri)
        requestParam['uri'] = self._uriTransform(interfaceUri)

        requestParam['method'] = interfaceConf['method']
        if requestParam["method"] == "POST":
            requestParam['body'] = interfaceConf['template']['body']
            self._paramTransform(requestParam['body'], self._args_temp)
        self._args['http_request'] = requestParam

    def _uriTransform(self, uri):
        return re.sub("\(\(.*?\)\)", self._uriResReplace, uri)

    def _uriResReplace(self, match):
        matchTrim = match.group()[2:-2]
        return self._args_temp[matchTrim]

    def _paramTransform(self, argsTemplate, argsDict):
        for (k, v) in argsTemplate.items():
            if isinstance(v, str):
                if re.match('^\(\(.*\)\)', v):
                    argsTemplate[k] = argsDict[v[2:-2]]
            elif isinstance(v, dict):
                self._paramTransform(v, argsDict)

    def start(self):
        pass
