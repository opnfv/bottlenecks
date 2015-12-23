#!/usr/bin/env python
# -*- coding: utf8 -*-
# author: wly
# date: 2015-09-06
# see license for license details

import logging
import pprint

import vstf.controller.settings.settings as sets
import vstf.common.decorator as deco
from vstf.common.input import raw_choice

LOG = logging.getLogger(__name__)


class MailSettings(sets.Settings):
    def __init__(self, path="/etc/vstf", filename="reporters.mail.mail-settings", mode=sets.SETS_DEFAULT):
        super(MailSettings, self).__init__(path, filename, mode)

    def _register_func(self):
        super(MailSettings, self)._register_func()
        body = set(
            self._fset['body'].keys()
        )
        LOG.debug(body)
        for item in body:
            item = item.encode()
            func_name = "set_%s" % item
            setattr(self, func_name, self._setting_file(func_name, self._mset['body'], self._fset['body'], item))
        other = {"attach", "content", "subtype"}
        for item in other:
            func_name = "mset_%s" % item
            setattr(self, func_name, self._setting_memory(func_name, self._mset['body'], item))

        LOG.debug(self.__dict__)

    def sinput(self):
        if raw_choice("if set mail server"):
            server = self.raw_server()
            self.set_server(server)

        if raw_choice("if set mail body"):
            body = self.raw_body()
            self.set_body(body)
        print "%s set finish: " % (self._filename)
        print "+++++++++++++++++++++++++++++++++++++++++"
        pprint.pprint(self.settings, indent=4)
        print "+++++++++++++++++++++++++++++++++++++++++"

    @deco.vstf_input("password", types=str)
    @deco.vstf_input("username", types=str)
    @deco.vstf_input('host', types=str)
    def raw_server(self):
        print "---------------------------------------"
        print "Please vstf set mail server info like:"
        print "    'host': 'localhost',"
        print "    'username': 'user',['\\n' = None]"
        print "    'password': '******',['\\n' = None]"
        print "---------------------------------------"

    @deco.vstf_input("subject", types=str, default='vstf mail')
    @deco.vstf_input("bcc", types=list, default=[])
    @deco.vstf_input("cc", types=list, default=[])
    @deco.vstf_input("to", types=list, default=[])
    @deco.vstf_input('from', types=list, default=['vstf_from@vstf.com'])
    def raw_body(self):
        print "----------------------------------------------------"
        print "Please vstf set mail server info like:"
        print "    'from': ['vstf_from@vstf.com'],"
        print "    'to': ['vstf_to@vstf.com'],"
        print "    'cc': ['vstf_cc@vstf.com']"
        print "    'bcc': ['vstf_bcc@vstf.com']"
        print "    'subject': Vstf Performance Test Report"
        print "----------------------------------------------------"


def unit_test():
    from vstf.common.log import setup_logging
    setup_logging(level=logging.DEBUG, log_file="/var/log/vstf/vstf-mail-settings.log", clevel=logging.INFO)

    mail_settings = MailSettings()
    mail_settings.sinput()

    return

    mail_server = {
        "host": "localhost",
        "username": None,
        "password": None
    }
    mail_settings.set_server(mail_server)

    from_list = ['vstf_from@vstf.com']
    mail_settings.set_from(from_list)
    to_list = ['wangli11@huawei.com']
    mail_settings.set_to(to_list)
    cc_list = ['wangli11@huawei.com']
    mail_settings.set_cc(cc_list)
    bcc_list = ['wangli11@huawei.com']
    mail_settings.set_bcc(bcc_list)
    bcc_list = ['wangli11@huawei.com']
    mail_settings.set_bcc(bcc_list)

    subject = "Virtual Switching Performance Test Report"
    mail_settings.set_subject(subject)

    subtype = "plain"
    mail_settings.mset_subtype(subtype)

    attach_list = []
    mail_settings.mset_attach(attach_list)

    content = "this is a test"
    mail_settings.mset_content(content)

    LOG.info(mail_settings.settings)


if __name__ == '__main__':
    unit_test()
