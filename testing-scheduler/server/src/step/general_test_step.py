from step.test_step import TestStep
import os
import yaml
import re
class GeneralTestStep(TestStep):
	__step_type__ = "test"

	def __init__(self, id, name, service, action, args, context):
		super(GeneralTestStep, self).__init__(self.__step_type__, id, name, service, action, args, context)
		self._stepParse()
		self.action()

	def _contextTransform(self, argsDict):
		for (k, v) in argsDict.items():
			if isinstance(v, str):
				#if len(v) > 4 and v[0:4] == "cxt.":
				if re.match('^\(context\..*\)', v):
					v = v[9:-1]
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
		envFilePath = os.path.join(self._getCurrentDir(), "..", "env", self._serviceName + ".yaml")
		requestParam = {}
		envFilePath = os.path.join(self._getCurrentDir(), "..", "env", self._serviceName + ".yaml")
		with open(envFilePath, 'r') as f:
			conf = yaml.load(f)
			conf = conf[self._serviceName]
		for apiItem in conf["apis"]:
			if apiItem['name'] == self._serviceInterface:
				interfaceConf = apiItem
		if interfaceConf == None:
			return

		# transform the args config
		self._contextTransform(self._args_temp)

		interfaceUri = interfaceConf['uri'] + interfaceConf['template']['uri'][5:]
		interfaceUri = "http://%s:%s/%s"%(conf['ip'], conf['port'], interfaceUri)
		requestParam['uri'] = self._uriTransform(interfaceUri)

		requestParam['method'] = interfaceConf['method']
		if requestParam["method"] == "POST":
			requestParam['body'] = interfaceConf['template']['body']
			self._paramTransform(requestParam['body'], self._args_temp)
		self._args['http_request'] = requestParam

	def _uriTransform(self, uri):
		return re.sub("\(.*?\)", self._uriResReplace, uri)

	def _uriResReplace(self, match):
		matchTrim = match.group()[1:-1]
		return self._args_temp[matchTrim]

	def _paramTransform(self, argsTemplate, argsDict):
		for (k, v) in argsTemplate.items():
			if isinstance(v, str):
				if re.match('^\(.*\)', v):
					argsTemplate[k] = argsDict[k]
			elif isinstance(v, dict):
				self._paramTransform(v, argsDict)

## waiting to restruct...
	def run_testcase(self):
		### fimd_service_conf, set proper command in data to transfer
		if "http_request" in self._args:
			requestParam = self._args['http_request']
			envFilePath = os.path.join(self._getCurrentDir(), "..", "env", self._serviceName + ".yaml")
			with open(envFilePath, 'r') as f:
				conf = yaml.load(f)
				conf = conf[self._serviceName]
				apiPath = conf['apis'][self._action]
				requestParam['uri'] = requestParam['uri'] + apiPath
				tcBaseDir = conf['testcase_base_dir']
				requestBody = requestParam['body']

				requestBody['action'] = "run_test_case"
				requestBody['args']['testcase'] = tcBaseDir + requestBody['args']['testcase']

			if requestParam['method'] == "GET":
				requestParam.pop('body')

	def start(self):
		pass

	## this function is for testing, can be removed latter.
	def start2(self):
		if "http_request" in self._args:
			requestParam = self._args['http_request']
			envFilePath = os.path.join(self._getCurrentDir(), "..", "env", self._serviceName + ".yaml")
			with open(envFilePath, 'r') as f:
				conf = yaml.load(f)
				conf = conf[self._serviceName]
			requestBody = requestParam['body']
			command = requestBody['command']
			requestBody.pop('command')
			apiPath = conf['apis'][command]['realname']
			requestParam['uri'] = requestParam['uri'] + apiPath
			
			if "args" in requestBody:
				requestBody = requestBody['args']
				requestParam['body'] = requestBody
			
			if "format" not in conf['apis'][command]:
				if "args" not in requestBody:
					requestParam.pop("body")
				return

			requestBodyFormat = conf['apis'][command]['format']
			for k,v in requestBodyFormat.items():
				if k in requestBody and isinstance(requestBody[k], eval(v)):
					print "param %s:%s is ok--------------"%(k, requestBody[k])
				else:
					requestBody[k] = "default"

			if requestParam['method'] == "GET":
				requestParam.pop('body')
			## should contain the logic of request_body data
			## should contain the logic of request_body data
			## should contain the logic of request_body data