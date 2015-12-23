#!/usr/bin/python
# -*- coding: utf8 -*-
# author: wly
# date: 2015-09-06
# see license for license details

import json
import re
import os
import copy
import logging
import sys

LOG = logging.getLogger(__name__)


def object2dict(obj):
    # convert object to a dict
    dic = {'__class__': obj.__class__.__name__, '__module__': obj.__module__}
    dic.update(obj.__dict__)
    return dic


def dict2object(dic):
    # convert dict to object
    if '__class__' in dic:
        class_name = dic.pop('__class__')
        module_name = dic.pop('__module__')
        module = __import__(module_name)
        class_ = getattr(module, class_name)
        args = dict((key.encode('ascii'), value) for key, value in dic.items())  # get args
        inst = class_(**args)  # create new instance
    else:
        inst = dic
    return inst


def filter_comments(filename, flags="//"):
    result = []
    with open(filename, "r") as ifile:
        lines = ifile.readlines()
        for data in lines:
            data = re.sub("%s.*$" % (flags), '', data)
            data = re.sub("^\s*$", '', data)
            if data:
                result.append(data)
    LOG.debug(result)
    return ''.join(result)


class BaseSettings(object):
    def _load(self, fullname):
        data = filter_comments(fullname)
        LOG.debug(fullname)
        LOG.debug(data)
        jparams = None
        if data:
            jparams = json.loads(data)
        return jparams

    def _sub(self, ldata, rdata):
        if isinstance(ldata, list) and isinstance(rdata, list):
            data = []
            if ldata:
                for litem in ldata:
                    if rdata:
                        for ritem in rdata:
                            if isinstance(litem, dict) or isinstance(litem, list):
                                tmp = self._sub(litem, ritem)
                            else:
                                tmp = ritem
                            if tmp and tmp not in data:
                                data.append(tmp)
                    else:
                        data.append(litem)

            else:
                data = rdata

        elif isinstance(ldata, dict) and isinstance(rdata, dict):
            data = {}
            rdata_bak = copy.deepcopy(rdata)
            for rkey, rvalue in rdata_bak.items():
                if rkey not in ldata:
                    rdata_bak.pop(rkey)
            for lkey, lvalue in ldata.items():
                if lkey in rdata:
                    if isinstance(lvalue, dict) or isinstance(lvalue, list):
                        data[lkey] = self._sub(lvalue, rdata[lkey])
                    else:
                        data[lkey] = rdata[lkey]
                else:
                    if rdata_bak:
                        data[lkey] = lvalue
        else:
            data = rdata

        return data

    def _save(self, data, filename):
        if os.path.exists(filename):
            os.remove(filename)
        with open(filename, 'w') as ofile:
            content = json.dumps(data, sort_keys=True, indent=4, separators=(',', ':'))
            ofile.write(content)


class DefaultSettings(BaseSettings):
    def __init__(self, path):
        self._default = os.path.join(path, 'default')
        self._user = os.path.join(path, 'user')
    
    def load(self, filename):
        dfile = os.path.join(self._default, filename)
        if os.path.exists(dfile):
            ddata = self._load(dfile)
            data = ddata
        else:
            err = "default file is missing : %s" % (dfile)
            LOG.error(err)
            raise Exception(err)
        ufile = os.path.join(self._user, filename)
        if os.path.exists(ufile):
            udata = self._load(ufile)
            if udata:
                data = self._sub(ddata, udata)
        else:
            LOG.info("no user file :%s" % (ufile))
        return data

    def save(self, data, filename):
        ufile = os.path.join(self._user, filename)
        self._save(data, ufile)


class SingleSettings(BaseSettings):
    def __init__(self, path):
        self._path = path

    def load(self, filename):
        pfile = os.path.join(self._path, filename)
        if os.path.exists(pfile):
            ddata = self._load(pfile)
            data = ddata
        else:
            err = "settings file is missing : %s" % (pfile)
            LOG.error(err)
            raise Exception(err)
        return data

    def save(self, data, filename):
        pfile = os.path.join(self._path, filename)
        self._save(data, pfile)

