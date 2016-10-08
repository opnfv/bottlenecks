##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import commands
import re


# import pdb
# pdb.set_trace()

class Optimize(object):

    def __init__(self):
        pass

    def bind_cpu(self, cpu_range, thread):
        flag, num = commands.getstatusoutput(
            'taskset -pc %s %s' %
            (cpu_range, thread))
        return flag

    def catch_thread_info(self):
        thread_info = {
            'fwd_vhost': None,
            'src_recv_irq': None,
            'dst_send_irq': None}
        # top -H get the usage info
        flag, threads_usages = commands.getstatusoutput(
            'top -bH -n1 -c -w 2000')
        line_array = threads_usages.split('\n')
        # get highest vhost line
        for line in line_array:
            if re.search('vhost-', line) and self._check_thread_usage(line):
                thread_info['fwd_vhost'] = line.split()[0]
                break
        # get highest irq thread as src_recv_irq thread
        for line in line_array:
            if re.search('irq/', line) and self._check_thread_usage(line):
                thread_info['src_recv_irq'] = line.split()[0]
                line_array.remove(line)
                break
        # get the second highest irq thread as dst_send_irq
        for line in line_array:
            if re.search('irq/', line) and self._check_thread_usage(line):
                thread_info['dst_send_irq'] = line.split()[0]
                break
        # check the data valid

        for key in thread_info.keys():
            if thread_info[key] is None:
                return False, str(thread_info)
        return True, str(thread_info)

    def _check_thread_usage(self, line):
        try:
            usage = line.split()[8]
            if float(usage) >= 3.0:
                return True
            else:
                print("[ERROR]The highest thread %s is less than 0.05" % usage)
                return False
        except:
            print("[ERROR]The thread usage get failed.")
