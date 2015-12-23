#!/usr/bin/python
# -*- coding: utf8 -*-
# author: wly
# date: 2015/11/26
# see license for license details

from vstf.common.utils import check_call, call, check_output


def affctl_load(policy):
    cmd = "affctl load %s" % policy
    return check_call(cmd, shell=True)


def affctl_list():
    cmd = "affctl list"
    return check_output(cmd, shell=True)

