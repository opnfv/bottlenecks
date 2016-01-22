##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import json
import logging
from vstf.common.utils import randomMAC

LOG = logging.getLogger(__name__)


class IntentParser(object):
    def __init__(self, cfg_file):
        self.cfg_file = cfg_file
        with file(cfg_file) as fp:
            self.cfg_intent = json.load(fp)

    def parse_cfg_file(self):
        self.set_default()
        self.parse_br_type()
        self.parse_vms_cfg()
        return self.cfg_intent

    def set_default(self):
        for host_cfg in self.cfg_intent['env-build']:
            host_cfg.setdefault("scheme", 'libvirt')
            host_cfg.setdefault("drivers", [])
            host_cfg.setdefault("vms", [])
            host_cfg.setdefault("bridges", [])
            for vm_cfg in host_cfg["vms"]:
                vm_cfg.setdefault("init_config", {})
                vm_cfg["init_config"].setdefault('amqp_port', 5672)
                vm_cfg["init_config"].setdefault('amqp_user', "guest")
                vm_cfg["init_config"].setdefault('amqp_passwd', "guest")
                vm_cfg["init_config"].setdefault('amqp_id', "")

    def _nomornize_boolean(self, flag):
        if isinstance(flag, bool):
            return flag
        lflag = flag.lower()
        if lflag == 'true':
            return True
        if lflag == 'false':
            return False
        raise Exception("flag %s cannot be nomonized to bool value" % flag)

    def parse_br_type(self):
        for host_cfg in self.cfg_intent['env-build']:
            br_cfgs = host_cfg['bridges']
            br_type_set = set()
            for br_cfg in br_cfgs:
                br_type_set.add(br_cfg["type"])
            for vm_cfg in host_cfg['vms']:
                for tap_cfg in vm_cfg['taps']:
                    br_type_set.add(tap_cfg["br_type"])
            if len(br_type_set) > 1:
                raise Exception("specified more than one type of vswitchfor host:%s" % host_cfg['ip'])
            if len(br_type_set) > 0:
                br_type = br_type_set.pop()
                host_cfg['br_type'] = br_type

    def parse_vms_cfg(self):
        for host_cfg in self.cfg_intent['env-build']:
            vm_cfgs = host_cfg["vms"]
            self._parse_vm_init_cfg(vm_cfgs)
            self._parse_vm_ctrl_cfg(vm_cfgs)
            for vm_cfg in vm_cfgs:
                self._parse_taps_cfg(vm_cfg['taps'])

    def _parse_taps_cfg(self, tap_cfgs):
        tap_name_set = set()
        tap_mac_set = set()
        count = 0
        for tap_cfg in tap_cfgs:
            count += 1
            tap_name_set.add(tap_cfg["tap_mac"])
            tap_mac_set.add(tap_cfg["tap_name"])
        if len(tap_mac_set) != len(tap_name_set) != count:
            raise Exception('config same tap_mac/tap_name for different taps')
        LOG.info("tap_name_set: %s", tap_name_set)
        LOG.info("tap_mac_set: %s", tap_mac_set)

    def _parse_vm_init_cfg(self, vm_cfgs):
        count = 0
        ip_set = set()
        gw_set = set()
        required_options = {"ctrl_ip_setting", "ctrl_gw", "amqp_server"}
        for vm_cfg in vm_cfgs:
            init_cfg = vm_cfg["init_config"]
            sub = required_options - set(init_cfg.keys())
            if sub:
                raise Exception("unset required options:%s" % sub)
            count += 1
            ip_set.add(init_cfg["ctrl_ip_setting"])
            gw_set.add(init_cfg["ctrl_gw"])
        if len(gw_set) > 1:
            raise Exception("cannot config more than one gw for vm")
        if len(ip_set) < count:
            raise Exception("config same ip for different vm")
        LOG.info("ip_set: %s", ip_set)
        LOG.info("gw_set: %s", gw_set)

    def _parse_vm_ctrl_cfg(self, vm_cfgs):
        count = 0
        ctrl_mac_set = set()
        ctrl_br_set = set()
        for vm_cfg in vm_cfgs:
            count += 1
            vm_cfg.setdefault("ctrl_mac", randomMAC())
            vm_cfg.setdefault("ctrl_br", 'br0')
            ctrl_mac_set.add(vm_cfg['ctrl_mac'])
            ctrl_br_set.add(vm_cfg['ctrl_br'])
        if len(ctrl_br_set) > 1:
            raise Exception("cannot config more than one ctrl_br_set.")
        if len(ctrl_mac_set) < count:
            raise Exception("config same ctrl_mac_set for different vm.")
        LOG.info("ctrl_mac_set: %s", ctrl_mac_set)
        LOG.info("ctrl_br_set: %s", ctrl_br_set)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='config file to parse')
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    p = IntentParser(args.config)
    LOG.info(json.dumps(p.parse_cfg_file(), indent=4))
