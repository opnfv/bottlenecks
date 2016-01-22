##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import os
import platform
import logging
from collections import OrderedDict

from vstf.agent.env.basic.commandline import CommandLine
from vstf.common import constants as const

log = logging.getLogger(__name__)
CMD = CommandLine()


class Collect(object):
    """collect host information such as _cpu, memory and so on"""

    def __init__(self):
        super(Collect, self).__init__()
        self._system = self._system()
        self._cpu = self._cpu()

    def _system(self):
        """the base _system info
        {'os info':{'_system':'ubuntu', 'kernel': '3.13.3'}}"""
        return {const.OS_INFO:
            {
                '_system': open('/etc/issue.net').readline().strip(),
                'kernel': platform.uname()[2]
            }
        }

    def _memery(self):
        """ Return the information in /proc/meminfo
        as a dictionary """
        meminfo = OrderedDict()
        with open('/proc/meminfo') as f:
            for line in f:
                meminfo[line.split(':')[0]] = line.split(':')[1].strip()

        return {const.MEMORY_INFO:
            {
                "Mem Total": meminfo['MemTotal'],
                "Mem Swap": meminfo['SwapTotal']
            }
        }

    def _lscpu(self):
        ret = {}
        with os.popen("lscpu") as f:
            for line in f:
                ret[line.split(':')[0].strip()] = line.split(':')[1].strip()
        return ret

    def _cpu(self):
        ret = []
        with open('/proc/cpuinfo') as f:
            cpuinfo = OrderedDict()
            for line in f:
                if not line.strip():
                    ret.append(cpuinfo)
                    cpuinfo = OrderedDict()
                elif len(line.split(':')) == 2:
                    cpuinfo[line.split(':')[0].strip()] = line.split(':')[1].strip()
                else:
                    log.error("_cpu info unknow format <%(c)s>", {'c': line})
        return {const.CPU_INFO:
            dict(
                {
                    "Model Name": ret[0]['model name'],
                    "Address sizes": ret[0]['address sizes']
                },
                **(self._lscpu())
            )
        }

    def _hw_sysinfo(self):
        cmdline = "dmidecode | grep  -A 2 'System Information' | grep -v 'System Information'"
        ret, output = CMD.execute(cmdline, shell=True)
        if ret:
            result = {}
            # del the stderr
            for tmp in output.strip().split('\n'):
                if tmp is None or tmp is "":
                    continue
                # split the items 
                tmp = tmp.split(":")
                if len(tmp) >= 2:
                    # first item as key, and the other as value
                    result[tmp[0].strip("\t")] = ";".join(tmp[1:])
            return {const.HW_INFO: result}
        else:
            return {const.HW_INFO: "get hw info failed. check the host by cmd: dmidecode"}

    def collect_host_info(self):
        return [self._system, self._cpu, self._memery(), self._hw_sysinfo()]


if __name__ == "__main__":
    c = Collect()
    import json

    print json.dumps(c.collect_host_info(), indent=4)
