#!/usr/bin/python
# -*- coding: utf8 -*-
# author: wly
# date: 2015-05-29
# see license for license details
__version__ = ''' '''

import os

from vstf.controller.reporters.report.pdf.styles import TemplateStyle
from vstf.controller.reporters.report.pdf.pdftemplate import PdfVswitch
from vstf.controller.reporters.report.pdf.story import TitleStory, SpaceStory, ImageStory, LineChartStory, \
    LinePlotStory, uTableStory, Story, TableOfContentsStory, PageBreakStory, ParagraphStory, BarChartStory, cTableStory
from vstf.controller.reporters.report.data_factory import CommonData, ScenarioData, HistoryData
from vstf.controller.database.dbinterface import DbManage
import vstf.controller


class LetterOrder(object):
    def __init__(self):
        self.lettertable = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self._cur = 0
        self._len = len(self.lettertable)

    def get(self):
        return self.lettertable[self._cur]

    def pre(self):
        self._cur = (self._cur + self._len - 1) % self._len

    def next(self):
        self._cur = (self._cur + 1) % self._len


class PdfBase(object):
    def __init__(self):
        self._case = ''
        self._ofile = ''
        self._title = []
        self._story = []
        self._rootdir = os.path.dirname(vstf.controller.__file__) + '/'
        self._pdf = None

    def create_pdf(self):
        style = TemplateStyle(name='default')
        title = self._title
        logo = [self._rootdir + "res/logo.jpg"]
        header = ['']
        footer = [""]
        note = ['', '']
        output = [self._ofile]
        self._pdf = PdfFrameLoss(style, title, logo, header, footer, output, note)

    def save_pdf(self):
        self._pdf.generate(self._story)

    def add_coverpage(self):
        story = Story()
        story = PageBreakStory(story)
        self._story += story.storylist

    def create_story(self):
        raise NotImplementedError("abstract PdfBase")

    def create(self):
        self.create_pdf()
        self.create_story()
        self.save_pdf()


