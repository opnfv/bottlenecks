##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import smtplib
import logging
import os
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

LOG = logging.getLogger(__name__)
SRV = 'localhost'
USER = None
PASSWD = None


class Mail(object):
    def __init__(self, srv=SRV, user=USER, passwd=PASSWD):
        self.srv = srv
        self.user = USER
        self.passwd = PASSWD
        self._msg = MIMEMultipart('mixed')

        # addr type
        self.TO = "To"
        self.FROM = "From"
        self.CC = "Cc"
        self.BCC = "Bcc"
        self.__addr_choice = [self.TO, self.FROM, self.CC, self.BCC]

        # text mode
        self.HTML = "html"
        self.PLAIN = "plain"
        self.__mode = [self.HTML, self.PLAIN]
        # self._charset = 'gb2312'

        # timeout
        self.timeout = 10

    def attach_addr(self, addr, addr_type):
        """
        :param addr: a list of email address.
        :param addr_type: must be one of [to, from, cc, bcc]
        """
        if not addr or not isinstance(addr, list):
            LOG.error("The addr must be a list")
            return False

        if addr_type not in self.__addr_choice:
            LOG.error("Not support addr type")
            return False

        if not self._msg[addr_type]:
            self._msg[addr_type] = ','.join(addr)
        self._msg[addr_type].join(addr)

    def attach_title(self, title):
        """Notice:
        each time attach title, the old title will be covered.
        """
        if title:
            self._msg["Subject"] = str(title)

    def attach_text(self, text, mode):
        if mode not in self.__mode:
            LOG.error("The text mode not support.")
            return False

        msg_alternative = MIMEMultipart('alternative')
        msg_text = MIMEText(text, mode)
        msg_alternative.attach(msg_text)

        return self._msg.attach(msg_alternative)

    def attach_files(self, files):
        for _file in files:
            part = MIMEApplication(open(_file, "rb").read())
            part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(_file))
            self._msg.attach(part)

    def send(self):
        server = smtplib.SMTP(self.srv, timeout=self.timeout)
        if self.user:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(self.user, self.passwd)
        maillist = []
        if self._msg[self.TO]:
            maillist += self._msg[self.TO].split(',')
        if self._msg[self.CC]:
            maillist += self._msg[self.CC].split(',')
        if self._msg[self.BCC]:
            maillist += self._msg[self.BCC].split(',')
        ret = server.sendmail(self._msg[self.FROM].split(','),
                              maillist, self._msg.as_string())
        LOG.info("send mail ret:%s", ret)
        server.close()


if __name__ == "__main__":
    m = Mail()
    m.attach_addr(["vstf_server@vstf.com"], m.FROM)
    m.attach_addr(["wangli11@huawei.com"], m.TO)
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
    m.attach_text(context, m.HTML)
    m.attach_title("Email from xeson Check")
    m.send()
