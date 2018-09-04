##############################################################################
# Copyright (c) 2018 Huawei Technologies Co.,Ltd. and others
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from conductor import conductor
import json


class WorkflowMgr(object):
    def __init__(self, serverAddr):
        self._serverAddr = serverAddr + '/api'
        self._metaDataClient = conductor.MetadataClient(self._serverAddr)
        self._workflowClient = conductor.WorkflowClient(self._serverAddr)
        self._tasksDefined = False
        self._workflowDefined = False
        self._workflowName = ""

    def setTaskDef(self, taskJson):
        jsonObj = json.loads(taskJson)
        print "define tasks:\n", taskJson
        for (k, v) in jsonObj.items():
            self._metaDataClient.registerTaskDefs(v)
        self._tasksDefined = True

    def setWorkflowDef(self, workflowJson):
        jsonObj = json.loads(workflowJson)
        print "define workflow:\n", workflowJson
        try:
            self._metaDataClient.createWorkflowDef(jsonObj)
        except Exception as e:
            print e
        self._workflowName = jsonObj['name']
        self._workflowDefined = True

    def startWorkflow(self, param={}):
        workflowId = ''
        if not self._tasksDefined:
            print "error: please define the task at first\n"
        elif not self._workflowDefined:
            print "error: please define the workflow at first\n"
        else:
            workflowId = self._workflowClient.startWorkflow(
                self._workflowName, param)
        return workflowId

    def setTaskDefFromFile(self, taskFilePath):
        with open(taskFilePath, 'r') as f:
            self.setTaskDef(f.read())

    def setWorkflowFromFile(self, workflowFilePath):
        with open(workflowFilePath, 'r') as f:
            self.setWorkflowDef(f.read())


# test demo
def main():
    serverAddr = "http://192.168.199.131:8080"
    wfMgr = WorkflowMgr(serverAddr)
    wfMgr.setTaskDefFromFile('mock_tasks.json')
    wfMgr.setWorkflowFromFile('mock_workflow.json')
    inputParam = {'input': 'fake'}
    wfMgr.startWorkflow(inputParam)


if __name__ == "__main__":
    main()