class PdfvSwitchCreator(PdfBase):
    def __init__(self, ofile, common_data, scenario_data, history_data):
        PdfBase.__init__(self)
        self._common = common_data
        self._result = scenario_data
        self._history = history_data
        self._ofile = ofile
        self._chapterid = 0
        self._appendixid = LetterOrder()

    def create_pdf(self):
        style = TemplateStyle(name='default')
        title = self._result.get_covertitle()
        logo = [self._rootdir + "res/logo.jpg"]
        header = ['']
        footer = [""]
        note = ['', '']
        output = [self._ofile]
        self._pdf = PdfVswitch(style, title, logo, header, footer, output, note)

    def get_chapterid(self):
        self._chapterid = self._chapterid + 1
        return self._chapterid

    def create_story(self):
        self.add_coverpage()
        self.add_table_of_contents()
        # self.add_contact()
        # self.add_overview()
        self.add_scenario()
        # self.add_info()
        # self.add_appendix()
        self.add_historys()

    def add_info(self):
        self.add_systeminfo()
        self.add_gitinfo()
        self.add_profile_parameters()
        self.add_testing_options()

    def add_contact(self):
        story = Story()
        story = SpaceStory(story)
        title = ["", "", "", "Reporter"]
        body = self._common.get_contact()
        story = TitleStory(story, data=title, style=7)
        story = ParagraphStory(story, data=body)
        self._story += story.storylist

    def add_table_of_contents(self):
        story = Story()
        story = TableOfContentsStory(story)
        self._story += story.storylist

    def add_overview(self):
        story = Story()
        story = PageBreakStory(story)

        chapterid = self.get_chapterid()
        title = ["%d.Overview" % (chapterid)]
        body = [""]
        story = TitleStory(story, data=title, style=1)
        story = ParagraphStory(story, data=body)

        sectionid = 1
        title = ["%d.%d Components under Test" % (chapterid, sectionid)]
        body = self._common.get_components()
        story = TitleStory(story, data=title, style=2)
        story = ParagraphStory(story, data=body)

        sectionid = sectionid + 1
        title = ["%d.%d Test" % (chapterid, sectionid)]
        body = self._result.get_test()
        story = TitleStory(story, data=title, style=2)
        story = ParagraphStory(story, data=body)

        sectionid = sectionid + 1
        title = ["%d.%d Configuration" % (chapterid, sectionid)]
        story = TitleStory(story, data=title, style=2)

        title = ["Software"]
        body = self._common.get_software()
        story = TitleStory(story, data=title, style=6)
        story = ParagraphStory(story, data=body)

        title = ["Hardware"]
        body = self._common.get_hardware()
        story = TitleStory(story, data=title, style=6)
        story = ParagraphStory(story, data=body)
        self._story += story.storylist

    def add_scenario(self):
        case_list = self._result.get_caselist()
        for case in case_list:
            self.add_case(case)

    def add_case(self, case):
        story = Story()
        chapterid = self.get_chapterid()

        title = ["%d. Case : %s (%s)" % (chapterid, case, self._common.get_casename(case))]

        tools = self._result.get_test_tools(case)
        pic = self._common.get_casefigure(case, tools)
        print pic

        story = TitleStory(story, data=title, style=1)
        story = SpaceStory(story)
        story = ImageStory(story, data=[self._rootdir + pic])
        story = SpaceStory(story)

        sectionid = 1
        story = self.add_summary(story, chapterid, sectionid, case)
        story = SpaceStory(story)

        if self._result.is_throughput_start(case):
            sectionid = sectionid + 1
            story = self.add_throughput_result(story, chapterid, sectionid, case)

        if self._result.is_frameloss_start(case):
            sectionid = sectionid + 1
            story = self.add_frameloss_result(story, chapterid, sectionid, case)

        if self._result.is_latency_start(case):
            sectionid = sectionid + 1
            story = self.add_latency_result(story, chapterid, sectionid, case)

        story = SpaceStory(story)
        story = SpaceStory(story)
        self._story += story.storylist

    def add_summary(self, story, chapterid, sectionid, case):
        title = ["%d.%d Summary" % (chapterid, sectionid)]
        story = TitleStory(story, data=title, style=2)
        provider_list = ["fastlink", "rdp", "l2switch"]
        provider_dict = {"fastlink": "Fast Link", "l2switch": "L2Switch", "rdp": "Kernel RDP"}
        unitid = 1
        case_name = self._common.get_casename(case)
        for provider in provider_list:
            if self._result.is_provider_start(case, provider):
                title = ["%d.%d.%d %s (%s_%s)" % (
                chapterid, sectionid, unitid, provider_dict[provider], case_name, provider)]
                unitid = unitid + 1
                story = TitleStory(story, data=title, style=6)
                test_types = ["throughput", "frameloss"]
                for test_type in test_types:
                    if self._result.is_type_provider_start(case, provider, test_type):
                        story = self.add_summary_type(story, case, provider, test_type)
        return story

    def add_summary_type(self, story, case, provider, test_type):
        bar_list = [test_type, "latency"]
        for item in bar_list:
            bar_data = self._result.get_bardata(case, provider, item)
            story = SpaceStory(story)
            story = BarChartStory(story, data=bar_data)

        table_content = self._result.get_summary_tabledata(case, provider, test_type)
        story = SpaceStory(story)
        story = cTableStory(story, data=table_content, style=3)
        story = SpaceStory(story)
        return story

    def add_throughput_result(self, story, chapterid, sectionid, case):
        title = ["%d.%d Throughput " % (chapterid, sectionid)]
        story = TitleStory(story, data=title, style=2)
        unitid = 1
        title = ["%d.%d.%d Summary" % (chapterid, sectionid, unitid)]
        story = TitleStory(story, data=title, style=6)

        test_type = "throughput"
        unit = 'RX Frame Rate'
        chart_data = self._result.get_frameloss_chartdata(case, test_type)
        table_data = self._result.get_frameloss_tabledata(case, test_type)
        title = [unit + ' (%)']
        story = TitleStory(story, data=title, style=6)
        #       story = SpaceStory(story)
        #       story = LinePlotStory(story, data=chart_data)
        story = SpaceStory(story)
        story = uTableStory(story, data=table_data)
        story = SpaceStory(story)

        unit = 'Frame Loss Rate'
        title = [unit + ' (Mpps)']

        chart_data = self._result.get_framerate_chartdata(case, test_type)
        table_data = self._result.get_framerate_tabledata(case, test_type)
        story = TitleStory(story, data=title, style=6)
        story = SpaceStory(story)
        story = LinePlotStory(story, data=chart_data)
        story = SpaceStory(story)
        story = uTableStory(story, data=table_data)
        story = SpaceStory(story)
        return story

    def add_frameloss_result(self, story, chapterid, sectionid, case):
        title = ["%d.%d Frame Loss Rate " % (chapterid, sectionid)]
        story = TitleStory(story, data=title, style=2)
        unitid = 1
        title = ["%d.%d.%d Summary" % (chapterid, sectionid, unitid)]
        story = TitleStory(story, data=title, style=6)

        test_type = "frameloss"
        unit = 'RX Frame Rate'
        chart_data = self._result.get_frameloss_chartdata(case, test_type)
        table_data = self._result.get_frameloss_tabledata(case, test_type)
        title = [unit + ' (%)']
        story = TitleStory(story, data=title, style=6)
        #       story = SpaceStory(story)
        #       story = LineChartStory(story, data=chart_data)
        story = SpaceStory(story)
        story = uTableStory(story, data=table_data)
        story = SpaceStory(story)

        unit = 'Frame Loss Rate'
        title = [unit + ' (Mpps)']

        chart_data = self._result.get_framerate_chartdata(case, test_type)
        table_data = self._result.get_framerate_tabledata(case, test_type)
        story = TitleStory(story, data=title, style=6)
        story = SpaceStory(story)
        story = LineChartStory(story, data=chart_data)
        story = SpaceStory(story)
        story = uTableStory(story, data=table_data)
        story = SpaceStory(story)
        return story

    def add_latency_result(self, story, chapterid, sectionid, case):
        title = ["%d.%d Latency " % (chapterid, sectionid)]
        story = TitleStory(story, data=title, style=2)
        unitid = 1
        title = ["%d.%d.%d Summary" % (chapterid, sectionid, unitid)]
        story = TitleStory(story, data=title, style=6)

        unit = 'Average Latency'
        title = [unit + ' (uSec)']
        #       chart_data = self._result.get_latency_chartdata(case)
        bar_data = self._result.get_latency_bardata(case)
        table_data = self._result.get_latency_tabledata(case)
        story = TitleStory(story, data=title, style=6)
        story = SpaceStory(story)
        #       story = LineChartStory(story, data=chart_data)
        story = BarChartStory(story, data=bar_data)

        story = SpaceStory(story)
        story = uTableStory(story, data=table_data)
        story = SpaceStory(story)
        return story

    def add_systeminfo(self):
        story = Story()
        chapterid = self.get_chapterid()
        story = SpaceStory(story)
        title = ["%d. System Information " % (chapterid)]
        story = PageBreakStory(story)
        story = TitleStory(story, data=title, style=1)
        table_content = self._common.get_systeminfo_tabledata()
        story = SpaceStory(story)
        story = cTableStory(story, data=table_content, style=0)
        story = SpaceStory(story)
        self._story += story.storylist

    def add_gitinfo(self):
        story = Story()
        chapterid = self.get_chapterid()
        title = ["%d. Git Repository Information " % (chapterid)]
        story = TitleStory(story, data=title, style=1)

        table_content = self._common.get_gitinfo_tabledata()
        if table_content:
            story = SpaceStory(story)
            story = cTableStory(story, data=table_content, style=5)
            story = SpaceStory(story)
        self._story += story.storylist

    def add_testing_options(self):
        story = Story()
        chapterid = self.get_chapterid()
        story = SpaceStory(story)
        title = ["%d. Testing Options" % (chapterid)]

        story = TitleStory(story, data=title, style=1)
        table_content = self._common.get_testingoptions_tabledata()
        story = SpaceStory(story)
        story = cTableStory(story, data=table_content, style=1)
        story = SpaceStory(story)
        self._story += story.storylist

    def add_profile_parameters(self):
        story = Story()
        chapterid = self.get_chapterid()
        story = PageBreakStory(story)
        title = ["%d. " % (chapterid)]
        story = TitleStory(story, data=title, style=1)
        table_content = self._common.get_profileparameters_tabledData()
        story = SpaceStory(story)
        story = cTableStory(story, data=table_content, style=2)
        story = SpaceStory(story)
        self._story += story.storylist

    def add_appendix(self):
        story = Story()
        story = PageBreakStory(story)

        title = ["<b>Appendix %s: vSwitching Testing Methodology</b>" % (self._appendixid.get())]
        self._appendixid.next()
        story = TitleStory(story, data=title, style=1)
        filename = "res/Traffic-types.jpg"
        story = SpaceStory(story)
        story = ImageStory(story, data=[self._rootdir + filename])
        #       story = SpaceStory(story)

        title = ["Traffic Patterns: "]
        story = TitleStory(story, data=title, style=6)

        body = [
            "<b>Ti</b>  - South North Traffic",
            "<b>Tu</b>  - East Eest Traffic",
            "<b>Tn</b>  - Physical host or VM loop back",
            "<b>Tnv</b>  - Virtual Machine loop back",
        ]
        story = ParagraphStory(story, data=body)

        title = ["<b>Performance Testing Coverage </b> (version 0.1):"]
        story = TitleStory(story, data=title, style=6)

        table_content = self._common.get_introduct_tabledata()
        story = SpaceStory(story)
        story = cTableStory(story, data=table_content, style=4)
        self._story += story.storylist

    def add_historys(self):
        case_list = self._result.get_caselist()
        for case in case_list:
            history = self._history.get_history_info(case)
            if history:
                self.add_history(case, history)

    def add_history(self, case, history):
        story = Story()
        story = PageBreakStory(story)

        title = ["<b>Appendix %s : %s History Records</b>" % (self._appendixid.get(), case)]
        story = TitleStory(story, data=title, style=1)

        for i in range(len(history)):
            title = ["%s.%s %s" % (self._appendixid.get(), i, history[i]["title"])]
            story = TitleStory(story, data=title, style=2)

            section = history[i]["data"]
            for unit in section:
                title = [unit['title']]
                story = TitleStory(story, data=title, style=6)
                content = unit['data']
                story = uTableStory(story, data=content)

        self._appendixid.next()
        self._story += story.storylist


def main():
    dbase = DbManage()
    taskid = dbase.get_last_taskid()
    common_data = CommonData(taskid, dbase)
    scenario_list = common_data.get_scenariolist()
    history_data = HistoryData(taskid, dbase)
    for scenario in scenario_list:
        out_file = "vstf_report_%s.pdf" % (scenario)
        scenario_data = ScenarioData(taskid, dbase, scenario)
        reporter = PdfvSwitchCreator(out_file, common_data, scenario_data, history_data)
        if reporter:
            reporter.create()


if __name__ == '__main__':
    main()
