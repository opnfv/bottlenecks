##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


import logging
import time
from vstf.agent.env.basic.image_manager import ImageManager
from vstf.agent.env.basic.source_manager import SourceCodeManager
from vstf.agent.env.basic import commandline
from vstf.agent.env.basic.device_manager import DeviceManager
from vstf.agent.env.basic import collect as coll
from vstf.agent.perf import netns, vnstat, vstfperf, sar, ethtool, affctl
from vstf.agent.env import builder
from vstf.agent.equalizer.get_info import GetPhyInfo
from vstf.agent.equalizer.optimize import Optimize
from vstf.agent.env.driver_plugins.manager import DriverPluginManager

LOG = logging.getLogger(__name__)


class ENV(object):
    def __init__(self):
        super(ENV, self).__init__()
        self.builder = builder.PluginManager()

    def build_env(self, cfg_intent):
        return self.builder.build(cfg_intent)

    def clean_env(self):
        return self.builder.clean()

    @staticmethod
    def create_images(cfg):
        return ImageManager(cfg).create_all()

    @staticmethod
    def clean_images(cfg):
        return ImageManager(cfg).clean_all()


class Drivers(object):
    def __init__(self):
        super(Drivers, self).__init__()
        self.dr_mgr = DriverPluginManager()

    def install_drivers(self, drivers):
        LOG.info("install drivers:%s", drivers)
        self.dr_mgr.clean()
        ret = self.dr_mgr.load(drivers)
        return ret

    def clean_drivers(self):
        return self.dr_mgr.clean()

    def autoneg_on(self, iface, nspace):
        return ethtool.autoneg_on(iface, nspace)

    def autoneg_off(self, iface, nspace):
        return ethtool.autoneg_off(iface, nspace)

    def autoneg_query(self, iface, nspace):
        return ethtool.autoneg_query(iface, nspace)


class Cpu(object):
    def affctl_load(self, policy):
        return affctl.affctl_load(policy)

    def affctl_list(self):
        return affctl.affctl_list()


class Perf(object):
    def __init__(self):
        super(Perf, self).__init__()
        self._vnstat = vnstat.VnStat()
        self._vstfperf = vstfperf.Vstfperf()
        self._sar = sar.Sar()
   
    def run_vnstat(self, device, namespace=None):
        return self._vnstat.run_vnstat(device, namespace)

    def kill_vnstat(self, pid, namespace=None):
        return self._vnstat.kill_vnstat(pid, namespace)

    def perf_run(self, **kwargs):
        return self._vstfperf.run(**kwargs)

    def run_cpuwatch(self, interval = 2):
        return self._sar.start(interval)

    def kill_cpuwatch(self, pid):
        return self._sar.stop(pid)

    def force_clean(self):
        self._vstfperf.force_clean()
        self._sar.force_clean()
        self._vnstat.force_clean()
        return True


class EqualizerOps(GetPhyInfo, Optimize):
    def __init__(self):
        super(EqualizerOps, self).__init__()


class BaseAgent(coll.Collect,
                ENV,
                Cpu,
                Drivers,
                DeviceManager,
                commandline.CommandLine, 
                netns.NetnsManager,
                SourceCodeManager
                ):
    def __init__(self):
        super(BaseAgent, self).__init__()


class softAgent(BaseAgent, Perf, EqualizerOps):
    def __init__(self):
        super(softAgent, self).__init__()


if __name__ == '__main__':
    softAgent()

