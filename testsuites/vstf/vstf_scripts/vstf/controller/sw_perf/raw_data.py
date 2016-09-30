##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import subprocess
import re
import logging

LOG = logging.getLogger(__name__)


class RawDataProcess(object):

    def __init__(self):
        pass

    def process_vnstat(self, data):
        buf = data.splitlines()
        buf = buf[9:]
        buf = ' '.join(buf)
        m = {}
        digits = re.compile(r"\d{1,}\.?\d*")
        units = re.compile(
            r"(?:gib|mib|kib|kbit/s|gbit/s|mbit/s|p/s)",
            re.IGNORECASE | re.MULTILINE)
        units_arr = units.findall(buf)
        LOG.debug(units_arr)
        digits_arr = digits.findall(buf)

        for i in range(len(digits_arr)):
            digits_arr[i] = round(float(digits_arr[i]), 2)

        LOG.info("-------------digit_arr------------------")
        LOG.info(digits_arr)
        LOG.info(units_arr)
        LOG.info("-----------------------------------------")
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
        LOG.info("---------------vnstat data start-------------")
        LOG.info(m)
        LOG.info("---------------vnstat data end---------------")
        return m

    def process_sar_cpu(self, raw):
        lines = raw.splitlines()
        # print lines
        head = lines[2].split()[3:]
        average = lines[-1].split()[2:]
        data = {}
        for h, d in zip(head, average):
            data[h.strip('%')] = float(d)
        return data

    def process_qperf(self, raw):
        buf = raw.splitlines()
        data = buf[1].strip().split()
        key = data[0]
        value = float(data[2])
        unit = data[3]
        return {key: value, 'unit': unit}

    @classmethod
    def process(cls, raw):
        self = cls()
        tool, data_type, data = raw['tool'], raw['type'], raw['raw_data']
        m = {}
        if tool == 'vnstat' and data_type == 'nic':
            m = self.process_vnstat(data)
        if tool == 'sar' and data_type == 'cpu':
            m = self.process_sar_cpu(data)
            if 'cpu_num' in raw:
                m['cpu_num'] = raw['cpu_num']
            if 'cpu_mhz' in raw:
                m['cpu_mhz'] = raw['cpu_mhz']
        if tool == 'qperf':
            m = self.process_qperf(data)
        return m


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    p = RawDataProcess()
    cmd = "vnstat -i eth0 -l"
    child = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    import time
    import os
    from signal import SIGINT

    time.sleep(20)
    os.kill(child.pid, SIGINT)
    data = child.stdout.read()
    print data
    print p.process_vnstat(data)

    cmd = "sar -u 2"
    child = subprocess.Popen(
        cmd.split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    import time
    import os
    from signal import SIGINT

    time.sleep(20)
    os.kill(child.pid, SIGINT)
    data = child.stdout.read()
    print data
    print p.process_sar_cpu(data)
