#!/usr/bin/env python
##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import click

from command_group.testcase import Testcase

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='0.1')
@click.pass_context
def main(ctx):
    """cli for bottlenecks project

       commands:
       bottlenecks testcase run <testcase>
    """
    pass


_testcase = Testcase()


@main.group()
@click.pass_context
def testcase(ctx):
    """testcase cli group for bottlenecks project"""
    pass


@testcase.command('run', help="To execute a test case.")
@click.argument('testname', type=click.STRING, required=True)
@click.option('-n', '--noclean', is_flag=True, default=False,
              help='Openstack resources created by the test'
              'will not be cleaned after the testcase execution.')
def testcase_run(testname, noclean):
    _testcase.run('-c ' + testname, noclean)


@main.group()
@click.pass_context
def teststory(ctx):
    """teststory cli group for bottlenecks project"""
    pass


@teststory.command('run', help="To execute a test story.")
@click.argument('testname', type=click.STRING, required=True)
@click.option('-n', '--noclean', is_flag=True, default=False,
              help='Openstack resources created by the test'
              'will not be cleaned after the teststory execution.')
def teststory_run(testname, noclean):
    _testcase.run('-s ' + testname, noclean)
