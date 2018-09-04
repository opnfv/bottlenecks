##############################################################################
# Copyright (c) 2018 Huawei Technologies Co.,Ltd. and others
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import random
import collections
import re
from src.conductor_processor.task import TaskFile


class WorkflowFile(object):
    def __init__(self, name):
        self._name = "workflow_" + name + "(%s)" % getRandString(10)
        self._description = ''
        self._version = 1
        self._schemaVersion = 2
        self._tasks = []
        self._outputParameters = {}

    def getDict(self):
        d = collections.OrderedDict()
        d['name'] = self._name
        d['description'] = self._description
        d['version'] = self._version
        d['schemaVersion'] = self._schemaVersion
        d['tasks'] = self._tasks
        d['outputParameters'] = self._outputParameters

        return d

    def generateMetaData(self, flowList, stepObjArr):
        flowParser = FlowParser(flowList, stepObjArr)
        self._tasks, taskMetaList = flowParser.parseMainFlow()
        normalTasks = flowParser.getNormalTaskList()
        for normalTask in normalTasks:
            taskName = normalTask['name']
            referenceName = normalTask['taskReferenceName']
            self._outputParameters["%s(%s)" % (taskName, referenceName)] = \
                "${%s.output.response.body}" % referenceName
        return self.getDict(), taskMetaList


class FlowParser(object):
    def __init__(self, flowList, stepObjArr):
        self._mainFlow = {}
        self._subFlowDict = {}
        self._stepObjArr = stepObjArr
        self._normalTasks = []
        for flow in flowList:
            if flow['name'] == "main":
                self._mainFlow = flow
            else:
                self._subFlowDict[flow['name']] = flow

    def parseMainFlow(self):
        return self.parseOrderList(self._mainFlow['orders'], self._stepObjArr)

    def parse(self, obj, stepObjArr):
        if isinstance(obj, str):
            return self.parseFlow(obj, stepObjArr)
        else:
            return self.parseOrderList(obj, stepObjArr)

    def parseFlow(self, flowName, stepObjArr):
        orderList = self._subFlowDict[flowName]['orders']
        return self.parseOrderList(orderList, stepObjArr)

    def parseOrderList(self, orderList, stepObjArr):
        tasks = []
        taskMetaAllList = []
        for order in orderList:
            if order['type'] == "normal":
                genTask = NormalTask(order, stepObjArr, self)
                self._normalTasks.append(genTask)
            elif order['type'] == "switch":
                genTask = SwitchTask(order, stepObjArr, self)
            elif order['type'] == "parallel":
                genTask = ParallelTask(order, stepObjArr, self)
            tasks.append(genTask.getDict())

            if order['type'] == "parallel":
                joinTask = genTask.getJoinTask()
                tasks.append(joinTask.getDict())

            taskMetaList = genTask.getTaskMetaList()
            if taskMetaList is not None:
                taskMetaAllList.extend(taskMetaList)
        return tasks, taskMetaAllList

    def getNormalTaskList(self):
        normalTasksDict = []
        for normalTask in self._normalTasks:
            normalTasksDict.append(normalTask.getDict())
        return normalTasksDict

    def getNormalTask(self, stepId):
        for normalTask in self._normalTasks:
            if normalTask.getStepId() == stepId:
                return normalTask
        return None


class BaseWorkflowTask(object):
    def __init__(self, name):
        self._name = name
        self._taskReferenceName = self._name + "_task_%s" % getRandString(10)
        self._type = ''
        self._args = {}

    def __str__(self):
        dictObj = self.getDict()
        return str(dictObj)

    def getDict(self):
        d1 = {
            "name": self._name,
            "taskReferenceName": self._taskReferenceName,
            "type": self._type
        }
        return dict(d1, **self._args)

    def getName(self):
        return self._name

    def getReferenceName(self):
        return self._taskReferenceName

    def getTaskMetaList(self):
        taskFile = TaskFile()
        return [taskFile.generateFromStep(self)]


