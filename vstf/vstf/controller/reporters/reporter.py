##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import os
import argparse
import logging
import time

from vstf.controller.reporters.report.provider.html_provider import HtmlProvider
from vstf.controller.reporters.report.provider.pdf_provider import PdfProvider
from vstf.controller.settings.template_settings import TemplateSettings
from vstf.controller.reporters.report.data_factory import TaskData
from vstf.controller.reporters.report.html.htmlcreator import HtmlCreator
from vstf.controller.reporters.report.pdf.pdfcreator import PdfCreator
from vstf.controller.database.dbinterface import DbManage
from vstf.controller.settings.mail_settings import MailSettings
from vstf.controller.reporters.mail.sendmail import SendMail
from vstf.controller.settings.html_settings import HtmlSettings
from vstf.controller.reporters.report.candy_generator import CandyGenerator
import vstf.common.constants as cst


__version__ = ''' '''
LOG = logging.getLogger(__name__)


class Report(object):
    def __init__(self, dbase, rpath):
        """

        :type dbase: object DbManage
        """
        self._dbase = dbase
        self._rpath = "."
        self._mail_settings = MailSettings()
        if os.path.exists(rpath):
            self._rpath = rpath

    def create_pdf(self, taskid):
        task = TaskData(taskid, self._dbase)
        scenario_list = task.common.get_scenariolist()
        creator = CandyGenerator(task)
        attach_list = []
        for scenario in scenario_list:
            out_file = os.path.join(self._rpath, "vstf_report_%s_%s.pdf" % (scenario, time.strftime(cst.TIME_FORMAT3)))
            LOG.info(out_file)
            creator.create(scenario)
            info = TemplateSettings()
            provider = PdfProvider(info.settings)
            reporter = PdfCreator(provider)
            reporter.create(out_file)
            attach_list.append(out_file)

        if attach_list:
            self._mail_settings.mset_attach(attach_list)

    def create_html(self, taskid):
        task = TaskData(taskid, self._dbase)

        creator = CandyGenerator(task)
        creator.create_all()

        html_settings = HtmlSettings()
        info = TemplateSettings()
        LOG.info(html_settings.settings)

        provider = HtmlProvider(info.settings, html_settings.settings)
        out_file = os.path.join(self._rpath, "mail.html")
        LOG.info(out_file)

        html = HtmlCreator(provider)
        content = html.create(out_file)

        self._mail_settings.mset_subtype('html')
        self._mail_settings.mset_content(content)

    def report(self, taskid, mail_off):
        self._mail_settings = MailSettings()
        mail = SendMail(self._mail_settings.settings)
        self.create_pdf(taskid)
        self.create_html(taskid)
        if not mail_off:
            mail.send()


def main():
    from vstf.common.log import setup_logging
    setup_logging(level=logging.DEBUG, log_file="/var/log/vstf/vstf-reporter.log", clevel=logging.INFO)

    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('-rpath',
                        action='store',
                        default='./',
                        type=str,
                        help=" the path name of test results  "
                        )
    parser.add_argument('-mail_off',
                        action='store_true',
                        help="is need send mail the for the report"
                        )
    parser.add_argument('--taskid',
                        action='store',
                        default=-1,
                        help="report depand of a history task id."
                        )
    args = parser.parse_args()
    dbase = DbManage()

    report = Report(dbase, args.rpath)
    if args.taskid == -1:
        taskid = dbase.get_last_taskid()
    else:
        taskid = args.taskid
    report.report(taskid, args.mail_off)


if __name__ == '__main__':
    main()
