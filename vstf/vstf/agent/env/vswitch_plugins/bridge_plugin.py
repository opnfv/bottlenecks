##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from vstf.agent.env.vswitch_plugins import model
from vstf.common.utils import check_call, get_eth_by_bdf, check_output


class BridgePlugin(model.VswitchPlugin):
    def __init__(self):
        pass

    def clean(self):
        """clean brs created before.

        """
        out = check_output(r"brctl show | grep -v '^\s' | awk '{print $1}'|sed '1,1d'", shell=True)
        print out
        for br in out.split():
            if br != 'br0':
                self._del_br(br)

        return True

    def init(self):
        pass

    def _del_br(self, name):
        check_call('ip link set dev %s down' % name, shell=True)
        check_call('brctl delbr %s' % name, shell=True)

    def create_br(self, br_cfg):
        """Create a bridge(virtual switch). Return True for success, return False for failure.

        :param dict    br_cfg: configuration for bridge creation like
                {
                    "name": "br1",
                    "uplinks": [
                        {
                            "bdf": "04:00.0",
                        },
                        {
                            "bdf": "04:00.1",
                        }
                    ]
                }

        """
        name, uplinks = br_cfg['name'], br_cfg['uplinks']
        check_call("brctl addbr %s" % name, shell=True)
        for uplink in uplinks:
            device = get_eth_by_bdf(uplink['bdf'])
            check_call("ip link set dev %s up" % device, shell=True)
            check_call("brctl addif %s %s" % (name, device), shell=True)
        check_call("ip link set dev %s up" % name, shell=True)
        return True

    def set_tap_vid(self, tap_cfg):
        """linux bridge doesn't support vlan id setting.
        """
        return True

    def set_fastlink(self, br_cfg):
        """linux bridge doesn't support openflow protocol.
        """
        return True
