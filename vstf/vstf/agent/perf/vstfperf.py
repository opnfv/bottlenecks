##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

__doc__ = """
operation: [start, stop, restart]
action: [send, receive]
tool: [pktgen, netperf, qperf, iperf, netmap]
params:
    protocol: [tcp_lat, udp_lat, tcp_bw, udp_bw]
    namespace: None
    src:[
       { "iface":"eth0", "ip":"xxx.xxx.xxx.xxx", "mac":"FF:FF:FF:FF:FF:FF"}
    ]
    dst:[
       { "iface":"eth0", "ip":"xxx.xxx.xxx.xxx", "mac":"FF:FF:FF:FF:FF:FF"}
    ]
    size: 64
    threads: 1
    ratep: 100000  (pps)
    time: 100  (s)
"""

import sys
import logging
import vstf.common.constants as cst
import vstf.common.decorator as deco
import vstf.agent.perf.pktgen as vstf_pktgen
import vstf.agent.perf.netmap as vstf_netmap
import vstf.agent.perf.qperf as vstf_qperf
import vstf.agent.perf.iperf as vstf_iperf
import vstf.agent.perf.netperf as vstf_netperf

LOG = logging.getLogger(__name__)


class Vstfperf(object):
    def __init__(self):
        for tool in cst.TOOLS:
            obj_name = 'vstf_' + tool
            obj = getattr(sys.modules[__name__], obj_name)
            cls_name = tool.title()
            cls = getattr(obj, tool.title())
            self.__dict__.update({tool: cls()})

    @deco.check("operation", choices=cst.OPERATIONS)
    @deco.check("action", choices=cst.ACTIONS)
    @deco.check("tool", choices=cst.TOOLS)
    @deco.check("params", defaults={})
    def run(self, **kwargs):
        print "_run in"
        operation = kwargs.pop("operation")
        tool = kwargs.pop("tool")
        instance = getattr(self, tool)
        action = kwargs.pop("action")
        func_name = "%s_%s" % (action, operation)
        func = getattr(instance, func_name)
        LOG.info(kwargs['params'])
        LOG.info(func)
        ret = func(**kwargs['params'])
        return ret

    def force_clean(self):
        LOG.info("%s %s start", self.__class__, self.force_clean.__name__)
        for tool in cst.TOOLS:
            instance = getattr(self, tool)
            instance.force_clean()
        return True


def unit_test():
    from vstf.common.log import setup_logging
    setup_logging(level=logging.DEBUG, log_file="/var/log/vstf/vstf-vstfperf.log", clevel=logging.INFO)

    perf = Vstfperf()
    start = {
        "operation": "start",
        "action": "send",
        "tool": "netperf",
        "params": {
            "namespace": "vnet_name1",
            "protocol": "udp_lat",
            "dst": [
                {"ip": "192.168.1.102"}
            ],
            "size": 64,
            "threads": 1,
            "time": 100,
        },
    }
    perf.run(**start)

    stop = {
        "operation": "stop",
        "action": "send",
        "tool": "netperf",
    }
    perf.run(**stop)


if __name__ == '__main__':
    unit_test()
