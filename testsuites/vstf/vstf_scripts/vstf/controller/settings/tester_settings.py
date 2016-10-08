##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


import logging

import vstf.controller.settings.settings as sets

LOG = logging.getLogger(__name__)


class TesterSettings(sets.Settings):

    def __init__(self, path="/etc/vstf/env/",
                 filename="tester.json",
                 mode=sets.SETS_SINGLE):
        super(TesterSettings, self).__init__(path, filename, mode)
