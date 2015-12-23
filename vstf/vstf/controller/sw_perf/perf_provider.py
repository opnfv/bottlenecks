#!/usr/bin/python
# -*- coding: utf8 -*-
# author: wly
# date: 2015-09-21
# see license for license details

import logging

LOG = logging.getLogger(__name__)


def get_agent_dict(nodes):
    """
    :param:
        nodes: list of flow info
               and ever element must be a dict and kas key "agent"
    :return : list for agent
    :rtype : dict
    """
    agent_list = map(lambda x: x["agent"], nodes)
    return {}.fromkeys(agent_list, False)


class PerfProvider(object):
    def __init__(self, flows_info, tool_info, tester_info):
        self._flows_info = flows_info
        self._tool_info = tool_info
        self._tester_info = tester_info

    def _islation(self):
        flows = self._flows_info["flows"]
        if flows == 2 and self._flows_info["senders"][0]["agent"] == self._flows_info["senders"][1]["agent"]:
            return True
        return False

    def get_senders(self, tool, protocol):
        result = []
        flows = self._flows_info["flows"]
        if self._islation() and "pktgen" == tool:
            sender = {
                "agent": self._flows_info["senders"][0]["agent"],
                "params": {
                    "protocol": protocol,
                    "namespace": None,
                    "src": [],
                    "dst": [],
                    "time": self._tool_info[tool]["time"],
                    "threads": self._tool_info[tool]["threads"]
                }
            }
            for i in range(flows):
                sender['params']['src'].append(self._flows_info["senders"][i]['dev'])
                sender['params']['dst'].append(self._flows_info["receivers"][i]['dev'])
            result.append(sender)
        else:
            for i in range(flows):
                sender = {
                    "agent": self._flows_info["senders"][i]["agent"],
                    "params": {
                        "protocol": protocol,
                        "namespace": None if "netmap" == tool else self._flows_info["senders"][i]['dev']['namespace'],
                        "src": [self._flows_info["senders"][i]['dev']],
                        "dst": [self._flows_info["receivers"][i]['dev']],
                        "time": self._tool_info[tool]["time"],
                        "threads": self._tool_info[tool]["threads"]
                    }
                }
                result.append(sender)
        return result

    def get_receivers(self, tool, protocol):
        result = []
        flows = self._flows_info["flows"]
        if self._islation() and "pktgen" == tool:
            receiver = {
                "agent": self._flows_info["receivers"][0]["agent"],
                "params": {
                    "namespace": None,
                    "protocol": protocol,
                }
            }
            result.append(receiver)
        else:
            for i in range(flows):
                receiver = {
                    "agent": self._flows_info["receivers"][i]["agent"],
                    "params": {
                        "namespace": None if "netmap" == tool else self._flows_info["receivers"][i]['dev']['namespace'],
                        "protocol": protocol,
                        "dst": [self._flows_info["receivers"][i]['dev']]
                    }
                }
                result.append(receiver)
        return result

    def get_watchers(self, tool):
        result = []
        for watcher in self._flows_info["watchers"]:
            node = {
                "agent": watcher["agent"],
                "params": {
                    "iface": watcher['dev']["iface"],
                    "namespace": None if tool in ["pktgen", "netmap"] else watcher['dev']["namespace"],
                }
            }
            result.append(node)
        return result

    def get_namespaces(self, tool):
        result = []

        for watcher in self._flows_info["namespaces"]:
            node = {
                "agent": watcher["agent"],
                "params": {
                    "iface": watcher['dev']["iface"],
                    "namespace": watcher['dev']["namespace"] if tool not in ["pktgen", "netmap"] else None,
                    "ip": watcher['dev']["ip"] + '/24',
                }
            }
            result.append(node)
        return result

    @property
    def get_cpuwatcher(self):
        LOG.info(self._flows_info["cpu_listens"])
        result = {
            "agent": self._flows_info["cpu_listens"][0]["agent"],
            "params": {
            }
        }
        return result

    @property
    def get_cpu_affctl(self):
        LOG.info(self._flows_info["cpu_listens"])
        result = {
            "agent": self._flows_info["cpu_listens"][0]["agent"],
            "params": {
                "policy": self._flows_info["cpu_listens"][0]["affctl"]["policy"]
            }
        }
        return result

    def get_cleaners(self, tool, protocol):
        nodes = self.get_senders(tool, protocol) + \
            self.get_receivers(tool, protocol) + \
            self.get_watchers(tool) + \
            [self.get_cpuwatcher]
        return get_agent_dict(nodes).keys()

    @property
    def get_testers(self):
        agents = get_agent_dict(self._flows_info["namespaces"]).keys()
        result = []
        for agent in agents:
            node = {
                "agent": agent,
                "params": {
                    "drivers": self._tester_info["drivers"]
                }
            }
            result.append(node)
        return result

    def duration(self, tool):
        return self._tool_info[tool]["time"]

    def wait_balance(self, tool):
        return self._tool_info[tool]["wait"]


def unit_test():
    from vstf.common.log import setup_logging
    setup_logging(level=logging.DEBUG, log_file="/var/log/vstf/vstf-perf-provider.log", clevel=logging.INFO)

    from vstf.controller.settings.flows_settings import FlowsSettings
    from vstf.controller.settings.tool_settings import ToolSettings
    from vstf.controller.settings.tester_settings import TesterSettings

    flows_settings = FlowsSettings()
    tool_settings = ToolSettings()
    tester_settings = TesterSettings()

    provider = PerfProvider(flows_settings.settings, tool_settings.settings, tester_settings.settings)

    tools = ['pktgen']
    protocols = ['udp_bw', 'udp_lat']

    for tool in tools:
        LOG.info(tool)
        for protocol in protocols:
            LOG.info(protocol)
            senders = provider.get_senders(tool, protocols)
            LOG.info(len(senders))
            LOG.info(senders)

            receivers = provider.get_receivers(tool, protocols)
            LOG.info(len(receivers))
            LOG.info(receivers)

        LOG.info(provider.get_cpuwatcher)
        LOG.info(provider.get_watchers(tool))
        LOG.info(provider.get_namespaces(tool))
        LOG.info(provider.duration(tool))


if __name__ == '__main__':
    unit_test()
