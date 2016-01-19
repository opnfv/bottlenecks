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


class DriverPlugin:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        """don't pass in any args for __init__.
        """

    @abstractmethod
    def clean(self):
        """implement this clean function to clean environment before and after calling any other functions.
        
        """
        pass

    @abstractmethod
    def load(self, drivers):
        """load driver modules.
        
        :param list    drivers:list of modules to be inserted. for example:[ixgbe,vhost_net]
        
        """
        pass

    @abstractmethod
    def get_supported_drivers(self):
        """return a list of supported driver modules.
        """
        pass
