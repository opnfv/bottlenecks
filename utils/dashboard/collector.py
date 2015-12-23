##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd. and others
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


import subprocess as subp

def exec_shell(cmd):
    out,err = subp.Popen(cmd, stdout=subp.PIPE, shell=True).communicate()
    return out.strip()


def get_onetime_data(dir_name):
    cmd = "grep -in 'remote client nodes' %s/index.html|awk '{print $5}'|awk -F '<' '{print $1}'" % dir_name
    client_node_num = int(exec_shell(cmd))
    cmd = "grep -n 'Number of clients' %s/index.html|awk '{print $5}'|awk -F '<' '{print $1}'" % dir_name
    each_client_num = int(exec_shell(cmd))
    total_client = (client_node_num+1) * each_client_num
    cmd = 'grep -n "throughput" %s/stat_client*.html |awk -F "<B>" \'FNR%%4==0 {printf "%%s\\n", $3 }\'|awk \'BEGIN{sum=0;}{sum=sum+$1;}END{print sum}\'' % dir_name
    throughput = int(exec_shell(cmd))

    return total_client, throughput


class Collector(object):


    def __init__(self):
        pass


    def collect_data(self, data_home):
        cmd =  'ls -l %s |grep ^d|awk \'{print $9}\'' % data_home
        result = []
        for subdir in exec_shell(cmd).split('\n'):
            total_client, throughput = get_onetime_data(data_home+'/'+subdir)
            result.append({'client':total_client, 'throughput':throughput})
            result.sort(key=lambda x:x['client'])

        return result;

