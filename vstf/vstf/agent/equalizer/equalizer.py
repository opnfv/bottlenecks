##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import os
import re
import subprocess
import logging

log = logging.getLogger(__name__)


def run_cmd(cmd, shell=True):
    try:
        ret = subprocess.check_output(cmd, shell=shell)
    except subprocess.CalledProcessError as e:
        raise e
    return ret


class Resource(object):
    def __init__(self):
        super(Resource, self).__init__()
        self.sysfs = "/sys/devices/system/node"
        self.mapping = {}
        for node in self._init_numa():
            self.mapping[node] = {}

            process_mapping = self._get_process_mapping(node)
            for process_index in xrange(0, len(bin(process_mapping)) - 2):
                if process_mapping & 1 << process_index != 0:
                    core = self._get_core_id(node, process_index)
                    if not self.mapping[node].has_key(core):
                        self.mapping[node][core] = []
                    self.mapping[node][core].append(process_index)

    def _get_process_mapping(self, numa_node):
        ret = run_cmd("cat " + self.sysfs + '/' + numa_node + '/cpumap').replace(',', '').lstrip('0')
        return int(ret, 16)

    def _get_core_id(self, numa_node, process_index):
        cmd = "cat " + self.sysfs + '/' + numa_node + '/cpu' + str(process_index) + '/topology/core_id'
        return run_cmd(cmd).strip('\n')

    def _init_numa(self):
        """the node name is node0, node1......"""
        try:
            node_list = os.listdir(self.sysfs)
        except Exception as e:
            raise e
        ret = []
        partten = re.compile("^node[0-9]{,}$")
        for node in node_list:
            if partten.match(node) is None:
                continue
            ret.append(node)
        return ret


class Equalizer(Resource):
    def __init__(self):
        super(Equalizer, self).__init__()

    def topology(self):
        print self.mapping


e = Equalizer()
e.topology()
