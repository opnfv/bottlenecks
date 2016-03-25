##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

_DEFAULTS = "vstf check key defaults".encode()


def check(key, choices=[], defaults=_DEFAULTS):
    def _deco(func):
        def __deco(*args, **kwargs):
            if key not in kwargs:
                if defaults != _DEFAULTS:
                    kwargs[key] = defaults
                else:
                    raise Exception("Error: '%s' is needed in %s" % (key, func))

            if choices and kwargs[key] not in choices:
                raise Exception("Error: %s :%s" % (key, kwargs[key]))
            ret = func(*args, **kwargs)
            return ret

        return __deco

    return _deco


def dcheck(key, choices=[]):
    def _deco(func):
        def __deco(*args):
            if len(args) == 2:
                values = args[1]
            elif len(args) == 1:
                values = args[0]
            else:
                values = None
            if isinstance(values, dict):
                if key not in values:
                    raise Exception("Error: '%s' is needed in %s" % (key, func))
                if choices and values[key] not in choices:
                    raise Exception("Error: %s :%s" % (key, values[key]))
            ret = func(*args)
            return ret

        return __deco

    return _deco


def vstf_input(key, types=str, choices=[], default=None):
    def _deco(func):
        def __deco(*args):
            ret = func(*args)
            if not isinstance(ret, dict):
                ret = {}
            in_str = "----> %s : " % key
            if choices:
                in_str = "---- %s\n" % (str(choices)) + in_str
            while True:
                if types == list or types == dict:
                    value = input(in_str)
                else:
                    value = raw_input(in_str)
                    value = types(value)
                if not value:
                    value = default
                if not choices or value in choices:
                    break
            ret.update({key: value})
            return ret

        return __deco

    return _deco


def namespace():
    def _deco(func):
        def __deco(*args, **kwargs):
            ret = func(*args, **kwargs)
            nspace = kwargs.get("namespace", None)
            if nspace:
                ret = "ip netns exec %(namespace)s " % {"namespace": nspace} + ret
            return ret

        return __deco

    return _deco
