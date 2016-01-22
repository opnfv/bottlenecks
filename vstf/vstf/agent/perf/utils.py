##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import logging
import subprocess
from vstf.common.utils import check_call, check_output

LOG = logging.getLogger(__name__)


def get_pid_by_name(process_name):
    out = check_output(['ps', '-A'])
    pids = []
    for line in out.splitlines():
        values = line.split()
        pid, name = values[0], values[3]
        if process_name == name:
            pids.append(int(pid))
    return pids


def get_cpu_num():
    cpu_num = check_output('cat /proc/cpuinfo  | grep processor | wc -l', shell=True).strip()
    cpu_num = int(cpu_num)
    return cpu_num


def get_default_threads():
    cpu_num = get_cpu_num()
    return 2 if cpu_num > 3 * 3 else 1


def modprobe_pktgen():
    check_call('modprobe pktgen', shell=True)
    return True


def iface_up(device):
    check_call("ifconfig %s up" % device, shell=True)
    return True
