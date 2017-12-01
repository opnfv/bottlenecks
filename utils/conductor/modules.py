import os
import time
import logging
import random

import etcd
import requests
from conductor import conductor

from utils.logger import Logger

LOG = Logger(__name__).getLogger()
LOG.setLevel(logging.DEBUG)


class GetTestcaseDescription(object):

    def __init__(self, data):
        if not isinstance(data, dict):
            LOG.error('Input should be a dict')
            raise RuntimeError

        self.data = data

        host = os.environ.get('ETCD_HOST', 'localhost')
        port = int(os.environ.get('ETCD_PORT', 2379))
        LOG.debug('Etcd server: http://%s:%s', host, port)

        self.client = etcd.Client(host=host, port=port)

    def run(self):
        services = self._get_services()
        service = self._random_loadblance(services)
        self._get_description(service)

    def _get_services(self):
        service = '/{}'.format(self.data.get('service'))
        LOG.debug('Searching for service: %s ......', service)
        while True:
            try:
                resp = self.client.read(service)
            except etcd.EtcdKeyNotFound:
                time.sleep(5)
            else:
                services = resp._children
                if services:
                    return services
                else:
                    time.sleep(5)

    def _random_loadblance(self, services):
        rand = random.randint(0, len(services) - 1)
        LOG.debug('Find Service: http://%s', services[rand].value)
        return services[rand]

    def _get_description(self, service):
        case = self.data.get('testcase')
        url = 'http://{}/yardstick/testcases/{}/docs'
        url = url.format(service.value, case)
        description = requests.get(url).json()['result']['docs']
        LOG.info('Test case description: \n%s', description)


class Template(object):

    def __init__(self, template, data):
        self.template = template
        self.data = data

        url = os.environ.get('CONDUCTOR', 'http://localhost:8080/api')
        self.meta_client = conductor.MetadataClient(url)
        self.workflow_client = conductor.WorkflowClient(url)

    def run(self):
        self._register_tasks()
        self._create_workflow()

        self._run()

        self._output()

        # self._unregister_tasks()

    def _run(self):
        task_list = [t['taskReferenceName'] for t in self.template['tasks']]

        self.workflow_id = self._start_workflow()
        LOG.debug('Start workflow: %s', self.workflow_id)

        self._print_splitline()
        for task in task_list:
            LOG.debug('%s: Start. Wait......', task)
            self._wait_until_task_complete(task)

    def _wait_until_task_complete(self, task):
        while True:
            workflow = self.workflow_client.getWorkflow(self.workflow_id)
            flag = False
            for t in workflow['tasks']:
                if task == t['referenceTaskName'] and \
                        t['status'] == 'COMPLETED':
                    LOG.info('%s: Task Done', task)
                    self._print_splitline()
                    flag = True
                    break
            if flag:
                break
            else:
                time.sleep(5)

    def _register_tasks(self):
        for task in self.template['tasks']:
            self._register_task(task)

    def _register_task(self, task):
        task = self.meta_client.getTaskDef(task['name'])
        if not task:
            task_def = {
                "name": task['name'],
                "description": task['name'],
                "retryCount": 1,
                "timeoutSeconds": 0,
                "timeoutPolicy": "TIME_OUT_WF",
                "retryLogic": "FIXED",
                "retryDelaySeconds": 60,
                "responseTimeoutSeconds": 3600
            }
            LOG.debug('Register Task: %s', task['name'])
            self.meta_client.registerTaskDefs(task_def)

    def _create_workflow(self):
        workflow = self.meta_client.getWorkflowDef(self.template['name'])
        if not workflow:
            LOG.debug('Create workflow: %s', self.template['name'])
            self.meta_client.createWorkflowDef(self.template)

    def _start_workflow(self):
        return self.workflow_client.startWorkflow(self.template['name'],
                                                  self.data)

    def _unregister_tasks(self):
        for task in self.template['tasks']:
            self._unregister_task(task)

    def _unregister_task(self, task):
        task = self.meta_client.getTaskDef(task['name'])
        if task:
            LOG.debug('Unregister workflow: %s', task['name'])
            self.meta_client.unRegisterTaskDef(task['name'])

    def _output(self):
        workflow = self.workflow_client.getWorkflow(self.workflow_id)
        LOG.info('Output is: \n%s', workflow['output'])

    def _print_splitline(self):
        print('=' * 80)
