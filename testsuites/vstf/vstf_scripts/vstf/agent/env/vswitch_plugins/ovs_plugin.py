##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import os
import shutil
import logging
import time
import re

from vstf.agent.env.vswitch_plugins import model
from vstf.common.utils import check_and_kill, check_and_rmmod, check_call, check_output, \
    get_eth_by_bdf, my_mkdir, call

LOG = logging.getLogger(__name__)


class OvsPlugin(model.VswitchPlugin):

    def __init__(self):
        self.daemons = ['ovs-vswitchd', 'ovsdb-server']
        self.mods = ['openvswitch']
        self.dirs = {'db': "/usr/local/etc/openvswitch"}
        self.cmds = []
        self.cmds.append("mkdir -p /usr/local/etc/openvswitch")
        self.cmds.append(
            "ovsdb-tool create /usr/local/etc/openvswitch/conf.db")
        self.cmds.append("ovsdb-server --remote=punix:/usr/local/var/run/openvswitch/db.sock \
             --remote=db:Open_vSwitch,Open_vSwitch,manager_options \
             --private-key=db:Open_vSwitch,SSL,private_key \
             --certificate=db:Open_vSwitch,SSL,certificate \
             --bootstrap-ca-cert=db:Open_vSwitch,SSL,ca_cert \
             --pidfile --detach")
        self.cmds.append("ovs-vsctl --no-wait init")
        self.cmds.append("ovs-vswitchd --pidfile --detach")
        self.initialized = False

    def init(self):
        if not self.initialized:
            self._start_servers()
            self.initialized = True

    def clean(self):
        """clean for ovs. Rmmod openvswitch.ko, kill openvswitch daemon process.

        """
        for process in self.daemons:
            check_and_kill(process)
        for mod in self.mods:
            check_and_rmmod(mod)
        for _, directory in self.dirs.items():
            if os.path.isdir(directory):
                LOG.info('rm -rf %s', directory)
                shutil.rmtree(directory, ignore_errors=True)
        self.initialized = False
        return True

    def create_br(self, br_cfg):
        """Create a bridge(virtual switch). Return True for success, return False for failure.

        :param dict    br_cfg: configuration for bridge creation like
                {
                    "type": "ovs",
                    "name": "ovs1",
                    "uplinks": [
                        {
                            "bdf": "04:00.0",
                            "vlan_mode": "access",
                            "vlan_id": "1"
                        }
                    ],
                    "vtep": {},
                }

        """
        self.init()
        name, uplinks = br_cfg['name'], br_cfg['uplinks']

        check_call("ovs-vsctl add-br %s" % (name), shell=True)
        if br_cfg['vtep']:  # vxlan supports
            local_ip, remote_ip = br_cfg['vtep'][
                'local_ip'], br_cfg['vtep']['remote_ip']
            assert len(uplinks) == 1
            uplink = uplinks[0]
            device = get_eth_by_bdf(uplink['bdf'])
            time.sleep(0.5)
            vtep = 'vx1'
            check_call("ifconfig %s %s up" % (device, local_ip), shell=True)
            check_call("ovs-vsctl add-port %s %s" % (name, vtep), shell=True)
            check_call(
                "ovs-vsctl set interface %s type=vxlan options:remote_ip=%s" %
                (vtep, remote_ip), shell=True)
        for uplink in uplinks:
            device = get_eth_by_bdf(uplink['bdf'])
            vlan_mode = uplink['vlan_mode']
            vlan_id = uplink['vlan_id']
            check_call("ip link set dev %s up" % device, shell=True)
            call("ethtool -A %s rx off tx off " % device, shell=True)
            check_call("ovs-vsctl add-port %s %s" % (name, device), shell=True)
            if vlan_mode == 'trunk':
                check_call(
                    "ovs-vsctl set port %s trunks=%s" %
                    (device, vlan_id), shell=True)
            elif vlan_mode == 'access':
                check_call(
                    "ovs-vsctl set port %s tag=%s" %
                    (device, vlan_id), shell=True)
            else:
                raise Exception("unreconized vlan_mode:%s" % vlan_mode)
        return True

    def set_tap_vid(self, tap_cfg):
        """set vlan id or vxlan id for tap device(virtual nic for vm).
        return True for success, return False for failure.

        :param dict    tap_cfg: dictionary config for tap device like
                        {
                            "tap_name": "tap_in",
                            "vlan_mode": "access",
                            "vlan_id": "1"
                        }

        """
        port, vlan_mode, vlan = tap_cfg['tap_name'], tap_cfg[
            'vlan_mode'], tap_cfg['vlan_id']
        assert vlan_mode in ('access', 'vxlan')
        if int(vlan) > '4095':
            # vxlan setting
            self.__set_tap_vid(port, "vxlan", vlan)
        else:
            # vlan setting
            self.__set_tap_vid(port, vlan_mode, vlan)
        return True

    def set_fastlink(self, br_cfg):
        """connect two ports directly, so that packets comes from any one port be forwarded to the other.
        return True for success, return False for failure.

        :param dict    br_cfg: dictionary configuration for linking ports.
                {
                    "name": "ovs1",
                    "fastlink": [
                        {
                            "inport": "04:00.0",
                            "outport": "tap_in"
                        }
                    ]
                }
        """
        br_name = br_cfg['name']
        for fast_cfg in br_cfg['fastlink']:
            p1, p2 = fast_cfg['inport'], fast_cfg['outport']
        self.__fastlink(br_name, p1, p2)
        return True

    def _start_servers(self):
        for _, directory in self.dirs.items():
            my_mkdir(directory)
        for mod in self.mods:
            check_call("modprobe %s" % mod, shell=True)
        for cmd in self.cmds:
            check_call(cmd, shell=True)
        return True

    def __set_tap_vid(self, port, vlan_mode, vlan_id):
        if vlan_mode == 'vxlan':
            raise Exception("don't support vxlan setting right now.")
        elif vlan_mode == 'trunk':
            check_call(
                "ovs-vsctl set port %s trunks=%s" %
                (port, vlan_id), shell=True)
        else:
            check_call(
                "ovs-vsctl set port %s tag=%s" %
                (port, vlan_id), shell=True)

    def __fastlink(self, br, p1, p2):
        LOG.info("_fastlink(%s,%s,%s)", br, p1, p2)
        p1 = p1.replace(' ', '')
        p2 = p2.replace(' ', '')
        bdfs = check_output(
            "lspci |grep Eth | awk '{print $1}'",
            shell=True).splitlines()
        if p1 in bdfs:
            p1 = get_eth_by_bdf(p1)
        if p2 in bdfs:
            p2 = get_eth_by_bdf(p2)
        ovs_port = {}
        buf = check_output("ovs-ofctl show %s" % br, shell=True)
        port_info = re.compile(r"[0-9]+\(.*\)", re.IGNORECASE | re.MULTILINE)
        for s in port_info.findall(buf):
            port_num, interface = s.replace('(', ' ').replace(')', ' ').split()
            ovs_port[interface] = port_num
        pn1, pn2 = ovs_port[p1], ovs_port[p2]
        check_call(
            "ovs-ofctl add-flow %s in_port=%s,priority=100,action=output:%s" %
            (br, pn1, pn2), shell=True)
        check_call(
            "ovs-ofctl add-flow %s in_port=%s,priority=100,action=output:%s" %
            (br, pn2, pn1), shell=True)
        return True
