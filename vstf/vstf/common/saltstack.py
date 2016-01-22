##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import os
import sys
import inspect
import logging
import salt.client as sclient

from vstf.common import cmds

log = logging.getLogger(__name__)


class Mysalt(object):
    IS_DIR = 1
    IS_FILE = 2
    FAILED = -1

    def __init__(self):
        self.cur_path = os.path.abspath(os.path.dirname(inspect.stack()[1][1]))
        self.salt_conf = "/etc/salt/master"
        if not os.path.exists(self.salt_conf):
            raise Exception("this python must be run on the salt master.")
        self.pillar_path = str(
            cmds.execute("grep '^pillar_roots' \
                    /etc/salt/master -A 2 | sed 1,2d | awk '{print $2}'") + '/')
        if self.pillar_path == "":
            log.warning("pillar path not found, make sure the pillar_roots configed")
        else:
            os.system("mkdir -p " + self.pillar_path)

        self.state_path = str(cmds.execute("grep '^file_roots' \
            /etc/salt/master -A 2 | sed 1,2d | awk '{print $2}'") + '/')
        if self.state_path == "":
            log.warning("state path not found, make sure the file_roots configed")
        else:
            os.system("mkdir -p " + self.state_path)

        self.salt = sclient.LocalClient()

    def slave_exists(self, host):
        pslave = "/etc/salt/pki/master/minions/" + host
        if os.path.exists(pslave):
            return True
        else:
            return False

    def __is_dir_or_file(self, src):
        if not os.path.exists(src):
            return self.FAILED
        if os.path.isdir(src):
            return self.IS_DIR
        elif os.path.isfile(src):
            return self.IS_FILE
        else:
            return self.FAILED

    def __copy_target(self, target, flag=""):
        if not os.path.exists(target):
            log.error("target %(d)s  not exists.", {'d': target})
            return False

        if flag == "pillar":
            dst = self.pillar_path
        elif flag == "state":
            dst = self.state_path
        else:
            log.error("this file or dir not pillar or state, can not support now.")
            return False

        if self.IS_FILE == self.__is_dir_or_file(target):
            os.system('cp ' + target + ' ' + dst)
        else:
            os.system("cp -r " + target + ' ' + dst)
        return True

    def copy(self, host, src, dst):
        """copy file or dir to slave.
        :src a file or a dir
        :dst if src is a file, the dst must be like this /home/xx.py, not /home
        """

        '''check if the host exists on the master'''
        if not self.slave_exists(host):
            log.error("the host %(h)s is not held by master, please check.")
            return False

        '''copy file to salt's file_roots'''
        if not self.__copy_target(src, "state"):
            return False

        if self.IS_DIR == self.__is_dir_or_file(src):
            dir_name = os.path.basename(src)
            self.salt.cmd(host, "cp.get_dir", ["salt://" + dir_name, dst])
        elif self.IS_FILE == self.__is_dir_or_file(src):
            file_name = os.path.basename(src)
            print self.salt.cmd(host, "cp.get_file", ["salt://" + file_name, dst])
        else:
            log.error("not file and not dir, what is it")
            return False
        return True

    def __luxuriant_line(self, str, color):
        if "red" == color:
            return "\033[22;35;40m" + str + "\033[0m"
        elif "green" == color:
            return "\033[22;32;40m" + str + "\033[0m"
        else:
            return str

    def result_check(self, ret, host):
        num_s = 0
        num_f = 0
        msg = ""
        try:
            for key in ret[host].keys():
                if True == ret[host][key]['result']:
                    num_s += 1
                else:
                    num_f += 1
                    msg = msg + self.__luxuriant_line("Failed %d:\n" % num_f, "red")
                    msg = msg + "\t" + key + '\n'
                    msg = msg + self.__luxuriant_line("\t%s\n" % ret[host][key]['comment'], "red")
                    if True == ret[host][key]['changes'].has_key('retcode'):
                        msg = msg + "RETCODE: %s\n" % (ret[host][key]['changes']['retcode'])
                    if True == ret[host][key]['changes'].has_key('stderr'):
                        msg = msg + "STDERR: %s\n" % (ret[host][key]['changes']['stderr'])
                    if True == ret[host][key]['changes'].has_key('stdout'):
                        msg = msg + "STDOUT: %s\n" % (ret[host][key]['changes']['stdout'])
            msg = msg + self.__luxuriant_line("total success: %d\n" % num_s, "green")
            msg = msg + self.__luxuriant_line("failed: %d\n" % num_f, "red")
        except Exception as e:
            log.error("sorry, thy to check result happend error, <%(e)s>.\nret:%(ret)s",
                      {'e': e, 'ret': ret})
            return -1
        log.info(':\n' + msg)
        return num_f

    def run_state(self, host, fstate, ext_pillar={}, care_result=True):
        try:
            log.info("salt " + host + " state.sls " +
                     fstate + ' pillar=\'' + str(ext_pillar) + '\'')
            ret = self.salt.cmd(host, 'state.sls', [fstate, 'pillar=' + str(ext_pillar)], 180, 'list')
        except Exception as e:
            log.error("try to init host %(host)s happend error: <%(e)s>.",
                      {'host': host, 'e': e})
            if True == care_result:
                raise e

        if 0 != self.result_check(ret, host) and care_result:
            sys.exit(-1)
        return True

    def salt_cmd(self, host, cmd):
        # import pdb
        # pdb.set_trace()
        logging.info("Begin to run cmd %s on %s" % (host, cmd))

        try:
            ret = self.salt.cmd(host, 'cmd.run', [cmd])
        except Exception:
            log.error("Remote salt execute failed.")
        return ret

    def copy_by_state(self, host, src, state_cmd, **kwargs):
        '''the src must be a dir, and the state.sls 
        must be the name of the dir name'''

        if not self.slave_exists(host):
            log.error("the host %(h)s is not held by master, please check.")
            return False

        if not self.__copy_target(src, "state"):
            return False

        return self.run_state(host, state_cmd, kwargs, care_result=True)

    def get_master_ip(self, host=None):
        if not host:
            ret = cmds.execute("grep '^interface:' /etc/salt/master | awk '{print $2}'").strip()
            return ret
        try:
            ret = self.salt.cmd(host, "grains.item", ["master"])[host]['master']
        except Exception:
            log.error("salt happened error when get master ip")
            return ""
        return ret


mysalt = Mysalt()
