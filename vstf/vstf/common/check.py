##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

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
