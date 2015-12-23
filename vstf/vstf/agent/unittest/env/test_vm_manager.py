"""
Created on 2015-9-24

@author: y00228926
"""
import unittest

from vstf.agent.unittest.env import model
from vstf.agent.env.basic.vm9pfs import VMConfigBy9pfs
from vstf.agent.env.basic.vm_manager import VMControlOperation


class TestVM9pfs(model.Test):
    def setUp(self):
        super(TestVM9pfs, self).setUp()
        self.vm_config = {
            'vm_name': 'vm1',
            'vm_cpu': 5,
            'image_path': "/mnt/sdb/ubuntu_salt_master.img",
            'child_dir': '/mnt/sdb/',
            'image_type': 'qcow2',
            'ctrl_br': 'br0',
            'ctrl_mac': '56:6f:44:a5:3f:a4',
            "taps": [
                {
                    "tap_name": "tap_in",
                    "br_type": "bridge",
                    "br_name": "br0",
                    "tap_mac": "56:6f:44:a5:3f:a2",
                },
                {
                    "tap_name": "tap_out",
                    "br_type": "bridge",
                    "br_name": "br0",
                    "tap_mac": "56:6f:44:a5:3f:a3",
                }
            ],
            'init_config': {
                "amqp_passwd": "guest",
                "amqp_user": "guest",
                "amqp_server": "192.168.188.10",
                "amqp_port": 5672,
                'ctrl_ip_setting': '192.168.188.200/23',
                'tap_pktloop_config': 'dpdk',
                'ctrl_gw': '192.168.188.1'
            }
        }
        self.mgr = VMControlOperation()
        self.mgr.clean_all_vms()

    def tearDown(self):
        self.mgr.clean_all_vms()
        super(TestVM9pfs, self).tearDown()

    def test_create_vm_bridge(self):
        self.mgr.create_vm(self.vm_config)
        self.mgr.wait_vm(self.vm_config["vm_name"])
        self.mgr.init_config_vm(self.vm_config["vm_name"])

    def _replace_opts(self, cfg, br_type):
        for tap_cfg in cfg["taps"]:
            tap_cfg["br_type"] = br_type


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    LOG = logging.getLogger(__name__)
    unittest.main()
