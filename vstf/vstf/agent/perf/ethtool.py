#!/usr/bin/python
# -*- coding: utf8 -*-
# author: wly
# date: 2015/11/12
# see license for license details

import vstf.common.utils as utils

__all__ = ["autoneg_on", "autoneg_off", "autoneg_query"]

_para_map = {
    "Autonegotiate": ("-A", "-a", "autoneg"),
    "RX": ("-A", "-a", "rx"),
    "TX": ("-A", "-a", "tx"),
}


def autoneg_on(iface, nspace=None):
    return _set(nspace, iface, Autonegotiate="on", RX="on", TX="on")


def autoneg_off(iface, nspace=None):
    return _set(nspace, iface, Autonegotiate="off", RX="off", TX="off")


def autoneg_query(iface, nspace=None):
    return _query(nspace, iface, "-a")


def _set(nspace, iface, **kwargs):
    cmds = {}
    for item, value in kwargs.items():
        opt, _, key = _para_map[item]
        cmds.setdefault(opt, [])
        cmds[opt].append(key)
        cmds[opt].append(value)

    for key, value in cmds.items():
        cmd = _namespace(nspace)
        cmd += ["ethtool", key, iface] + value
        utils.call(cmd)

    return True


def _query(nspace, iface, item):
    cmd = _namespace(nspace)
    cmd += ["ethtool", item, iface]
    return utils.check_output(cmd)


def _namespace(nspace):
    result = ""
    if nspace:
        result = "ip netns exec %(namespace)s " % {"namespace": nspace}
    return result.split()
