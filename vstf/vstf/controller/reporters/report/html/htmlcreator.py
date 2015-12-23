#!/usr/bin/python
# -*- coding: utf8 -*-
# author: wly
# date: 2015-08-04
# see license for license details
__version__ = ''' '''

import logging

from vstf.controller.reporters.report.data_factory import TaskData
from vstf.controller.database.dbinterface import DbManage
from vstf.controller.reporters.report.html.html_base import *

LOG = logging.getLogger(__name__)


class HtmlvSwitchCreator(HtmlBase):
    def __init__(self, task_data, provider, ofile='creator.html'):
        HtmlBase.__init__(self, provider, ofile)
        self._task = task_data
        self._table_type = 'html'

    def create_story(self):
        self.add_subject()
        self.add_gitinfo()
        self.add_envinfo()
        self.add_scenarios()

    def add_subject(self):
        job_name = "JOB_NAME: " + self._task.common.get_taskname()
        self._page << H2(job_name)

    def add_gitinfo(self):
        self._page << H2("Trigger and Repository Info")

        git_table = self._task.common.get_gitinfo_tabledata()
        if git_table:
            self.add_table(git_table)

    def add_envinfo(self):
        self._page << H2("System Environment Information")
        env_table = self._task.common.get_systeminfo()
        LOG.info(env_table)
        if env_table:
            self.add_table(env_table)

    def add_scenarios(self):
        scenario_list = self._task.common.get_scenariolist()
        self._page << H2("Scenario List: " + ', '.join(scenario_list))
        for scenario in scenario_list:
            self._page << H2("Scenario: " + scenario)
            data = getattr(self._task, scenario)
            self.add_scenario(data)

    def add_scenario(self, scenario_data):
        case_list = scenario_data.get_caselist()
        for case in case_list:
            self.add_case(scenario_data, case)

    def add_case(self, scenario_data, case):
        case_name = self._task.common.get_casename(case)
        title = "Case : %s (%s)" % (case, case_name)
        self._page << H2(title)

        provider_list = ["fastlink", "rdp", "l2switch"]
        provider_dict = {"fastlink": "Fast Link", "l2switch": "L2Switch", "rdp": "Kernel RDP"}

        for provider in provider_list:
            if scenario_data.is_provider_start(case, provider):
                title = " %s (%s_%s)" % (provider_dict[provider], case_name, provider)
                self._page << H3(title)
                test_types = ["throughput", "frameloss"]
                for test_type in test_types:
                    if scenario_data.is_type_provider_start(case, provider, test_type):
                        self.add_casedata(scenario_data, case, provider, test_type)

        if scenario_data.is_latency_start(case):
            self.add_latency_result(scenario_data, case)

    def add_casedata(self, scenario_data, case, provider, test_type):
        table_content = scenario_data.get_summary_tabledata(case, provider, test_type, self._table_type)
        if table_content:
            title = "Test type:%s" % (test_type)
            self._page << H4(title)
            self.add_table(table_content)

    def add_latency_result(self, scenario_data, case):
        title = "Average Latency Summary"
        table_content = scenario_data.get_latency_tabledata(case)
        if table_content:
            self._page << H2(title)
            self.add_table(table_content)


def unit_test():
    from vstf.common.log import setup_logging
    setup_logging(level=logging.DEBUG, log_file="/var/log/html-creator.log", clevel=logging.INFO)

    dbase = DbManage()
    taskid = dbase.get_last_taskid()
    task_data = TaskData(taskid, dbase)

    from vstf.controller.settings.html_settings import HtmlSettings
    from vstf.controller.reporters.report.provider.html_provider import StyleProvider

    html_settings = HtmlSettings()
    LOG.info(html_settings.settings)

    provider = StyleProvider(html_settings.settings)
    html = HtmlvSwitchCreator(task_data, provider)

    result = html.create(True)
    print result


if __name__ == '__main__':
    unit_test()
