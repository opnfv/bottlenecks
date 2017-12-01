from __future__ import print_function
from __future__ import absolute_import

import os
import logging
import json

from conductor.ConductorWorker import ConductorWorker

from yardstick.common import constants as consts
from yardstick.benchmark.core import Param
from yardstick.benchmark.core.task import Task

LOG = logging.getLogger(__name__)

try:
    URL = os.environ['CONDUCTOR']
except KeyError:
    LOG.debug('Conductor url not set. Existing...')
    raise
else:
    LOG.debug('Conductor URL: %s', URL)
    worker = ConductorWorker(URL, 5, 0.1)


class ListenCommands(object):     # pragma: no cover

    def do_start(self, args, **kwargs):
        worker.start('yardstick_run_task', do_task_job, False)
        worker.start('yardstick_get_result', get_result, True)


def run_task(task_id, inputData):
    try:
        case = inputData['testcase']
    except KeyError:
        return {'status': 1, 'result': 'lack of case name'}
    else:
        case = os.path.join(consts.TESTCASE_DIR, '{}.yaml'.format(case))

    args = {'inputfile': [case], 'task_id': task_id}
    args.update(inputData.get('opts', {}))

    param = Param(args)
    result = Task().start(param)

    return result


def do_task_job(data):
    taskType = data.get('taskType')
    taskId = data.get('taskId')
    inputData = data.get('inputData')

    LOG.debug('Type: %s, inputData: %s', taskType, inputData)

    output = run_task(taskId, inputData)

    output_path = os.path.join('/tmp/yardstick', '{}.out'.format(taskId))
    log_path = os.path.join(consts.TASK_LOG_DIR, '{}.log'.format(taskId))

    with open(output_path, 'w') as f:
        f.write(json.dumps(output, indent=4))

    with open(log_path) as f:
        logs = f.readlines()

    result = {
        'status': output['status'],
        'result': {'task_id': output['result']['task_id']}
    }

    return {'status': 'COMPLETED', 'output': result, 'logs': logs}


def get_result(data):
    taskType = data.get('taskType')
    inputData = data.get('inputData')

    LOG.debug('Type: %s, inputData: %s', taskType, inputData)

    job_id = inputData['task_id']
    path = os.path.join('/tmp/yardstick', '{}.out'.format(job_id))
    with open(path) as f:
        output = json.load(f)

    return {'status': 'COMPLETED', 'output': output, 'logs': []}
