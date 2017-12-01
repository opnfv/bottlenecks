#!/usr/bin/env python
##############################################################################
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import os
import logging
import errno

import yaml

from utils.conductor import modules
from utils.logger import Logger

LOG = Logger(__name__).getLogger()
LOG.setLevel(logging.DEBUG)


class Conductor(object):
    """Conductor command group.

       Set of commnads to service Conductor
    """

    def __init__(self):
        self.base_path = '/home/opnfv/bottlenecks'

    def run(self, path):
        jobs = self._get_jobs(path)

        for job in jobs:
            self._print_splitline()
            try:
                getattr(self, job.get('type'))(job)
            except AttributeError:
                LOG.error('Invalid type: %s', job.get('type'))
                raise
            self._print_splitline()

    def _print_splitline(self):
        print('=' * 80)

    def _get_jobs(self, path):
        if not os.path.exists(path):
            path = os.path.join(self.base_path, path)
        LOG.debug('Case file path: %s', path)

        try:
            with open(path) as f:
                content = f.read()
        except OSError as e:
            if e.errno == errno.ENOENT:
                LOG.error('Case file does not exist')
                raise
            raise
        else:
            LOG.info('Case content: \n%s', content)
            return yaml.safe_load(content).get('jobs')

    def normal(self, job):
        try:
            action = getattr(modules, job.get('name'))
        except AttributeError:
            LOG.error('Class %s not found', job.get('name'))
            raise
        else:
            action(job.get('input')).run()

    def template(self, job):
        action = modules.Template(job['template'], job['input'])
        action.run()
