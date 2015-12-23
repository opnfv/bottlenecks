"""
Created on 2015-9-15

@author: y00228926
"""
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
