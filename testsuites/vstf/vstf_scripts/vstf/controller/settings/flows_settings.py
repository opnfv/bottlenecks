##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import logging

import vstf.controller.settings.settings as sets

LOG = logging.getLogger(__name__)


class FlowsSettings(sets.Settings):

    def __init__(self, path="/etc/vstf/perf/",
                 filename="sw_perf.flownodes-settings",
                 mode=sets.SETS_SINGLE):
        self._check_actors = {'namespaces', 'senders', 'receivers', 'watchers'}
        self._nocheck_actors = {"cpu_listens"}
        super(FlowsSettings, self).__init__(path, filename, mode)

    def _register_func(self):
        super(FlowsSettings, self)._register_func()
        for actor in self._check_actors:
            actor = actor.encode()
            func_name = "add_%s" % actor
            setattr(
                self,
                func_name,
                self._adding_file(
                    func_name,
                    self._mset,
                    self._fset,
                    actor,
                    self._check_add))
            func_name = "madd_%s" % actor
            setattr(
                self,
                func_name,
                self._adding_memory(
                    func_name,
                    self._mset,
                    actor,
                    self._check_add))

        for actor in self._nocheck_actors:
            actor = actor.encode()
            func_name = "add_%s" % actor
            setattr(
                self,
                func_name,
                self._adding_file(
                    func_name,
                    self._mset,
                    self._fset,
                    actor))
            func_name = "madd_%s" % actor
            setattr(
                self,
                func_name,
                self._adding_memory(
                    func_name,
                    self._mset,
                    actor))

        LOG.debug(self.__dict__.keys())

    def clear_all(self):
        actors = self._check_actors | self._nocheck_actors
        for actor in actors:
            func_name = "set_%s" % actor
            func = getattr(self, func_name)
            func([])

    def mclear_all(self):
        actors = self._check_actors | self._nocheck_actors
        for actor in actors:
            func_name = "mset_%s" % actor
            func = getattr(self, func_name)
            func([])

    def _check_add(self, value):
        flows = ['agent', 'dev']
        if not isinstance(value, dict):
            raise Exception("type is error: %s" % (str(value)))
        for flow in flows:
            if flow not in value.keys():
                raise Exception("keys[%s] is missing: %s" % (flow, str(value)))

        items = ["ip", "namespace", "mac", "iface", "bdf"]
        for item in items:
            if item not in value['dev'].keys():
                raise Exception("keys[%s] is error: %s" % (item, str(value)))


def unit_test():
    from vstf.common.log import setup_logging
    setup_logging(
        level=logging.DEBUG,
        log_file="/var/log/vstf/vstf-flows-settings.log",
        clevel=logging.INFO)

    flows_settings = FlowsSettings()
    LOG.info(flows_settings.settings)

    flows_settings.clear_all()
    flows_settings.set_flows(2)
    LOG.info(flows_settings.settings)

    flow_1 = {
        "agent": "192.168.188.14",
        "dev": {
            "ip": "192.168.1.100",
            "namespace": "vstf-space-1",
            "mac": "90:e2:ba:20:1f:d8",
            "iface": "eth4",
            "bdf": "04:00.0"
        }
    }
    flow_2 = {
        "agent": "192.168.188.14",
        "dev": {
            "ip": "192.168.1.101",
            "namespace": "vstf-space-2",
            "mac": "90:e2:ba:20:1f:d9",
            "iface": "p57p2",
            "bdf": "04:00.1"
        }
    }

    flows_settings.add_senders(flow_1)
    flows_settings.add_senders(flow_2)
    flows_settings.add_receivers(flow_2)
    flows_settings.add_receivers(flow_1)

    flows_settings.add_watchers(flow_1)
    flows_settings.add_watchers(flow_2)

    flows_settings.add_namespaces(flow_1)
    flows_settings.add_namespaces(flow_2)

    cpu = {
        "agent": "192.168.188.16",
        "affctl": {
            "policy": 2
        }
    }
    flows_settings.add_cpu_listens(cpu)
    LOG.info(flows_settings.settings)


if __name__ == '__main__':
    unit_test()
