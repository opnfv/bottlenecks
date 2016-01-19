##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


class ChannelDie(Exception):
    """rabbitmq's channel connect failed"""
    pass


class UnsolvableExit(Exception):
    """the soft maybe error , and the code can not solvable, must be exit"""
    pass


class AgentExit(Exception):
    pass
