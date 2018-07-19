import json
import os
from step.test_step import TestStep
class WorkloadStep(TestStep):
	__step_type__ = 'workload'

	def __init__(self, id, name, service, action, args):
		super(WorkloadStep, self).__init__(self.__step_type__, id, name, service, action, args)
		self._argsParse()
		self._action()

	def _argsParse(self):
		if self._callType == "REST":
			currentDirPath = os.path.dirname(os.path.abspath(__file__))
			envDirPath = os.path.abspath(os.path.join(currentDirPath, os.pardir, os.pardir, 'env'))
			envFilePath = os.path.join(envDirPath, "%s.json"%self._service['name'])
			with open(envFilePath) as f:
				propDict = json.load(f)
				self._args['ip'] = propDict['ip']
				self._args['port'] = propDict['port']
				self._args['api'] = "%s/%s" % (propDict['api_map']['workload'], self._args['command'])
				exclude = {'ip', 'port', 'api', 'command', 'method'}
				self._args['req_body'] = {key:value for key,value in self._args.items() if key not in exclude}


	def _start(self):
		print "workload start"

	def _stop(self):
		print "workload stop"