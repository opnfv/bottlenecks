##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


import sys

THIS = sys.modules[__name__]
__id_max = 100
__style_max = 10
dom = {"chapter", "section", "unit"}
element = {"title", "table", "figure", "paragraph", "plot", "chart", "space"}

nodes = dom | element
for _node in nodes:
    setattr(THIS, _node, _node)


def tuple2text(sn, node, style):
    assert sn in range(__id_max)
    assert style in range(__style_max)
    assert node in nodes
    return "%02d##%s#%d" % (sn, node, style)


def dict2text(info):
    assert "sn" in info and info["sn"] in range(__id_max)
    assert "style" in info and info["style"] in range(__style_max)
    assert "node" in info and info["node"] in nodes
    return "%02d##%s#%d" % (info["sn"], info["node"], info["style"])


def text2dict(candy):
    tmp = candy.replace("##","#").split("#")
    result = {
        "sn": int(tmp[0]),
        "node": tmp[1],
        "style": int(tmp[2])
    }
    assert result["sn"] in range(__id_max)
    assert result["style"] in range(__style_max)
    assert result["node"] in nodes
    return result


def text2tuple(candy):
    tmp = candy.replace("##","#").split("#")

    sn = int(tmp[0])
    node = tmp[1]
    style = int(tmp[2])

    assert sn in range(__id_max)
    assert style in range(__style_max)
    assert node in nodes
    return sn, node, style
