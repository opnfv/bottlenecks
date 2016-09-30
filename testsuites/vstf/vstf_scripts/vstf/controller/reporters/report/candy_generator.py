##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from vstf.controller.settings.template_settings import TemplateSettings
from vstf.controller.reporters.report.data_factory import TaskData
from vstf.controller.database.dbinterface import DbManage
import vstf.common.candy_text as candy
import logging
LOG = logging.getLogger(__name__)


class CandyGenerator(object):

    def __init__(self, task):
        self._task = task

    def create(self, scenario):
        context = {}

        sn = 1
        chapterid = 1
        name = candy.tuple2text(sn, candy.chapter, chapterid)
        context[name] = self.create_env()

        sn += 1
        chapterid += 1
        name = candy.tuple2text(sn, candy.chapter, chapterid)
        context[name] = self.create_scenario(scenario)

        template = TemplateSettings()
        template.set_context(context)
        LOG.info(template.settings)

    def create_all(self):
        context = {}

        sn = 1
        chapterid = 1
        name = candy.tuple2text(sn, candy.chapter, chapterid)
        context[name] = self.create_env()

        scenarios = self._task.common.get_scenariolist()
        for scenario in scenarios:
            sn += 1
            chapterid += 1
            name = candy.tuple2text(sn, candy.chapter, chapterid)
            context[name] = self.create_scenario(scenario)

        template = TemplateSettings()
        template.set_context(context)
        LOG.info(template.settings)

    def create_env(self):
        env = {
            "01##title#1": ["System Environment"],
            "02##table#2": self._task.common.get_systeminfo()
        }
        return env

    def create_scenario(self, scenario):
        scenario_chapter = {
            "01##title#1": ["Scenario Result"]
        }
        scenario_data = getattr(self._task, scenario)
        test_list = scenario_data.get_testlist()
        sectionid = 0
        sn = 1
        for test in test_list:
            sn += 1
            sectionid += 1
            name = candy.tuple2text(sn, candy.section, sectionid)
            testid = test.TestID
            case = test.CaseTag.decode()
            ttype = test.Type.decode()

            params_info = [
                "  Case: " + case,
                "  Test tool: " + test.Tools.decode(),
                "  vSwitch: " + test.Switch.decode(),
                "  Protocol: " + test.Protocol.decode(),
                "  Type: " + ttype
            ]
            if ttype in ["frameloss", "throughput"]:
                draw = {
                    "style": 1,
                    "node": candy.plot,
                    "data": scenario_data.get_framerate_chartdata(case, ttype)
                }
                table = scenario_data.get_ratedata(testid, ttype)
            else:
                draw = {
                    "style": 1,
                    "node": candy.chart,
                    "data": scenario_data.get_latency_bardata(case)
                }
                table = scenario_data.get_latency_tabledata(case)
            test_section = self.create_test(
                sectionid, params_info, table, draw)
            scenario_chapter[name] = test_section

        return scenario_chapter

    def create_test(self, section, info, table, draw):
        """

        :rtype : dict
        """
        sn = 7
        draw_name = candy.tuple2text(sn, draw["node"], draw["style"])
        case_section = {
            "01##title#2": ["Test ID: %s" % section],
            "02##paragraph#2": ["Parameter"],
            "03##paragraph#3": info,
            "04##paragraph#2": ["Result"],
            "05##table#2": table,
            "06##space#2": 2,
            draw_name: draw["data"]
        }
        return case_section


def main():
    from vstf.common.log import setup_logging
    setup_logging(
        level=logging.DEBUG,
        log_file="/var/log/vstf/vstf-candy.log",
        clevel=logging.INFO)

    dbase = DbManage()
    taskid = dbase.get_last_taskid()
    task = TaskData(taskid, dbase)
    creator = CandyGenerator(task)

    creator.create("Tn")
if __name__ == '__main__':
    main()
