from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import os
import json
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import test_parser
import time
import pyaml
import yaml
import traceback

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TESTSUITE_DIR = os.path.join(BASE_DIR, "..", "..", "test", "test_case")
SERVICE_DIR = os.path.join(BASE_DIR, "..", "env", "service")
CONTEXT_FILE_DIR = os.path.join(BASE_DIR, "..", "env", "context", "context.yaml")
app = Flask(__name__)
CORS(app)

###############
### 1. EXECUTE API
###########################################################################
@app.route("/")
def hello():
  return "Hello, World! This is a greet from parser." + SERVICE_DIR

@app.route("/execute/testcase", methods=['POST'])
def runTestcase():
  suiteName = request.values.get('suiteName')
  caseName = request.values.get('caseName')
  try:
    casePath = os.path.join(TESTSUITE_DIR, suiteName, caseName)
    if os.path.exists(casePath):
      workflowId = test_parser.parse(casePath)
      if workflowId == None or workflowId == '':
        return jsonify({"code": 500, "error": "Server Error."})
      return jsonify({"code": 200, "result": {"workflowId": workflowId}})
    else:
      return jsonify({"code": 300, "error": "no such test case:  %s"%(os.path.join(suiteName, caseName))})
  except BaseException, e:
    app.logger.error(traceback.format_exc())
    return jsonify({"code": 500, "error": "Server error"})


@app.route("/story-content")
def getStoryContent():
  try:
    story_name = request.args['story']
    service_name = request.args['service']
    baseTestDir = os.path.join(BASE_DIR, "..", "..", "test", "test_story")
    storyFileDir = os.path.join(baseTestDir, service_name, story_name)
    storyFileDir = os.path.join(BASE_DIR, "..", "tmp", "generate_workflow.json")
    with open(storyFileDir, "r") as f:
      storyContent = f.read()
  except BaseException, e:
    app.logger.error(traceback.format_exc())
    return jsonify({"code": 500, "error": "Server error"})

  result = {"code": 200, "result": {"service": service_name, "story": story_name, "content": storyContent}}
  return jsonify(result)

###############
### 2. TESTCASE CRUD
###########################################################################
@app.route("/testsuite/list")
def getAllSuite():
  res = []
  id = 1
  try:
    for fileName in os.listdir(TESTSUITE_DIR):
      suiteInfo = {}
      suiteInfo["id"] = id
      suiteInfo["testsuite"] = fileName
      res.append(suiteInfo)
      id = id + 1
  except BaseException, e:
    app.logger.error(traceback.format_exc())
    return jsonify({"code": 500, "error": "Server error"})
 
  return jsonify({"code": 200, "result": res}) 

@app.route("/testsuite/content")
def getSuiteContent():
  res = []
  id = 1
  try:
    suiteName = request.values.get("suiteName")
    exSuitePath = os.path.join(TESTSUITE_DIR, suiteName)
    if os.path.exists(exSuitePath):
      for fileName in os.listdir(exSuitePath):
        tcInfo = {}
        tcInfo["id"] = id
        tcInfo["testcase"] = fileName
        res.append(tcInfo)
        id = id + 1
    else:
      return jsonify({"code": 300, "error": "no such test suite!"})
  except BaseException, e:
    app.logger.error(traceback.format_exc())
    return jsonify({"code": 500, "error": "Server error"})
  
  return jsonify({"code": 200, "result": res})

@app.route("/testcase/content")
def getTCContent():
  res = ""
  editorRes = ""
  try:
    suiteName = request.values.get("suiteName")
    caseName = request.values.get("caseName")
    casePath = os.path.join(suiteName, caseName)
    casePath = os.path.join(TESTSUITE_DIR, casePath)
    if os.path.exists(casePath):
      with open(casePath, "r") as f:
        fileContent = f.read()
      res = fileContent
      editorRes = test_parser.getWebTestcase(yaml.load(res))
    else:
      return jsonify({"code": 300, "error": "no such file!"})
  except BaseException, e:
    app.logger.error(traceback.format_exc())
    return jsonify({"code": 500, "error": "Server error"})
  
  return jsonify({"code": 200, "result": {"content": res, "editorContent": editorRes}})