SETS_DEFAULT = "Default"
SETS_SINGLE = "Single"
SETTINGS = [SETS_SINGLE, SETS_DEFAULT]


class Settings(object):
    def __init__(self, path, filename, mode=SETS_SINGLE):
        if mode not in SETTINGS:
            raise Exception("error Settings mode : %s" % (mode))
        cls_name = mode + "Settings"
        thismodule = sys.modules[__name__]
        cls = getattr(thismodule, cls_name)
        self._settings = cls(path)
        self._filename = filename
        self._fset = self._settings.load(filename)
        self._mset = copy.deepcopy(self._fset)
        self._register_func()

    def reset(self):
        self._fset = self._settings.load(self._filename)
        self._mset = copy.deepcopy(self._fset)

    @property
    def settings(self):
        return self._mset

    def _setting_file(self, func_name, mset, fset, key, check=None):
        def infunc(value):
            if hasattr(check, '__call__'):
                check(value)
            if isinstance(fset, dict):
                mset[key] = copy.deepcopy(value)
                fset[key] = copy.deepcopy(value)
            elif isinstance(fset, list):
                del (mset[:])
                del (fset[:])
                mset.extend(copy.deepcopy(value))
                fset.extend(copy.deepcopy(value))
            self._settings.save(self._fset, self._filename)
            infunc.__name__ = func_name
            LOG.debug(self._mset)
            LOG.debug(self._fset)

        return infunc

    def _setting_memory(self, func_name, mset, key, check=None):
        def infunc(value):
            if hasattr(check, '__call__'):
                check(value)
            if isinstance(mset, dict):
                mset[key] = copy.deepcopy(value)
            elif isinstance(mset, list):
                for i in range(len(mset)):
                    mset.pop()
                mset.extend(copy.deepcopy(value))

            infunc.__name__ = func_name
            LOG.debug(self._mset)
            LOG.debug(self._fset)

        return infunc

    def _adding_file(self, func_name, mset, fset, key, check=None):
        def infunc(value):
            if hasattr(check, '__call__'):
                check(value)
            if key:
                mset[key].append(copy.deepcopy(value))
                fset[key].append(copy.deepcopy(value))
            else:
                mset.append(copy.deepcopy(value))
                fset.append(copy.deepcopy(value))

            self._settings.save(self._fset, self._filename)
            infunc.__name__ = func_name
            LOG.debug(self._mset)
            LOG.debug(self._fset)

        return infunc

    def _adding_memory(self, func_name, mset, key, check=None):
        def infunc(value):
            if hasattr(check, '__call__'):
                check(value)
            if key:
                mset[key].append(copy.deepcopy(value))
            else:
                mset.append(copy.deepcopy(value))
            infunc.__name__ = func_name
            LOG.debug(self._mset)
            LOG.debug(self._fset)

        return infunc

    def _register_func(self):
        if isinstance(self._fset, dict):
            items = set(
                self._fset.keys()
            )
            for item in items:
                item = item.encode()
                func_name = "set_%s" % item
                setattr(self, func_name, self._setting_file(func_name, self._mset, self._fset, item))
                func_name = "mset_%s" % item
                setattr(self, func_name, self._setting_memory(func_name, self._mset, item))
        elif isinstance(self._fset, list):
            func_name = "set"
            setattr(self, func_name, self._setting_file(func_name, self._mset, self._fset, None))
            func_name = "mset"
            setattr(self, func_name, self._setting_memory(func_name, self._mset, None))
            func_name = "add"
            setattr(self, func_name, self._adding_file(func_name, self._mset, self._fset, None))
            func_name = "madd"
            setattr(self, func_name, self._adding_memory(func_name, self._mset, None))


def unit_test():
    from vstf.common.log import setup_logging
    setup_logging(level=logging.DEBUG, log_file="/var/log/vstf-settings.log", clevel=logging.INFO)

    path = '/etc/vstf'
    setting = DefaultSettings(path)
    filename = 'reporters.mail.mail-settings'
    data = setting.load(filename)

    setting.save(data, filename)
    LOG.info(type(data))
    LOG.info(data)


if __name__ == '__main__':
    unit_test()
