#!/usr/bin/env python
##############################################################################
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import utils.infra_setup.heat.template as Heat

class stack_api():

    def from_config_template(stack_info):
        stack_name = stack_info['name']
        ext_gw_net = os.environ.get("EXTERNAL_NETWORK")
        heat_parser = HeatTemplate_Parser()
        heat_parser.add_security_group(stack_name)
        heat_parser.add_keypair(stack_name)
        for network in stack_info['networks']:
            heat_parser.add_network(stack_name)
            heat_parser.add_subnet(stack_name,
                                   stack_info['networks'][network]['cidr'])

            heat_parser.add_router(stack_name, ext_gw_net)
            heat_parser.add_router_interface(stack_name)

        for server in stack_info['servers']:
            heat_parser.add_port(server, stack_name)
            heat_parser.add_floating_ip(server, stack_name, ext_gw_net)
            heat_parser.add_floating_ip_ass(server)
            heat_parser.add_server(server,
                                   stack_info['servers'][server]['image'],
                                   stack_info['servers'][server]['flavor'],
                                   stack_info['servers'][server]['user'])

        template = heat_parser.get_template_date()
        stack = Heat.HeatTemplate(name=stack_name, heat_template=template)
        try:
            self.stack = stack.create()
        except KeyboardInterrupt:
            sys.exit("\nStack create interrupted")
        except RuntimeError as err:
            sys.exit("error: failed to deploy stack: '%s'" % err.args)
        except Exception as err:
            sys.exit("error: failed to deploy stack: '%s'" % err)

        for server in stack_info['servers']:
            if len(server.ports) > 0:
                # TODO(hafe) can only handle one internal network for now
                port = list(server.ports.values())[0]
                server.private_ip = self.stack.outputs[port["stack_name"]]

            if server.floating_ip:
                server.public_ip = \
                    self.stack.outputs[server.floating_ip["stack_name"]]

