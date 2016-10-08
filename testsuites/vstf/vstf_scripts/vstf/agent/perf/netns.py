##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import logging
from vstf.common.utils import IPCommandHelper
from vstf.agent.perf import ethtool
from vstf.common.utils import check_call, check_output, ns_cmd, my_popen, my_sleep

LOG = logging.getLogger(__name__)


class Netns(object):

    def __init__(self):
        super(Netns, self).__init__()
        self.netns_add_str = "ip netns add %s"
        self.netns_del_str = " ip netns del %s"
        self.netns_add_device_str = " ip link set %s netns %s"
        self.set_link_up_str = "ip link set dev %s up"
        self.set_link_addr_str = "ip addr replace %s dev %s"
        self.netns_remove_device_str = "ip netns exec %s ip link set %s netns  1"
        # self.set_link_addr_str = "ifconfig %s %s up"
        self.ns_devices = {}

    def clean_all_namespace(self):
        out = check_output("ip netns list", shell=True)
        for ns in out.splitlines():
            self.remove_namespace(ns)
        return True

    def create_namespace(self, name):
        if name in (None, 'None', 'none'):
            return True
        cmd = self.netns_add_str % name
        check_call(cmd, shell=True)
        return True

    def remove_namespace(self, ns):
        if ns in (None, 'None', 'none'):
            return True
        ip_helper = IPCommandHelper(ns)
        for dev in ip_helper.device_mac_map:
            cmd = self.netns_remove_device_str % (ns, dev)
            check_call(cmd, shell=True)
            self.activate_device(None, dev)
        cmd = self.netns_del_str % ns
        check_call(cmd, shell=True)
        return True

    def add_device(self, ns, device):
        if ns is None:
            return True
        cmd = self.netns_add_device_str % (device, ns)
        check_call(cmd, shell=True)
        return True

    def config_ip(self, ns, device, ip):
        self.activate_device(ns, device)
        cmd = self.set_link_addr_str % (ip, device)
        cmd = ns_cmd(ns, cmd)
        check_call(cmd, shell=True)
        return True

    def activate_device(self, ns, device):
        cmd = self.set_link_up_str % device
        cmd = ns_cmd(ns, cmd)
        check_call(cmd, shell=True)
        return True


class NetnsManager(object):

    def __init__(self):
        super(NetnsManager, self).__init__()
        self._netns = Netns()

    def config_dev(self, netdev):
        ns, device, ip = netdev["namespace"], netdev["iface"], netdev[
            'ip_setting'] if "ip_setting" in netdev else netdev['ip']
        self._netns.create_namespace(ns)
        self._netns.add_device(ns, device)
        self._netns.config_ip(ns, device, ip)
        my_sleep(1)
        ethtool.autoneg_off(device, ns)
        return True

    def recover_dev(self, netdev):
        ns = netdev["namespace"]
        return self._netns.remove_namespace(ns)

    def clean_all_namespace(self):
        return self._netns.clean_all_namespace()

    @staticmethod
    def ping(ns, ip):
        cmd = "ping -w2 -c1 %s" % ip
        cmd = ns_cmd(ns, cmd)
        child = my_popen(cmd, shell=True)
        return 0 == child.wait()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
