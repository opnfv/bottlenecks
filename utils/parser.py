#!/usr/bin/env python
#!/usr/bin/env python
##############################################################################
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
'''This file realize the function of how to parser a config file.
This contain Two part:
Frist is Init some variables the will be used.
Second is reading config file.'''

import os
import yaml


class Parser():

    bottlenecks_config = {}
    bottlenecks_test = {}

    @classmethod
    def config_init(cls):
        cls.code_dir = os.path.dirname(os.path.abspath(__file__))
        cls.root_dir = os.path.dirname(cls.code_dir)
        cls.test_dir = os.path.join(cls.root_dir, 'testsuites')
        config_dir = os.path.join(
            cls.root_dir,
            'config',
            'config.yaml')

        with open(config_dir) as file:
            config_info = yaml.load(file)
            common_config = config_info['common_config']
            cls.bottlenecks_config["releng_dir"] = common_config["releng_dir"]
            cls.bottlenecks_config["fetch_os"] = common_config["fetch_os_file"]
            cls.bottlenecks_config["log_dir"] = common_config['log_dir']
            cls.bottlenecks_config["rc_dir"] = common_config['rc_dir']
            cls.config_dir_check(cls.bottlenecks_config["log_dir"])

    @classmethod
    def story_read(cls, testcase, story_name):
        story_dir = os.path.join(
            cls.test_dir,
            testcase,
            'testsuite_story',
            story_name)
        with open(story_dir) as file:
            story_parser = yaml.load(file)
        for case_name in story_parser['testcase']:
            Parser.testcase_read(cls, testcase, case_name)

        return cls.bottlenecks_test

    @classmethod
    def testcase_read(cls, testcase, testcase_name):

        testcase_dir = os.path.join(
            cls.test_dir,
            testcase,
            'testcase_cfg',
            testcase_name)
        testcase_local = testcase_dir + ".yaml"
        with open(testcase_local) as f:
            cls.bottlenecks_test[testcase_name] = yaml.load(f)

        return cls.bottlenecks_test

    @classmethod
    def config_dir_check(cls, dirname):
        if dirname is None:
            dirname = '/tmp/'
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    @staticmethod
    def config_parser(testcase_cfg, parameters):
        test_cfg = testcase_cfg['test_config']
        stack_cfg = testcase_cfg['stack_config']
        # TO-DO add cli parameters to stack_config.
        return test_cfg, stack_cfg