@app.route("/testsuite/new", methods=['POST'])
def addNewSuite():
  res = []
  id = 1
  try:
    suiteName = request.values.get("suiteName")
    for fileName in os.listdir(TESTSUITE_DIR):
      if fileName == suiteName:
        return jsonify({"code": 300, "error": "testsuite already exists!"})
    testSuitePath = os.path.join(TESTSUITE_DIR, suiteName)
    os.mkdir(testSuitePath)
  except BaseException, e:
    app.logger.error(traceback.format_exc())
    return jsonify({"code": 500, "error": "Server error"})
 
  return jsonify({"code": 200, "result": "ok"})

@app.route("/testsuite/delete", methods=['POST'])
def deleteSuite():
  res = []
  id = 1
  try:
    suiteName = request.values.get("suiteName")
    for fileName in os.listdir(TESTSUITE_DIR):
      if fileName == suiteName:
        testSuitePath = os.path.join(TESTSUITE_DIR, fileName)
        del_file(testSuitePath)
        os.rmdir(testSuitePath)
        return jsonify({"code": 200, "result": "ok"})
  except BaseException, e:
    app.logger.error(traceback.format_exc())
    return jsonify({"code": 500, "error": "Server error"})
 
  return jsonify({"code": 300, "error": "no such testsuite!"})
 
def del_file(path):
  for i in os.listdir(path):
    path_file = os.path.join(path,i)
    if os.path.isfile(path_file):
      os.remove(path_file)
    else:
      del_file(path_file)

@app.route("/testcase/new", methods=['POST'])
def createTestcase():
  res = []
  id = 1
  try:
    suiteName = request.values.get("suiteName")
    caseName = request.values.get("caseName")
    exSuitePath = os.path.join(TESTSUITE_DIR, suiteName)
    if os.path.exists(exSuitePath):
      for fileName in os.listdir(exSuitePath):
        if fileName == caseName:
          return jsonify({"code": 301, "error": "testcase already exists!"})
      casePath = os.path.join(exSuitePath, caseName)
      with open(casePath, "w") as f:
        pass
    else:
      return jsonify({"code": 300, "error": "no such test suite!"})
  except BaseException, e:
    app.logger.error(traceback.format_exc())
    return jsonify({"code": 500, "error": "Server error"})
  
  return jsonify({"code": 200, "result": "ok"})


@app.route("/testcase/delete", methods=['POST'])
def deleteTestcase():
  try:
    suiteName = request.values.get("suiteName")
    caseName = request.values.get("caseName")
    exSuitePath = os.path.join(TESTSUITE_DIR, suiteName)
    if os.path.exists(exSuitePath):
      for fileName in os.listdir(exSuitePath):
        if fileName == caseName:
          casePath = os.path.join(exSuitePath, caseName)
          os.remove(casePath)
          return jsonify({"code": 200, "result": "ok"})
      return jsonify({"code": 301, "error": "no such test case!"})
    else:
      return jsonify({"code": 300, "error": "no such test suite!"})
  except BaseException, e:
    app.logger.error(traceback.format_exc())
    return jsonify({"code": 500, "error": "Server error"})
  

@app.route("/testcase/save", methods=["POST"])
def saveTCContent():
  res = ""
  try:
    suiteName = request.values.get("suiteName")
    caseName = request.values.get("caseName")
    stepList = json.loads(request.values.get("stepList"))
    subflowList = json.loads(request.values.get("subflowList"))
    mainOrdersList = json.loads(request.values.get("mainOrdersList"))
    jsonObj = {"stepList": stepList, "subflowList": subflowList, "mainOrdersList": mainOrdersList}
    parseData = test_parser.parseWebTestcase(jsonObj)

    casePath = os.path.join(suiteName, caseName)
    casePath = os.path.join(TESTSUITE_DIR, casePath)
    if os.path.exists(casePath):
      with open(casePath, "w") as f:
        pyaml.dump(parseData, f, safe=True)
    else:
      return jsonify({"code": 300, "error": "no such file!"})
  except BaseException, e:
    app.logger.error(traceback.format_exc())
    return jsonify({"code": 500, "error": "Server error"})
  
  return jsonify({"code": 200, "result": "save success"})

