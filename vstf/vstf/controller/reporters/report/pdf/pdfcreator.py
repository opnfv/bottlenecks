##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

__version__ = ''' '''


from vstf.controller.reporters.report.pdf.pdftemplate import PdfVswitch
from vstf.controller.reporters.report.pdf.story import TitleStory, SpaceStory, ImageStory, TableStory, \
    LinePlotStory, Story, TableOfContentsStory, PageBreakStory, ParagraphStory, BarChartStory
import vstf.common.candy_text as candy
from vstf.controller.reporters.report.provider.pdf_provider import PdfProvider
from vstf.controller.settings.template_settings import TemplateSettings

import os
import logging

LOG = logging.getLogger(__name__)


class PdfCreator(object):
    def __init__(self, provider):
        self._provider = provider
        self._story = []
        self._pdf = None

    def create_pdf(self):
        theme = self._provider.get_theme
        self._pdf = PdfVswitch(theme["title"],
                               theme["logo"],
                               theme["header"],
                               theme["footer"],
                               theme["note"],
                               theme["style"])

    def save_pdf(self, ofile):
        self._pdf.generate(self._story, ofile)

    def add_coverpage(self):
        story = Story()
        story = PageBreakStory(story)
        self._story += story.storylist

    def add_contents(self):
        if self._provider.ifcontents:
            story = Story()
            story = TableOfContentsStory(story)
            self._story += story.storylist

    def create_story(self):
        self.add_coverpage()
        self.add_contents()
        self.add_context()

    def create(self, ofile):
        self.create_pdf()
        self.create_story()
        self.save_pdf(ofile)

    def add_context(self):
        context = self._provider.get_context
        self._story += self._raw_context(context)

    def _raw_context(self, context, ci=0, si=0, ui=0, level=-1):
        _story = []
        for key, value in sorted(context.items()):
            LOG.info(key)
            LOG.info(value)
            _sn, _node, _style = candy.text2tuple(key)
            if _node in candy.dom:
                if _node == candy.chapter:
                    ci = _style
                elif _node == candy.section:
                    si = _style
                else:
                    ui = _style
                _story += self._raw_context(value, ci, si, ui, level + 1)

            else:
                story = Story()
                LOG.info("node: %s  %s" % (_node, candy.title))
                if _node == candy.title:
                    assert value
                    if level in range(len(candy.dom)):
                        if level == 0:
                            value[0] = "Chapter %s %s" % (ci, value[0])
                            story = PageBreakStory(story)
                        elif level == 1:
                            value[0] = "%s.%s %s" % (ci, si, value[0])
                        else:
                            value[0] = "%s.%s.%s %s" % (ci, si, ui, value[0])
                        LOG.info(value)
                        story = TitleStory(story, data=value, style=_style)
                elif _node == candy.table:
                    story = TableStory(story, data=value, style=_style)
                elif _node == candy.figure:
                    story = ImageStory(story, data=value, style=_style)
                elif _node == candy.paragraph:
                    story = ParagraphStory(story, data=value, style=_style)
                elif _node == candy.plot:
                    story = LinePlotStory(story, data=value, style=_style)
                elif _node == candy.chart:
                    story = BarChartStory(story, data=value, style=_style)
                elif _node == candy.space:
                    assert isinstance(value, int)
                    for i in range(value):
                        story = SpaceStory(story)
                _story += story.storylist
        return _story


def main():
    from vstf.common.log import setup_logging
    setup_logging(level=logging.DEBUG, log_file="/var/log/pdf-creator.log", clevel=logging.INFO)

    out_file = "vstf_report.pdf"

    info = TemplateSettings()
    provider = PdfProvider(info.settings)
    reporter = PdfCreator(provider)
    reporter.create(out_file)

if __name__ == '__main__':
    main()
