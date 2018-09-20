#!/usr/bin/env python

##############################################################################
# Copyright (c) 2018 HUAWEI TECHNOLOGIES CO.,LTD and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import click
import os
import yaml
import json
import collections
from src.step.step_manager import TestStepManager
from src.conductor_processor.workflow import WorkflowFile
from conductorclient.run_new_workflow import WorkflowMgr

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONDUCTOR_SERVER_ADDR = "http://conductor_conductor-server_1:8080"
STORE_TASK_PATH = "/tmp/generate_task.json"
STORE_WF_PATH = "/tmp/generate_workflow.json"


@click.command()
@click.option("--filepath", help="file path of test case")
def cmdParse(filepath):
    parse(filepath)


def parse(filepath):
    filePrefix, fileName = os.path.split(filepath)
    print '------------ start to parse the test case:' + \
        '%s ----------------' % fileName
    with open(filepath) as f:
        yaml_file = yaml.load(f)
        parseTestcase(yaml_file['schema'], fileName)

    workflowId = runWorkFlow()
    print '------------------- parse executes end -------------------------'

    return workflowId


def parseTestcase(schema, tcName='testcase0.yaml'):
    try:
        tcName.decode('ascii')
    except Exception, e:
        print e
        tcName = 'testcase0.yaml'
    if schema is None:
        return parseLog(False, reason='schema not found.')
    steps = schema['steps']
    if steps is None:
        return parseLog(False, reason='steps is invalid.')
    flows = schema['flows']
    if flows is None:
        return parseLog(False, reasion='flows is invalid.')
    # steps is a list, step is dict. no json here.
    # steps = sorted(steps, sortById)

    # load context
    contextDict = {}
    contextDir = os.path.join(BASE_DIR, "env", "context", "context.yaml")
    with open(contextDir, "r") as f:
        contextDict = yaml.load(f)
    #
    testStepMgr = TestStepManager(contextDict)

    stepObjArr = []
    for step in steps:
        if 'args' not in step:
            step['args'] = {}
        # type and action can be extended, default couple is 'test' & 'start'.
        if 'type' not in step:
            step['type'] = 'test'
            step['action'] = 'start'

        stepObj = testStepMgr.getStepObj(
            step['type'], step['id'], step['name'], step['service'],
            step['action'], step['args'])
        stepObjArr.append(stepObj)

    # generate workflow by 'flow' and 'step'
    tcName = os.path.splitext(tcName)[0]
    wfFileObj = WorkflowFile(tcName)
    workflowDict, taskMetaList = wfFileObj.generateMetaData(flows, stepObjArr)

    with open(STORE_TASK_PATH, 'w') as f:
        f.write(json.dumps({'task_group': taskMetaList}, indent=True))
    with open(STORE_WF_PATH, 'w') as f:
        f.write(json.dumps(workflowDict, indent=True))


def parseWebTestcase(webTestcase):
    print 'parseWebTestcase----------------------------'

    stepList = webTestcase['stepList']
    mainOrdersList = webTestcase['mainOrdersList']
    subflowList = webTestcase['subflowList']

    parseData = collections.OrderedDict()
    parseData['schema'] = collections.OrderedDict()
    parseData['schema']['steps'] = []
    parseData['schema']['flows'] = []

    parseStepList = parseData['schema']['steps']
    parseFlowList = parseData['schema']['flows']
    stepIndexDict = {}
    # parse stepList
    for index in range(len(stepList)):
        stepItem = stepList[index]
        parseStep = collections.OrderedDict()

        parseStep['id'] = index + 1
        parseStep['name'] = stepItem['name']
        parseStep['service'] = collections.OrderedDict()
        parseStep['service']['name'] = stepItem['service']
        parseStep['service']['interface'] = stepItem['action']
        parseStep['action'] = 'start'
        parseStep['args'] = {}
        for paramItem in stepItem['params']:
            parseStep['args'][paramItem['key']] = transParamString(
                paramItem['value'])

        parseStepList.append(parseStep)
        stepIndexDict[parseStep['name']] = parseStep['id']
    # parse flows
    # parse mainflow
    print stepIndexDict
    typeDict = {1: 'normal', 2: 'switch', 3: 'parallel'}
    mainFlow = collections.OrderedDict()
    mainFlow['name'] = 'main'
    mainFlow['orders'] = []
    mainFlow['orders'] = parseOrderList(
        mainOrdersList, stepIndexDict, typeDict)
    parseFlowList.append(mainFlow)

    # parse subflow
    for subflowItem in subflowList:
        replaceSubflow = collections.OrderedDict()
        replaceSubflow['name'] = subflowItem['name']
        replaceSubflow['orders'] = parseOrderList(
            subflowItem['orderList'], stepIndexDict, typeDict)
        parseFlowList.append(replaceSubflow)

    print 'END parseWebTestcase----------------------------'
    return parseData