class NormalTask(BaseWorkflowTask):
    def __init__(self, order, stepObjArr, flowParser):
        relatedStepObj = stepObjArr[order['step'] - 1]
        super(NormalTask, self).__init__(relatedStepObj.getName())
        self._taskReferenceName = "task_%s" % getRandString(10)
        self._stepId = relatedStepObj.getId()
        self._type = "HTTP"
        self._args['inputParameters'] = relatedStepObj.getArgs()
        self._paramTransform(self._args['inputParameters'], flowParser)
        print "NormalTask:----------------------\n", relatedStepObj.getArgs()

    def _paramTransform(self, argsDict, flowParser):
        for (k, v) in argsDict.items():
            if isinstance(v, str):
                if re.match("^\(\(\d+\..*\)\)", v):
                    v = v[2:-2]
                    stepId, outputParam = v.split(".")
                    stepId = int(stepId)
                    normalTask = flowParser.getNormalTask(stepId)
                    if normalTask is None:
                        continue
                    argsDict[k] = "${%s.output.response.body.%s}" %  \
                        (normalTask.getReferenceName(), outputParam)
            elif isinstance(v, dict):
                self._paramTransform(v, flowParser)

    def getStepId(self):
        return self._stepId


class SwitchTask(BaseWorkflowTask):
    seqNumber = 0

    def __init__(self, order, stepObjArr, flowParser):
        super(SwitchTask, self).__init__("switch_" + str(SwitchTask.seqNumber))
        SwitchTask.seqNumber = SwitchTask.seqNumber + 1
        if 'name' in order:
            self._name = order['name']
        self._type = "DECISION"
        caseValueParam = 'value'
        order['value'] = order['value'][2:-2]
        stepId, outputParam = order['value'].split(".")
        stepId = int(stepId)
        normalTask = flowParser.getNormalTask(stepId)
        caseValue = "${%s.output.response.body.%s}" % \
            (normalTask.getReferenceName(), outputParam)
        self._args['inputParameters'] = {caseValueParam: caseValue}
        self._args['caseValueParam'] = caseValueParam
        self._args['decisionCases'] = {}
        self._childTaskMetaList = []
        for case, caseOrders in order['cases'].items():
            self._args['decisionCases'][case], taskMetaList =  \
                flowParser.parse(caseOrders, stepObjArr)
            if taskMetaList is not None:
                self._childTaskMetaList.extend(taskMetaList)

    def getTaskMetaList(self):
        selfTaskMetaList = super(SwitchTask, self).getTaskMetaList()
        selfTaskMetaList.extend(self._childTaskMetaList)
        return selfTaskMetaList


class ParallelTask(BaseWorkflowTask):
    seqNumber = 0

    def __init__(self, order, stepObjArr, flowParser):
        InstSeqNumber = ParallelTask.seqNumber
        super(ParallelTask, self).__init__("parallel_" + str(InstSeqNumber))
        ParallelTask.seqNumber = ParallelTask.seqNumber + 1
        if 'name' in order:
            self._name = order['name']
        self._type = "FORK_JOIN"
        self._args['forkTasks'] = []
        self._childTaskMetaList = []
        lastTasksNameList = []
        parallelList = order['parallel'].items()
        parallelList.sort()
        for key, orderList in parallelList:
            print orderList
            taskList, taskMetaList = flowParser.parse(orderList, stepObjArr)
            self._args['forkTasks'].append(taskList)
            lastTasksNameList.append(taskList[-1]['taskReferenceName'])
            if taskMetaList is not None:
                self._childTaskMetaList.extend(taskMetaList)
        self._joinTaskObj = ParallelJoinTask(InstSeqNumber, lastTasksNameList)

    def getTaskMetaList(self):
        selfTaskMetaList = super(ParallelTask, self).getTaskMetaList()
        selfTaskMetaList.extend(self._childTaskMetaList)
        selfTaskMetaList.extend(self._joinTaskObj.getTaskMetaList())
        return selfTaskMetaList

    def getJoinTask(self):
        return self._joinTaskObj


class ParallelJoinTask(BaseWorkflowTask):
    def __init__(self, seqNumber, joinOnList):
        super(ParallelJoinTask, self).__init__(
            "paralleljoin_" + str(seqNumber))
        self._type = "JOIN"
        self._args['joinOn'] = joinOnList


def getRandString(length):
    return "".join(random.choice(str("0123456789")) for i in range(length))
