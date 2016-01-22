##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from abc import ABCMeta
from abc import abstractmethod


class EnvBuilderPlugin:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.host_cfg = None
        pass

    @abstractmethod
    def clean(self):
        pass

    @abstractmethod
    def load_drivers(self):
        pass

    @abstractmethod
    def create_brs(self):
        pass

    @abstractmethod
    def config_br_ports(self):
        pass

    @abstractmethod
    def create_vms(self):
        pass

    @abstractmethod
    def wait_vms(self):
        pass

    @abstractmethod
    def check_vm_connectivity(self):
        pass

    def build(self, cfg_intent):
        self.host_cfg = cfg_intent
        self.clean()
        self.load_drivers()
        self.create_brs()
        self.create_vms()
        self.wait_vms()
        self.config_br_ports()
        self.check_vm_connectivity()
        return True