# parse orderlist from web edition to server edition
def parseOrderList(orderList, stepIndexDict, typeDict):
    replaceList = []
    for orderItem in orderList:
        replaceOrder = collections.OrderedDict()
        orderType = typeDict[orderItem['type']]
        replaceOrder['type'] = orderType
        if orderType == 'normal':
            stepId = stepIndexDict[orderItem['step']]
            replaceOrder['step'] = stepId
        elif orderType == 'switch':
            replaceOrder['value'] = orderItem['value']
            replaceOrder['cases'] = collections.OrderedDict()
            for caseItem in orderItem['cases']:
                caseValue = caseItem['value']
                caseOrderType = caseItem['orderType']
                caseOrderValue = caseItem['orderValue']
                if caseOrderType == "step":
                    orderInCase = collections.OrderedDict()
                    orderInCase['type'] = 'normal'
                    orderInCase['step'] = stepIndexDict[caseOrderValue]
                    replaceOrder['cases'][caseValue] = [orderInCase]
                else:
                    replaceOrder['cases'][caseValue] = caseOrderValue
        else:
            replaceOrder['parallel'] = collections.OrderedDict()
            pIndex = 1
            for branchItem in orderItem['branches']:
                pKey = 'p' + str(pIndex)
                branchOrderType = branchItem['orderType']
                branchOrderValue = branchItem['orderValue']
                if branchOrderType == "step":
                    replaceBranchItem = collections.OrderedDict()
                    replaceBranchItem['type'] = 'normal'
                    replaceBranchItem['step'] = stepIndexDict[branchOrderValue]
                    replaceOrder['parallel'][pKey] = [replaceBranchItem]
                else:
                    replaceOrder['parallel'][pKey] = branchOrderValue
                pIndex += 1
        replaceList.append(replaceOrder)
    return replaceList


def transParamString(val):
    if type(val) != str:
        return val
    if '.' not in val:
        if val.isdigit():
            return int(val)
    try:
        f = float(val)
        return f
    except ValueError:
        return val


def getWebTestcase(originTcDict):
    print "getWebTestcase----------------------------------"
    webTcDict = {
        "stepList": [],
        "mainOrdersList": [],
        "subflowList": []
    }
    stepList = webTcDict['stepList']
    subflowList = webTcDict['subflowList']
    if originTcDict is None:
        return webTcDict
    originContent = originTcDict['schema']
    originSteps = originContent['steps']
    stepIndexDict = {}
    # transform steps to stepList
    for stepItem in originSteps:
        replaceStep = {}
        replaceStep['name'] = stepItem['name']
        replaceStep['service'] = stepItem['service']['name']
        replaceStep['action'] = stepItem['service']['interface']
        replaceStep['params'] = []
        if 'args' in stepItem:
            for (key, value) in stepItem['args'].items():
                replaceParam = {}
                replaceParam['key'] = key
                replaceParam['value'] = value
                replaceStep['params'].append(replaceParam)
        stepList.append(replaceStep)
        stepIndexDict[stepItem['id']] = stepItem['name']

    # transform main flow
    originFlows = originContent['flows']
    originMainflow = {}
    for flowIndex in range(len(originFlows)):
        flowItem = originFlows[flowIndex]
        if flowItem['name'] == 'main':
            originMainflow = flowItem
            originFlows.pop(flowIndex)
            break
    typeDict = {'normal': 1, 'switch': 2, 'parallel': 3}
    webTcDict['mainOrdersList'] = getOrderList(
        originMainflow['orders'], stepIndexDict, typeDict)

    # transform subflows
    for originSubflow in originFlows:
        replaceSubflow = {}
        replaceSubflow['name'] = originSubflow['name']
        replaceSubflow['orderList'] = getOrderList(
            originSubflow['orders'], stepIndexDict, typeDict)
        subflowList.append(replaceSubflow)

    # return web edition of testcase
    print "END getWebTestcase----------------------------------"
    return webTcDict


def getOrderList(originOrderList, stepIndexDict, typeDict):
    replaceOrderList = []
    for orderItem in originOrderList:
        replaceOrderItem = {}
        orderType = orderItem['type']
        replaceOrderItem['type'] = typeDict[orderType]
        if orderType == 'normal':
            stepName = stepIndexDict[orderItem['step']]
            replaceOrderItem['step'] = stepName
        elif orderType == 'switch':
            replaceOrderItem['value'] = orderItem['value']
            replaceOrderItem['cases'] = []
            for (caseValue, ordersInCase) in orderItem['cases'].items():
                replaceCase = {}
                replaceCase['value'] = caseValue
                if type(ordersInCase) == list:
                    replaceCase['orderType'] = 'step'
                    caseStepName = stepIndexDict[ordersInCase[0]['step']]
                    replaceCase['orderValue'] = caseStepName
                else:
                    replaceCase['orderType'] = 'flow'
                    replaceCase['orderValue'] = ordersInCase
                replaceOrderItem['cases'].append(replaceCase)
        else:
            replaceOrderItem['branches'] = []
            for paraIndex in orderItem['parallel']:
                paraItem = orderItem['parallel'][paraIndex]
                replaceBranch = {}
                if type(paraItem) == list:
                    replaceBranch['orderType'] = 'step'
                    branchStepName = stepIndexDict[paraItem[0]['step']]
                    replaceBranch['orderValue'] = branchStepName
                else:
                    replaceBranch['orderType'] = 'flow'
                    replaceBranch['orderValue'] = paraItem
                replaceOrderItem['branches'].append(replaceBranch)
        replaceOrderList.append(replaceOrderItem)

    return replaceOrderList


def runWorkFlow():
    wfMgr = WorkflowMgr(CONDUCTOR_SERVER_ADDR)
    wfMgr.setTaskDefFromFile(STORE_TASK_PATH)
    wfMgr.setWorkflowFromFile(STORE_WF_PATH)
    inputParam = {'input': 'fake'}
    workflowId = wfMgr.startWorkflow(inputParam)
    return workflowId


def parseLog(flag, **msg):
    return {'result': flag, 'message': msg}


if __name__ == "__main__":
    cmdParse()
