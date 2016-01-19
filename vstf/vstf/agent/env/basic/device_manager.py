##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import re
import logging
from vstf.agent.perf import netns
from vstf.common.utils import check_output, get_device_name, my_sleep, check_call, call, IPCommandHelper

LOG = logging.getLogger(__name__)

default_drivers = {
    '82599': 'ixgbe',
    '82576': 'igb',
}


class LspciHelper(object):
    def __init__(self):
        self.bdf_desc_map = {}
        self.bdf_device_map = {}
        self.device_bdf_map = {}
        self.bdf_ip_map = {}
        self.bdf_driver_map = {}
        self.mac_bdf_map = {}
        self.bdf_mac_map = {}
        self._get_bdfs()
        self._get_devices()
        self._get_drivers()
        self._get_ip_macs()

    def _get_bdfs(self):
        self.bdf_desc_map = {}
        out = check_output('lspci |grep Eth', shell=True)
        for line in out.splitlines():
            bdf, desc = line.split(' ', 1)
            self.bdf_desc_map[bdf] = desc

    def _get_devices(self):
        for bdf, desc in self.bdf_desc_map.items():
            device = get_device_name(bdf)
            if device is None:
                LOG.info("cann't find device name for bdf:%s, no driver is available.", bdf)
                try:
                    self._load_driver(desc)
                except:
                    LOG.warn("!!!unable to load_driver for device:%s", bdf)
                my_sleep(0.2)
                device = get_device_name(bdf)
            self.bdf_device_map[bdf] = device
            if device:
                self.device_bdf_map[device] = bdf
                check_call("ip link set dev %s up" % device, shell=True)

    def _get_drivers(self):
        for device, bdf in self.device_bdf_map.items():
            buf = check_output('ethtool -i %s | head -n1' % device, shell=True)
            driver = buf.split()[1]
            self.bdf_driver_map[bdf] = driver

    def _get_ip_macs(self):
        for device, bdf in self.device_bdf_map.items():
            buf = check_output("ip addr show dev %s" % device, shell=True)
            macs = re.compile("[A-F0-9]{2}(?::[A-F0-9]{2}){5}", re.IGNORECASE | re.MULTILINE)
            for mac in macs.findall(buf):
                if mac.lower() in ('00:00:00:00:00:00', 'ff:ff:ff:ff:ff:ff'):
                    continue
                else:
                    break
            ips = re.compile(r"inet (\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}/\d{1,2})", re.MULTILINE)
            ip = ips.findall(buf)
            if ip:
                self.bdf_ip_map[bdf] = ip[0]
            else:
                self.bdf_ip_map[bdf] = None
            self.bdf_mac_map[bdf] = mac
            self.mac_bdf_map[mac] = bdf

    def _load_driver(self, desc):
        for key in default_drivers:
            if key in desc:
                driver = default_drivers[key]
                LOG.info("try to load default driver [%s]", driver)
                check_call('modprobe %s' % driver, shell=True)
                break
        else:
            LOG.warn("unsupported nic type:%s", desc)


class DeviceManager(object):
    def __init__(self):
        super(DeviceManager, self).__init__()
        mgr = netns.NetnsManager()
        mgr.clean_all_namespace()
        self.lspci_helper = LspciHelper()

    def _get_device_detail(self, bdf):
        device = self.lspci_helper.bdf_device_map[bdf]
        mac = self.lspci_helper.bdf_mac_map[bdf]
        ip = self.lspci_helper.bdf_ip_map[bdf]
        desc = self.lspci_helper.bdf_desc_map[bdf]
        driver = self.lspci_helper.bdf_driver_map[bdf]
        detail = {
            'bdf': bdf,
            'device': device,
            'mac': mac,
            'ip': ip,
            'desc': desc,
            'driver': driver
        }
        return detail

    def get_device_detail(self, identity):
        """
        Gets the detail of a network card.

        :param identity: be it the mac address, bdf, device name of a network card.
        :return: device detail of a network card.
        """
        if identity in self.lspci_helper.bdf_device_map:
            bdf = identity
        elif identity in self.lspci_helper.device_bdf_map:
            bdf = self.lspci_helper.device_bdf_map[identity]
        elif identity in self.lspci_helper.mac_bdf_map:
            bdf = self.lspci_helper.mac_bdf_map[identity]
        else:
            raise Exception("cann't find the device by identity:%s" % identity)
        return self._get_device_detail(bdf)

    def get_device_verbose(self, identity):
        return IPCommandHelper().get_device_verbose(identity)

    def list_nic_devices(self):
        """
        Get all the details of network devices in the host.
        :return: a list of network card detail.
        """
        device_list = []
        for bdf in self.lspci_helper.bdf_device_map.keys():
            detail = self._get_device_detail(bdf)
            device_list.append(detail)
        return device_list