###############
### 3.1 API FOR SERVICE
############################################################
@app.route("/service/list")
def getAllServices():
  res = []
  try:
    for fileName in os.listdir(SERVICE_DIR):
      serviceName = os.path.splitext(fileName)[0]
      res.append(serviceName)
  except BaseException, e:
    app.logger.error(traceback.format_exc())
    return jsonify({"code": 500, "error": "Server error"})
  return jsonify({"code": 200, "result": res})

@app.route("/service/content")
def getServiceContent():
  res = {}
  try:
    serviceName = request.values.get("serviceName")
    for fileName in os.listdir(SERVICE_DIR):
      if serviceName == os.path.splitext(fileName)[0]:
        res["actions"] = []
        filePath = os.path.join(SERVICE_DIR, fileName)
        with open(filePath, "r") as f:
          content = yaml.load(f)
          apisArr = content[serviceName]['apis']
          for i in range(len(apisArr)):
            apisArr[i].pop("method")
            apisArr[i].pop("baseuri")
          res["actions"] = apisArr
  except BaseException, e:
    app.logger.error(traceback.format_exc())
    return jsonify({"code": 500, "error": "Server error"})
  if res == {}:
    return jsonify({"code": 300, "error": "no such service!"})

  return jsonify({"code": 200, "result": res})

def paramTransform(paramDict):
  res = []
  for (key, value) in paramDict.items():
    paramJson = {}
    paramJson["name"] = key
    paramJson["description"] = value["help"]
    if "params" in value:
      paramJson["params"] = paramTransform(value["params"])
    res.append(paramJson)
  return res

@app.route("/service/action_response")
def actionResponse():
  res = {}
  try:
    serviceName = request.values.get("serviceName")
    actionName = request.values.get("actionName")
    for fileName in os.listdir(SERVICE_DIR):
      if serviceName == os.path.splitext(fileName)[0]:
        res["responseParams"] = []
        filePath = os.path.join(SERVICE_DIR, fileName)
        with open(filePath, "r") as f:
          content = yaml.load(f)
          apisArr = content[serviceName]['apis']
        for i in range(len(apisArr)):
          if actionName == apisArr[i]['name'] and ("response" in apisArr[i]):
            res["responseParams"] = apisArr[i]["response"]
  except BaseException, e:
    app.logger.error(traceback.format_exc())
    return jsonify({"code": 500, "error": "Server error"})
  if res == {}:
    return jsonify({"code": 300, "error": "no such service!"})
  return jsonify({"code": 200, "result": res})

###############
### 3.2 API FOR ENVIRONMENT SERVICE AND CONTEXT
###########################################################################
@app.route('/env/getAllServices')
def getAllService():
  res = []
  id = 1
  try:
    for fileName in os.listdir(SERVICE_DIR):
      item = {}
      item['id'] = id
      item['name'] = os.path.splitext(fileName)[0]
      filePath = os.path.join(SERVICE_DIR, fileName)
      filemt = time.localtime(os.stat(filePath).st_mtime)
      item['time'] = time.strftime("%Y-%m-%d",filemt)
      res.append(item)
      id = id + 1
  except BaseException, e:
    app.logger.error(traceback.format_exc())
    return jsonify({"code": 500, "error": "Server error"})
  return jsonify({"code": 200, "result": res})

