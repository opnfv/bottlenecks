##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
# liangqi1@huawei.com matthew.lijun@huawei.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from oslo_config import cfg

import utils.dispatcher.func as func

func.import_modules_from_package("utils.dispatcher")

CONF = cfg.CONF
opts = [
    cfg.StrOpt('dispatcher',
               default='file',
               help='Dispatcher to store data.'),
]
CONF.register_opts(opts)
