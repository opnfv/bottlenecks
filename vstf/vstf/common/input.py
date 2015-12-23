#!/usr/bin/python
# -*- coding: utf8 -*-
# date: 2015-09-09
# see license for license details

__author__ = 'wly'
__version__ = '0.1'

import os


def raw_choice(title):
    ret = {'Y': True, 'N': False}
    while True:
        os.system("clear")
        in_str = "\n%s:(y|n)  " % title
        uin = raw_input(in_str).title()
        if uin in ['Y', 'N']:
            break
    return ret[uin]
