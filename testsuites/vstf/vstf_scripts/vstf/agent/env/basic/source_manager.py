##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import os
import logging
import contextlib
from subprocess import CalledProcessError
from vstf.common.utils import check_call

LOG = logging.getLogger(__name__)


@contextlib.contextmanager
def my_chdir(file_path):
    old_cwd = os.path.realpath(os.curdir)
    os.chdir(file_path)
    LOG.info("cd %s", file_path)
    yield
    os.chdir(old_cwd)
    LOG.info("cd %s", old_cwd)


class SourceCodeManager(object):

    def __init__(self):
        super(SourceCodeManager, self).__init__()
        self.base_path = '/opt/vstf/'

    @staticmethod
    def _git_pull(url, dest):
        if not os.path.isdir(dest):
            check_call("git clone %s %s" % (url, dest), shell=True)
        else:
            with my_chdir(dest):
                check_call("git pull", shell=True)

    @staticmethod
    def _install(dest):
        with my_chdir(dest):
            try:
                check_call("make && make install", shell=True)
            except CalledProcessError:
                LOG.info("retry make again")
                check_call("make clean; make && make install", shell=True)

    def src_install(self, cfg):
        for key, item in cfg.items():
            repo_type = item['repo_type']
            url = item['url']
            install = item['install']
            if install is True:
                LOG.info("installing src repo:%s", key)
                if repo_type == "git":
                    target = self.base_path + key
                    self._git_pull(url, target)
                    self._install(target)
                else:
                    raise Exception("unsupported repo type:%s" % repo_type)
            else:
                LOG.info("skip src repo:%s", key)
        return True


if __name__ == '__main__':
    import argparse
    import json
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='config file to parse')
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    cfg = json.load(open(args.config))
    mgr = SourceCodeManager()
    mgr.src_install(cfg)
