##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from vstf.agent.env.driver_plugins import model
from vstf.common.utils import check_and_rmmod, check_call


class OriginDriverPlugin(model.DriverPlugin):
    """
    implement for operating linux origin driver modules.
    """

    def __init__(self):
        """
        list all origin drivers in self.origin_drivers
        """
        self.origin_drivers = ['ixgbe', 'bnx2x', 'i40e', 'be2net', 'vhost_net']

    def clean(self):
        """clean drivers list in self.origin_drivers.
        
        """
        for mod in self.origin_drivers:
            check_and_rmmod(mod)

        check_and_rmmod('tun')
        return True

    def load(self, drivers):
        """insmod drivers
        
        :param list    drivers:list of drivers link ['ixgbe','vhost_net']
        """
        # load implicit 'tun' module dependency for vhost_net
        if 'vhost_net' in drivers:
            check_call("modprobe tun", shell=True)

        for drv in drivers:
            check_call("modprobe %s" % drv, shell=True)

        return True

    def get_supported_drivers(self):
        return self.origin_drivers
