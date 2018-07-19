import json
import os
class TaskFile(object):
	def __init__(self, taskName = 'task_0'):
		self._defaultConfFile = self._getFilePath("defaultTaskFile.json")
		with open(self._defaultConfFile) as defaultConf:
			self._jsonObj = json.load(defaultConf)
		self._jsonObj['name'] = taskName

	def generateFromStep(self, stepObject):
		self._jsonObj['name'] = stepObject.getName()
		print "taskFile:", self._jsonObj['name']
		return self._jsonObj

	def _getFilePath(self, fileName):
		dirPath = os.path.dirname(os.path.realpath(__file__))
		return os.path.join(dirPath, fileName)
