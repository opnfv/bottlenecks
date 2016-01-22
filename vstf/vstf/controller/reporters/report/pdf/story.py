##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

__doc__ = """
Story Decorator contains ImageStory, HeaderStory, PageBreakStory,
TableStory, LinePlotStory, TitleStory, ParagraphStory
"""
import sys
import os
from reportlab.platypus import PageBreak
from reportlab.lib import colors
from reportlab.platypus.tableofcontents import TableOfContents
from styles import *
from element import *


class Story(object):
    def __init__(self):
        self._storylist = []

    @property
    def storylist(self):
        return self._storylist


class StoryDecorator(Story):
    def __init__(self, story, data=None, style=None):
        self._story = story
        self._data = data
        self._style = style
        print self._data
        self.new_story()

    #       print self._story.storylist
    @property
    def storylist(self):
        return self._story.storylist

    def new_story(self):
        raise NotImplementedError("abstract StoryDecorator")


class ImageStory(StoryDecorator):
    def new_story(self):
        print "Image Story"
        for filename in self._data:
            if os.path.exists(filename) == False:
                print "not find %s" % filename
                continue
            if 'Traffic-types' in filename:
                style = is_traffic
                image_height = style.image_height
                image_width = style.image_width
                image_hAlign = style.image_hAlign
                image_vAlign = style.image_vAlign
                self._story.storylist.append(
                    eImage(filename, image_width, image_height, hAlign=image_hAlign, vAlign=image_vAlign))
            else:
                style = is_default
                image_height = style.image_height
                image_width = style.image_width
                image_hAlign = style.image_hAlign
                image_vAlign = style.image_vAlign
                #    self._story.storylist.append(eGraphicsTable([[' ' * 5, eImage(filename, image_width, image_height, hAlign=image_hAlign, vAlign=image_vAlign)]], ts_left).table)
                self._story.storylist.append(
                    eImage(filename, image_width, image_height, hAlign=image_hAlign, vAlign=image_vAlign))


class HeaderStory(StoryDecorator):
    def new_story(self):
        print "header story"
        self._story.storylist.append(PageBreak())


class PageBreakStory(StoryDecorator):
    def new_story(self):
        print "PageBreak story"
        self._story.storylist.append(PageBreak())


class TableOfContentsStory(StoryDecorator):
    def new_story(self):
        print "TableOfContents story"
        self._data = [" ", " ", "Table Of Contents", ""]
        style = ps_head_lv4
        self._story.storylist.append(eParagraph(self._data, style).para)
        toc = TableOfContents()
        toc.levelStyles = [ps_head_lv7, ps_head_lv8, ps_head_lv9]
        self._story.storylist.append(toc)


class SpaceStory(StoryDecorator):
    def new_story(self):
        style = ps_space
        self._story.storylist.append(eParagraph([" ", " "], style).para)


class TableStory(StoryDecorator):
    def new_story(self):
        print "table story"
        style = ts_default
        if self._style == 1:
            self._story.storylist.append(eDataTable(self._data, style).table)
        elif self._style ==2:
            style = ts_left
            self._story.storylist.append(eCommonTable(self._data, style).table)
        elif self._style == 3:
            self._story.storylist.append(eConfigTable(self._data, style).table)
        elif self._style == 4:
            self._story.storylist.append(eOptionsTable(self._data, style).table)
        elif self._style == 5:
            self._story.storylist.append(eProfileTable(self._data, style).table)
        elif self._style == 6:
            self._story.storylist.append(eSummaryTable(self._data, style).table)
        elif self._style == 7:
            self._story.storylist.append(eScenarioTable(self._data, style).table)
        elif self._style == 8:
            self._story.storylist.append(eGitInfoTable(self._data, style).table)


class LinePlotStory(StoryDecorator):
    def new_story(self):
        print "LinePlot"
        style = lps_default
        if not self._data:
            print "data error "
            return
        data = eGraphicsTable([[eLinePlot(self._data, style).draw]]).table
        if data:
            self._story.storylist.append(data)


class LineChartStory(StoryDecorator):
    def new_story(self):
        print "LineChartStory: "
        style = lcs_default
        if not self._data:
            print "data error "
            return
        data = eGraphicsTable([[eHorizontalLineChart(self._data, style).draw]]).table
        if data:
            self._story.storylist.append(data)


class BarChartStory(StoryDecorator):
    def new_story(self):
        print "BarChartStory: "
        style = bcs_default
        if not self._data:
            print "data error "
            return

        data = eGraphicsTable([[eBarChartColumn(self._data, style).draw]]).table
        if data:
            self._story.storylist.append(data)


class ParagraphStory(StoryDecorator):
    def new_story(self):
        print "Paragraph Story"
        style = ps_body
        if not self._data:
            print "data error "
            return
        data = eParagraph(self._data, style).para
        if data:
            self._story.storylist.append(data)


class TitleStory(StoryDecorator):
    def new_story(self):
        print "Paragraph Story"
        if self._style - 1 in range(9):
            style = eval("ps_head_lv" + "%d" % self._style)
        else:
            style = ps_body
        # print style
        # print self._data

        self._story.storylist.append(eParagraph(self._data, style).para)