@app.route('/env/getService')
def getService():
  try:
    serviceName = request.values.get('serviceName')
    serviceFile = serviceName + '.yaml'
    servicePath = os.path.join(SERVICE_DIR, serviceFile)
    if os.path.exists(servicePath):
      with open(servicePath, "r") as f:
        serviceDict = yaml.load(f)
        serviceDict = serviceDict[serviceName]
      return jsonify({"code": 200, "result": serviceDict})
    else:
      return jsonify({"code": 300, "error": "no such service!"})
  except BaseException, e:
    app.logger.error(traceback.format_exc())
    return jsonify({"code": 500, "error": "Server error"})

@app.route('/env/createService', methods=['POST'])
def createService():
  try:
    name = str(request.values.get('name'))
    ip = str(request.values.get('ip'))
    port = int(request.values.get('port'))
    apis = json.loads(request.values.get('apis'))
    service = {
      name: {
        'ip': ip,
        'port': port,
        'apis': apis
      }
    }
    serviceJson = json.dumps(service, indent=True)
    app.logger.debug(service)

    serviceFile = name + '.yaml'
    servicePath = os.path.join(SERVICE_DIR, serviceFile)
    with open(servicePath, 'w') as f:
      pyaml.dump(service, f, safe=True)
  except BaseException, e:
    app.logger.error(traceback.format_exc())
    return jsonify({"code": 500, "error": "Server error"})
  return jsonify({"code": 200, "result": "create success!"})

@app.route('/env/editService', methods=['POST'])
def editService():
  try:
    oldName = str(request.values.get('oldName'))
    name = str(request.values.get('newName'))
    ip = str(request.values.get('ip'))
    port = int(request.values.get('port'))
    apis = json.loads(request.values.get('apis'))
    app.logger.debug(apis)
    service = {
      name: {
        'ip': ip,
        'port': port,
        'apis': apis
      }
    }
    serviceJson = json.dumps(service, indent=True)
    app.logger.debug(service)

    for fileName in os.listdir(SERVICE_DIR):
      serviceName = os.path.splitext(fileName)[0]
      if serviceName == oldName:
        filePath = os.path.join(SERVICE_DIR, fileName)
        os.remove(filePath)

    serviceFile = name + '.yaml'
    servicePath = os.path.join(SERVICE_DIR, serviceFile)
    with open(servicePath, 'w') as f:
      pyaml.dump(service, f, safe=True)
  except BaseException, e:
    app.logger.error(traceback.format_exc())
    return jsonify({"code": 500, "error": "Server error"})
  return jsonify({"code": 200, "result": "edit success!"})

@app.route('/env/deleteService', methods=['POST'])
def deleteService():
  try:
    name = str(request.values.get('serviceName'))

    for fileName in os.listdir(SERVICE_DIR):
      serviceName = os.path.splitext(fileName)[0]
      if serviceName == name:
        filePath = os.path.join(SERVICE_DIR, fileName)
        os.remove(filePath)
  except BaseException, e:
    app.logger.error(traceback.format_exc())
    return jsonify({"code": 500, "error": "Server error"})
  return jsonify({"code": 200, "result": "delete success!"})

@app.route('/env/getContext')
def getContext():
  try:
    with open(CONTEXT_FILE_DIR, "r") as f:
      fileContent = f.read()
    res = fileContent
  except BaseException, e:
    app.logger.error(traceback.format_exc())
    return jsonify({"code": 500, "error": "Server error"})
  return jsonify({"code": 200, "result": {"context": res}})

@app.route('/env/editContext', methods=['POST'])
def editContext():  
  try:
    context = request.values.get("context")
    test = yaml.load(context)
    with open(CONTEXT_FILE_DIR, "w") as f:
      f.write(context)
  except yaml.constructor.ConstructorError, e:
    app.logger.error(traceback.format_exc())
    return jsonify({"code": 500, "error": "context content error: not a .yaml file!"})
  except BaseException, e:
    app.logger.error(traceback.format_exc())
    return jsonify({"code": 500, "error": "Server error"})

  return jsonify({"code": 200, "result": "edit context success!"})
###########################################################################



if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5310)