##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from heatclient import client as heat_client
from keystoneclient.v2_0 import client as keystone_client
from heatclient.common import template_utils

import heat.common as common


class HeatManager:

    def __init__(self, credentials):
        self.user = credentials['user']
        self.password = credentials['password']
        self.controller_ip = credentials['controller_ip']
        self.heat_url = credentials['heat_url']
        self.auth_uri = credentials['auth_uri']
        self.project_id = credentials['project']
        self.heat = None

    def heat_init(self):
        keystone = keystone_client.Client(username=self.user,
                                          password=self.password,
                                          tenant_name=self.project_id,
                                          auth_url=self.auth_uri)
        auth_token = keystone.auth_token
        self.heat_url = keystone.service_catalog.url_for(
            service_type='orchestration')
        self.heat = heat_client.Client('1', endpoint=self.heat_url,
                                       token=auth_token)

    def stacks_list(self, name=None):
        for stack in self.heat.stacks.list():
            if (name and stack.stack_name == name) or not name:
                common.LOG.info("stack name " + stack.stack_name)
                common.LOG.info("stack status " + stack.stack_status)

    def stack_generate(self, template_file, stack_name, parameters):
        self.heat_init()
        self.stacks_list()
        tpl_files, template = template_utils.get_template_contents(
            template_file)

        fields = {
            'template': template,
            'files': dict(list(tpl_files.items()))
        }
        self.heat.stacks.create(stack_name=stack_name, files=fields['files'],
                                template=template, parameters=parameters)
        self.stacks_list(stack_name)

    def stack_is_deployed(self, stack_name):
        self.heat_init()
        if stack_name in self.heat.stacks.list():
            return True
        return False

    def stack_check_status(self, stack_name):
        for stack in self.heat.stacks.list():
            if stack.stack_name == stack_name:
                return stack.stack_status
        return 'NOT_FOUND'

    def heat_validate_template(self, heat_template_file):
        self.heat_init()
        if not self.heat.stacks.validate(template=open(heat_template_file,
                                                       'r').read()):
            raise ValueError('The provided heat template "' +
                             heat_template_file +
                             '" is in the wrong format')

    def stack_delete(self, stack_name):
        self.heat_init()
        try:
            for stack in self.heat.stacks.list():
                if stack.stack_name == stack_name:
                    self.heat.stacks.delete(stack.id)
                    return True
        except:
            pass
        return False
