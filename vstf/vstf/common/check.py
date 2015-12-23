#!/usr/bin/python
# -*- coding: utf8 -*-
# author: wly
# date: 2015-11-5
# see license for license details

import logging
import vstf.common.constants as cst

LOG = logging.getLogger(__name__)


def check_case_params(protocol, typ, tool):
    if "throughput" == typ:
        return False, "Not support 'throughput' at this version"
    if "tcp" == protocol:
        if tool in ["pktgen", "netmap"]:
            return False, "%s cant support tcp test" % tool
    if "qperf" == tool and "latency" != typ:
        return False, "qperf support latency test only, cant support %s" % typ
    if "latency" == typ and tool not in ["netperf", "qperf"]:
        return False, "%s cant support latency test" % tool
    return True, "support successfully"
