##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

"""Heat template and stack management,
This file could manage stack include the function:
create stack delete stack and so on"""

import time
import sys
import logging

from heatclient import client as heatclient
import common as op_utils


log = logging.getLogger(__name__)


class HeatObject(object):
    ''' base class for template and stack'''
    def __init__(self):
        self._heat_client = None
        self.uuid = None

    def _get_heat_client(self):
        '''returns a heat client instance'''

        if self._heat_client is None:
            sess = op_utils.get_session()
            heat_endpoint = op_utils.get_endpoint(service_type='orchestration')
            self._heat_client = heatclient.Client(
                op_utils.get_heat_api_version(),
                endpoint=heat_endpoint, session=sess)

        return self._heat_client

    def status(self):
        '''returns stack state as a string'''
        heat = self._get_heat_client()
        stack = heat.stacks.get(self.uuid)
        return getattr(stack, 'stack_status')


class HeatStack(HeatObject):
    ''' Represents a Heat stack (deployed template) '''
    stacks = []

    def __init__(self, name):
        super(HeatStack, self).__init__()
        self.uuid = None
        self.name = name
        self.outputs = None
        HeatStack.stacks.append(self)

    @staticmethod
    def stacks_exist():
        '''check if any stack has been deployed'''
        return len(HeatStack.stacks) > 0

    def _delete(self):
        '''deletes a stack from the target cloud using heat'''
        if self.uuid is None:
            return

        log.info("Deleting stack '%s', uuid:%s", self.name, self.uuid)
        heat = self._get_heat_client()
        template = heat.stacks.get(self.uuid)
        start_time = time.time()
        template.delete()
        status = self.status()

        while status != u'DELETE_COMPLETE':
            log.debug("stack state %s", status)
            if status == u'DELETE_FAILED':
                raise RuntimeError(
                    heat.stacks.get(self.uuid).stack_status_reason)

            time.sleep(2)
            status = self.status()

        end_time = time.time()
        log.info("Deleted stack '%s' in %d secs", self.name,
                 end_time - start_time)
        self.uuid = None

    def delete(self, block=True, retries=3):
        '''deletes a stack in the target cloud using heat (with retry)
        Sometimes delete fail with "InternalServerError" and the next attempt
        succeeds. So it is worthwhile to test a couple of times.
        '''
        if self.uuid is None:
            return

        if not block:
            try:
                self._delete()
            except RuntimeError as err:
                log.warn(err.args)
            HeatStack.stacks.remove(self)
            return

        i = 0
        while i < retries:
            try:
                self._delete()
                break
            except RuntimeError as err:
                log.warn(err.args)
                time.sleep(2)
            i += 1

        if self.uuid is not None:
            sys.exit("delete stack failed!!!")
        else:
            HeatStack.stacks.remove(self)

    @staticmethod
    def delete_all():
        for stack in HeatStack.stacks[:]:
            stack.delete()

    def update(self):
        '''update a stack'''
        pass


class HeatTemplate(HeatObject):
    '''Describes a Heat template and a method to deploy template to a stack'''

    def __init__(self,
                 name,
                 template_file=None,
                 heat_parameters=None,
                 heat_template=None):
        super(HeatTemplate, self).__init__()
        self.name = name
        self.state = "NOT_CREATED"
        self.keystone_client = None
        self.heat_client = None
        self.heat_parameters = {}

        # heat_parameters is passed to heat in stack create, empty dict when
        # yardstick creates the template (no get_param in resources part)
        if heat_parameters:
            self.heat_parameters = heat_parameters

        if template_file:
            with open(template_file) as template:
                print "Parsing external template:", template_file
                template_str = template.read()
                self._template = template_str
            self._parameters = heat_parameters
        else:
            if heat_template:
                self._template = heat_template
            else:
                sys.exit("can't init template file!")

        # holds results of requested output after deployment
        self.outputs = {}

        log.debug("template object '%s' created", name)

    def create(self, block=True):
        '''creates a template in the target cloud using heat
        returns a dict with the requested output values from the template'''
        log.info("Creating stack '%s'", self.name)

        # create stack early to support cleanup, e.g. ctrl-c while waiting
        stack = HeatStack(self.name)

        heat = self._get_heat_client()
        end_time = start_time = time.time()
        print(self._template)
        stack.uuid = self.uuid = heat.stacks.create(
            stack_name=self.name, template=self._template,
            parameters=self.heat_parameters)['stack']['id']

        status = self.status()

        if block:
            while status != u'CREATE_COMPLETE':
                log.debug("stack state %s", status)
                if status == u'CREATE_FAILED':
                    raise RuntimeError(getattr(heat.stacks.get(self.uuid),
                                               'stack_status_reason'))

                time.sleep(2)
                status = self.status()

            end_time = time.time()
            outputs = getattr(heat.stacks.get(self.uuid), 'outputs')

        for output in outputs:
            self.outputs[output["output_key"].encode("ascii")] = \
                output["output_value"].encode("ascii")

        log.info("Created stack '%s' in %d secs",
                 self.name, end_time - start_time)

        stack.outputs = self.outputs
        return stack