class HeatTemplate_Parser():
    """parser a Heat template and a method to deploy template to a stack"""

    def __init__(self):
        self.heat_date = {}
        self.heat_date["resources"] = {}
        self.heat_date["outputs"] = {}
        self.heat_date["heat_template_version"] = "2013-05-23"
        self.heat_date["description"] = {"Stack built by the bottlenecks"
                                         " framework for root."}

    def add_security_group(self, name):
        """add to the template a Neutron SecurityGroup"""
        security_name = name + "-security_group"
        self.heat_date["resources"][security_name] = {
            "type": "OS::Neutron::SecurityGroup",
            "properties": {
                "name": security_name,
                "description": "Group allowing icmp and upd/tcp on all ports",
                "rules": [
                    {"remote_ip_prefix": "0.0.0.0/0",
                     "protocol": "tcp",
                     "port_range_min": "1",
                     "port_range_max": "65535"},
                    {"remote_ip_prefix": "0.0.0.0/0",
                     "protocol": "udp",
                     "port_range_min": "1",
                     "port_range_max": "65535"},
                    {"remote_ip_prefix": "0.0.0.0/0",
                     "protocol": "icmp"}
                ]
            }
        }

        self.heat_date["outputs"][security_name] = {
            "description": "ID of Security Group",
            "value": {"get_resource": security_name}
        }

    def add_keypair(self, name):
        """add to the template a Nova KeyPair"""
        key_name = name + "key"
        with open(Parser.root_dir +
                  "utils/infra_setup/"
                  "bottlenecks_key/bottlenecks_key.pub") as f:
            key_content = f.read()
            self.heat_date["resources"][key_name] = {
                "type": "OS::Nova::KeyPair",
                "properties": {
                    "name": key_name,
                    "public_key": key_content
                }
            }

    def add_network(self, name):
        """add to the template a Neutron Net"""
        network_name = name + "-net"
        self.heat_date["resources"][network_name] = {
            "type": "OS::Neutron::Net",
            "properties": {"name": network_name}
        }

    def add_subnet(self, name, cidr):
        """add to the template a Neutron Subnet"""
        network_name = name + "-net"
        subnet_name = name + "-subnet"
        self.heat_date["resources"][subnet_name] = {
            "type": "OS::Neutron::Subnet",
            "depends_on": network_name,
            "properties": {
                "name": subnet_name,
                "cidr": cidr,
                "network_id": {"get_resource": network_name}
            }
        }

        self.heat_date["outputs"][subnet_name] = {
            "description": "subnet %s ID" % subnet_name,
            "value": {"get_resource": subnet_name}
        }

    def add_router(self, name, ext_gw_net):
        """add to the template a Neutron Router and interface"""
        router_name = name + "-route"
        subnet_name = name + "-subnet"

        self.heat_date["resources"][router_name] = {
            "type": "OS::Neutron::Router",
            "depends_on": [subnet_name],
            "properties": {
                "name": router_name,
                "external_gateway_info": {
                    "network": ext_gw_net
                }
            }
        }

    def add_router_interface(self, name):
        """add to the template a Neutron RouterInterface and interface"""
        router_name = name + "-route"
        subnet_name = name + "-subnet"
        router_if_name = name + "-interface"

        self.heat_date["resources"][router_if_name] = {
            "type": "OS::Neutron::RouterInterface",
            "depends_on": [router_name, subnet_name],
            "properties": {
                "router_id": {"get_resource": router_name},
                "subnet_id": {"get_resource": subnet_name}
            }
        }

    def add_server(self, name, image, flavor, user, ports=None):
        """add to the template a Nova Server"""

        key_name = "bottlenecks-poscakey"
        port_name = name + "-port"
        self.heat_date["resources"][name] = {
            "type": "OS::Nova::Server",
            "properties": {
                "name": name,
                "flavor": flavor,
                "image": image,
                "key_name": {"get_resource": key_name},
                "admin_user": user,
                "networks": [{
                    "port": {"get_resource": port_name}
                }]
            }
        }

        self.heat_date["outputs"][name] = {
            "description": "VM UUID",
            "value": {"get_resource": name}
        }

    def add_port(self, name, stack_name=None):
        """add to the template a named Neutron Port"""
        network_name = stack_name + "-net"
        subnet_name = stack_name + "-subnet"
        port_name = name + "-port"
        security_name = stack_name + "-security_group"

        self.heat_date["resources"][port_name] = {
            "type": "OS::Neutron::Port",
            "depends_on": [subnet_name],
            "properties": {
                "name": port_name,
                "fixed_ips": [{"subnet": {"get_resource": subnet_name}}],
                "network_id": {"get_resource": network_name},
                "replacement_policy": "AUTO",
                "security_groups": [{"get_resource": security_name}]
            }
        }

        self.heat_date["outputs"][port_name] = {
            "description": "Address for interface %s" % port_name,
            "value": {"get_attr": [port_name, "fixed_ips", 0, "ip_address"]}
        }

    def add_floating_ip(self, name, stack_name, network_ext):
        """add to the template a Nova FloatingIP resource
        see: https://bugs.launchpad.net/heat/+bug/1299259
        """
        port_name = name + "-port"
        floating_ip_name = name + "-floating"
        router_if_name = stack_name + "-interface"

        self.heat_date["resources"][floating_ip_name] = {
            "depends_on": [router_if_name, port_name],
            "type": "OS::Nova::FloatingIP",
            "properties": {
                "pool": network_ext,
            }
        }
        self.heat_date['outputs'][floating_ip_name] = {
            'description': 'floating ip %s' % name,
            'value': {'get_attr': [name, 'ip']}
        }

    def add_floating_ip_ass(self, name):
        """add to the template a Nova FloatingIP resource
        see: https://bugs.launchpad.net/heat/+bug/1299259
        """
        port_name = name + "-port"
        floating_ip_name = name + "-floating"
        floating_ass = name + "-floating_ass"

        self.heat_date["resources"][floating_ass] = {
            "type": 'OS::Neutron::FloatingIPAssociation',
            "depends_on": [port_name, floating_ip_name],
            "properties": {
                "floatingip_id": {'get_resource': floating_ip_name},
                "port_id": {"get_resource": port_name}
            }
        }

    def get_template_date(self):
        return self.heat_date
