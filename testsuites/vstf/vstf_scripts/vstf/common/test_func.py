##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from vstf.common import cliutil as util


@util.arg("--test",
          dest="test",
          default="",
          help="a params of test-xx")
@util.arg("--xx",
          dest="xx",
          default="",
          help="a params of test-xx")
def do_test_xx(args):
    """this is a help doc"""
    print "run test01 " + args.test + args.xx
