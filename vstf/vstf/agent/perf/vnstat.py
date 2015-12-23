"""
Created on 2015-8-6

@author: y00228926
"""
import subprocess
import time
import re
from signal import SIGINT
import os
import logging
from vstf.common.utils import check_call, my_popen, kill_by_name

LOG = logging.getLogger(__name__)


class VnStat(object):
    def __init__(self):
        self.netns_exec_str = "ip netns exec %s "
        self.vnstat_cmd_str = "vnstat -l -i %s"
        self.child_process = {}

    def run_vnstat(self, device, namespace=None):
        cmd = self.vnstat_cmd_str
        if namespace:
            cmd1 = (self.netns_exec_str + "ifconfig %s") % (namespace, device)
            check_call(cmd1, shell=True)
            cmd = self.netns_exec_str + cmd
            cmd = cmd % (namespace, device)
        else:
            cmd = cmd % device
        check_call("which vnstat", shell=True)
        child = my_popen(cmd.split(), stdout=subprocess.PIPE)
        self.child_process[child.pid] = child
        return child.pid

    def kill_vnstat(self, pid, namespace=None):
        assert pid in self.child_process
        os.kill(pid, SIGINT)
        process = self.child_process.pop(pid)
        out = process.stdout.read()
        process.wait()
        LOG.info("os.kill(pid = %s)", pid)
        data = {'tool': 'vnstat', 'type': 'nic', 'raw_data': out}
        return data

    def clean(self):
        for _, process in self.child_process.items():
            process.kill()
            process.wait()
            LOG.info("process.kill(vnstat:%s)", process.pid)
        self.child_process = {}
        return True

    def process(self, raw):
        buf = raw.splitlines()
        buf = buf[9:]
        buf = ' '.join(buf)
        m = {}

        digits = re.compile(r"\d+\.?\d*")
        units = re.compile("(?:gib|mib|kib|kbit/s|gbits/s|mbit/s|p/s)", re.IGNORECASE | re.MULTILINE)
        units_arr = units.findall(buf)

        LOG.debug(units_arr)

        digits_arr = digits.findall(buf)

        for i in range(len(digits_arr)):
            digits_arr[i] = round(float(digits_arr[i]), 2)

        m['rxpck'], m['txpck'] = digits_arr[8], digits_arr[9]
        m['time'] = digits_arr[-1]
        digits_arr = digits_arr[:8] + digits_arr[10:-1]
        index = 0
        for unit in units_arr:
            unit = unit.lower()
            if unit == 'gib':
                digits_arr[index] *= 1024
            elif unit == 'kib':
                digits_arr[index] /= 1024
            elif unit == 'gbit/s':
                digits_arr[index] *= 1000
            elif unit == 'kbit/s':
                digits_arr[index] /= 1000
            else:
                pass
            index += 1

        for i in range(len(digits_arr)):
            digits_arr[i] = round(digits_arr[i], 2)

        m['rxmB'], m['txmB'] = digits_arr[0:2]
        m['rxmB_max/s'], m['txmB_max/s'] = digits_arr[2:4]
        m['rxmB/s'], m['txmB/s'] = digits_arr[4:6]
        m['rxmB_min/s'], m['txmB_min/s'] = digits_arr[6:8]
        m['rxpck_max/s'], m['txpck_max/s'] = digits_arr[8:10]
        m['rxpck/s'], m['txpck/s'] = digits_arr[10:12]
        m['rxpck_min/s'], m['txpck_min/s'] = digits_arr[12:14]
        return m

    def force_clean(self):
        LOG.info("%s %s start", self.__class__, self.force_clean.__name__)
        kill_by_name("vnstat")
        self.child_process = {}
        return True
