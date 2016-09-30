##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import subprocess
import logging
import time
import os
from signal import SIGINT

from vstf.common.utils import check_output, my_popen, kill_by_name
from vstf.agent.env.basic import collect

LOG = logging.getLogger(__name__)


class Sar(object):

    def __init__(self):
        self.sar_cmd_str = "sar -u %(interval)s"
        self.child_process = {}

    def start(self, interval=2):
        cmd = self.sar_cmd_str % {'interval': interval}
        child = my_popen(
            cmd.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        time.sleep(1)
        if child.poll() is not None:
            print child.poll()
            raise Exception("start vnstat error, vnstat is not running")
        self.child_process[child.pid] = child
        return child.pid

    def stop(self, pid):
        assert pid in self.child_process
        os.kill(pid, SIGINT)
        process = self.child_process.pop(pid)
        out = process.stdout.read()
        process.wait()
        data = {'raw_data': out, 'tool': 'sar', 'type': 'cpu'}
        cpu_info = collect.Collect().collect_host_info()[1]
        cpu_num = cpu_info['CPU INFO']['CPU(s)']
        cpu_mhz = cpu_info['CPU INFO']['CPU MHz']
        data.update({'cpu_num': float(cpu_num), 'cpu_mhz': float(cpu_mhz)})
        return data

    def process(self, raw):
        lines = raw.splitlines()
        # print lines
        head = lines[2].split()[3:]
        average = lines[-1].split()[2:]
        data = {}
        for h, d in zip(head, average):
            data[h.strip('%')] = float(d)
        cpu_num = check_output(
            'cat /proc/cpuinfo  | grep processor | wc -l',
            shell=True).strip()
        data.update({'cpu_num': int(cpu_num)})
        return data

    def clean(self):
        for _, process in self.child_process.items():
            process.kill()
            process.wait()
        self.child_process = {}
        return True

    def force_clean(self):
        LOG.info("%s %s start", self.__class__, self.force_clean.__name__)
        kill_by_name("sar")
        self.child_process = {}
        return True

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    q = Sar()
    pid = q.start()
    time.sleep(10)
    raw = q.stop(pid)
    print raw
    print q.process(raw['raw_data'])
