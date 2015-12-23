#!/usr/bin/python
# -*- coding: utf8 -*-
# author: wly
# date: 2015-09-07
# see license for license details
__version__ = ''' '''

import logging
from vstf.controller.reporters.mail.mail import Mail
from vstf.controller.settings.mail_settings import MailSettings
LOG = logging.getLogger(__name__)


class SendMail(object):
    def __init__(self, mail_info):
        self._mail_info = mail_info

    def send(self):
        send = Mail(self._mail_info['server']['host'],
                    self._mail_info['server']['username'],
                    self._mail_info['server']['password']
                    )
        send.attach_addr(self._mail_info['body']['from'], send.FROM)
        send.attach_addr(self._mail_info['body']['to'], send.TO)
        send.attach_addr(self._mail_info['body']['cc'], send.CC)
        send.attach_addr(self._mail_info['body']['bcc'], send.CC)

        LOG.info(self._mail_info['body'])

        if 'attach' in self._mail_info['body']:
            send.attach_files(self._mail_info['body']['attach'])
        send.attach_text(self._mail_info['body']['content'], self._mail_info['body']['subtype'])
        send.attach_title(self._mail_info['body']['subject'])
        send.send()


def unit_test():
    mail_settings = MailSettings()
    mail = SendMail(mail_settings.settings)

    attach_list = ['1', '2']
    mail_settings.set_attach(attach_list)

    context = """
        <!DOCTYPE html>
        <html>
        <head>
        <title>vstf</title>
        </head>
        
        <body>
            hello vstf
        </body>
        
        </html>
    """
    mail_settings.set_subtype('html')
    mail_settings.set_content(context)

    mail.send()


if __name__ == '__main__':
    unit_test()
