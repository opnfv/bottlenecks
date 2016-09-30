##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


__doc__ = """
it contains the base element for pdf
eImage is used to draw picture on the pdf document
eDataTable is used to draw table on the pdf document
eGraphicsTable is used to draw plot on the pdf document
eParagraph is used to draw text on the pdf document
"""
from reportlab.platypus import Image, Table
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.platypus.paragraph import Paragraph
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics.charts.axes import XValueAxis
from reportlab.graphics.shapes import Group
from reportlab.graphics.charts.barcharts import VerticalBarChart
from vstf.controller.reporters.report.pdf.styles import *


class eImage(Image):
    """ an image(digital picture)which contains the function of auto zoom picture """

    def __init__(
            self,
            filename,
            width=None,
            height=None,
            kind='direct',
            mask="auto",
            lazy=1,
            hAlign='CENTRE',
            vAlign='BOTTOM'):
        Image.__init__(self, filename, None, None, kind, mask, lazy)
        print height, width
        print self.drawHeight, self.drawWidth
        if self.drawWidth * height > self.drawHeight * width:
            self.drawHeight = width * self.drawHeight / self.drawWidth
            self.drawWidth = width
        else:
            self.drawWidth = height * self.drawWidth / self.drawHeight
            self.drawHeight = height
        self.hAlign = hAlign
        self.vAlign = vAlign
        print self.drawHeight, self.drawWidth


class eTable(object):
    """ an abstract table class, which is contains the base functions to create table """

    def __init__(self, data, style=TableStyle(name="default")):
        self._tablestyle = style
        self._table = []
        self._spin = False
        self._colWidths = None
        self._data = self.analysisData(data)
        if self._data:
            self.create()

    def analysisData(self, data):
        raise NotImplementedError("abstract eTable")

    def create(self):
        self._table = Table(self._data, style=self._style, splitByRow=1)
        self._table.hAlign = self._tablestyle.table_hAlign
        self._table.vAlign = self._tablestyle.table_vAlign
        self._table.colWidths = self._tablestyle.table_colWidths
        if self._spin or self._colWidths:
            self._table.colWidths = self._colWidths
        self._table.rowHeights = self._tablestyle.table_rowHeights

    @property
    def table(self):
        return self._table


class eCommonTable(eTable):

    def analysisData(self, data):
        self._style = [
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BOX', (0, 0), (-1, -1), 1.2, colors.black)
        ]
        return data


class eConfigTable(eTable):

    def analysisData(self, data):
        self._style = [
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('SPAN', (2, 0), (3, 0)),
            ('SPAN', (2, 1), (3, 1)),
            ('SPAN', (2, 8), (3, 8)),
            ('SPAN', (2, 9), (3, 9)),
            ('SPAN', (2, 10), (3, 10)),
            ('SPAN', (0, 0), (0, 7)),
            ('SPAN', (0, 8), (0, 10)),
            ('SPAN', (0, 11), (0, 19)),
            ('SPAN', (1, 2), (1, 6)),
            ('SPAN', (1, 12), (1, 13)),
            ('SPAN', (1, 14), (1, 16)),
            ('SPAN', (1, 17), (1, 19)),
            ('SPAN', (2, 3), (2, 6))
        ]
        return data


class eSummaryTable(eTable):

    def analysisData(self, data):
        self._style = [
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('SPAN', (0, 0), (0, 1)),
            ('SPAN', (1, 0), (4, 0)),
            ('SPAN', (5, 0), (-1, 0))
        ]
        return data


class eGitInfoTable(eTable):

    def analysisData(self, data):
        self._style = [
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('SPAN', (0, 0), (0, 2)),
            ('SPAN', (0, 3), (0, 5)),
            ('SPAN', (0, 6), (0, 8))
        ]
        return data


class eScenarioTable(eTable):

    def analysisData(self, data):
        self._style = [
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (2, 1), (-1, -1), 'LEFT'),
            ('SPAN', (0, 1), (0, 6)),
            ('SPAN', (0, 7), (0, 12)),
            ('SPAN', (0, 13), (0, 16)),
            ('SPAN', (0, 17), (0, 20))
        ]
        return data


class eOptionsTable(eTable):

    def analysisData(self, data):
        self._style = [
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('SPAN', (2, 0), (4, 0)),
            ('SPAN', (2, 1), (4, 1)),
            ('SPAN', (0, 0), (0, -1)),
            ('SPAN', (1, 2), (1, 16)),
            ('SPAN', (1, 17), (1, 19)),
            ('SPAN', (1, 20), (1, 22)),
            ('SPAN', (1, 23), (1, 24)),
            ('SPAN', (2, 2), (2, 4)),
            ('SPAN', (2, 5), (2, 12)),
            ('SPAN', (2, 13), (2, 16)),
            ('SPAN', (2, 17), (2, 19)),
            ('SPAN', (2, 20), (2, 22)),
            ('SPAN', (2, 23), (2, 24))
        ]
        return data


class eProfileTable(eTable):

    def analysisData(self, data):
        self._style = [
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('SPAN', (0, 1), (0, -1)),
            ('SPAN', (1, 0), (2, 0)),
        ]
        return data


class eDataTable(eTable):

    def analysisData(self, data):
        result = data
        self._style = [
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEADING', (0, 0), (-1, -1), 18),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('LINEBEFORE', (1, 0), (1, -1), 0.8, colors.black),
            # ('LINEBEFORE', (3, 0), (3, -1), 1, colors.black),
            # ('LINEBEFORE', (5, 0), (5, -1), 1, colors.black),
            ('LINEBELOW', (0, 0), (-1, 0), 0.8, colors.black),
            # ('SPAN', (0, 0), (0, 1)),
            # ('SPAN', (1, 0), (2, 0)),
            # ('SPAN', (3, 0), (4, 0))
        ]
        if self._spin is True:
            print "start spin"
            result = map(list, zip(*result))
            style = []
            for value in self._style:
                value = list(value)
                value[1] = (value[1][1], value[1][0])
                value[2] = (value[2][1], value[2][0])
                if value[0] == 'LINEBELOW':
                    value[0] = 'LINEAFTER'
                elif value[0] == 'LINEBEFORE':
                    value[0] = 'LINEABOVE'
                value = tuple(value)
                style.append(value)
            self._style = style
        return result


class eGraphicsTable(eTable):

    def analysisData(self, data):
        self._style = [
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]
        return data


class noScaleXValueAxis(XValueAxis):

    def __init__(self):
        XValueAxis.__init__(self)

    def makeTickLabels(self):
        g = Group()
        if not self.visibleLabels:
            return g

        f = self._labelTextFormat  # perhaps someone already set it
        if f is None:
            f = self.labelTextFormat or (self._allIntTicks() and '%.0f' or str)
        elif f is str and self._allIntTicks():
            f = '%.0f'
        elif hasattr(f, 'calcPlaces'):
            f.calcPlaces(self._tickValues)
        post = self.labelTextPostFormat
        scl = self.labelTextScale
        pos = [self._x, self._y]
        d = self._dataIndex
        pos[1 - d] = self._labelAxisPos()
        labels = self.labels
        if self.skipEndL != 'none':
            if self.isXAxis:
                sk = self._x
            else:
                sk = self._y
            if self.skipEndL == 'start':
                sk = [sk]
            else:
                sk = [sk, sk + self._length]
                if self.skipEndL == 'end':
                    del sk[0]
        else:
            sk = []

        nticks = len(self._tickValues)
        nticks1 = nticks - 1
        for i, tick in enumerate(self._tickValues):
            label = i - nticks
            if label in labels:
                label = labels[label]
            else:
                label = labels[i]
            if f and label.visible:
                v = self.scale(i)
                if sk:
                    for skv in sk:
                        if abs(skv - v) < 1e-6:
                            v = None
                            break
                if v is not None:
                    if scl is not None:
                        t = tick * scl
                    else:
                        t = tick
                    if isinstance(f, str):
                        txt = f % t
                    elif isSeq(f):
                        # it's a list, use as many items as we get
                        if i < len(f):
                            txt = f[i]
                        else:
                            txt = ''
                    elif hasattr(f, '__call__'):
                        if isinstance(f, TickLabeller):
                            txt = f(self, t)
                        else:
                            txt = f(t)
                    else:
                        raise ValueError('Invalid labelTextFormat %s' % f)
                    if post:
                        txt = post % txt
                    pos[d] = v
                    label.setOrigin(*pos)
                    label.setText(txt)

                    # special property to ensure a label doesn't project beyond
                    # the bounds of an x-axis
                    if self.keepTickLabelsInside:
                        if isinstance(
                                self, XValueAxis):  # not done yet for y axes
                            a_x = self._x
                            if not i:  # first one
                                x0, y0, x1, y1 = label.getBounds()
                                if x0 < a_x:
                                    label = label.clone(dx=label.dx + a_x - x0)
                            if i == nticks1:  # final one
                                a_x1 = a_x + self._length
                                x0, y0, x1, y1 = label.getBounds()
                                if x1 > a_x1:
                                    label = label.clone(
                                        dx=label.dx - x1 + a_x1)
                    g.add(label)

        return g

    def ___calcScaleFactor(self):
        """Calculate the axis' scale factor.
        This should be called only *after* the axis' range is set.
        Returns a number.
        """
        self._scaleFactor = self._length / (len(self._tickValues) + 1)
        return self._scaleFactor

    def scale(self, value):
        """Converts a numeric value to a plotarea position.
        The chart first configures the axis, then asks it to
        """
        assert self._configured, "Axis cannot scale numbers before it is configured"
        if value is None:
            value = 0
        # this could be made more efficient by moving the definition of org and
        # sf into the configuration
        org = (self._x, self._y)[self._dataIndex]
        sf = self._length / (len(self._tickValues) + 1)
        if self.reverseDirection:
            sf = -sf
            org += self._length
        return org + sf * (value + 1)


class noScaleLinePlot(LinePlot):

    def __init__(self):
        LinePlot.__init__(self)
        self.xValueAxis = noScaleXValueAxis()

    def calcPositions(self):
        """Works out where they go.

        Sets an attribute _positions which is a list of
        lists of (x, y) matching the data.
        """
        self._seriesCount = len(self.data)
        self._rowLength = max(map(len, self.data))

        self._positions = []
        for rowNo in range(len(self.data)):
            line = []
            len_row = len(self.data[rowNo])
            for colNo in range(len_row):
                datum = self.data[rowNo][colNo]  # x, y value
                x = self.x + self.width / (len_row + 1) * (colNo + 1)
                self.xValueAxis.labels[colNo].x = self.x + \
                    self.width / (len_row + 1) * (colNo + 1)
                y = self.yValueAxis.scale(datum[1])
                #               print self.width, " ", x
                line.append((x, y))
            self._positions.append(line)


# def _innerDrawLabel(self, rowNo, colNo, x, y):
#        return None
class eLinePlot(object):

    def __init__(self, data, style):
        self._lpstyle = style
        self._linename = data[0]
        self._data = self.analysisData(data[1:])
        if self._data:
            self.create()

    @property
    def draw(self):
        return self._draw

    def analysisData(self, data):
        columns = len(data)
        # print data
        data = map(list, zip(*data))
        rows = len(data)

        for i in range(rows):
            for j in range(columns):
                data[i][j] = float(data[i][j])
        self._linename = self._linename[1:]
        """
        delcnt = 0
        delrows = []
        for i in range(columns):
            delrows.append(0.0)
        del_line = [self._linename[0]]
        for i in range(rows):
           for j in range(columns):
              data[i][j] = float(data[i][j])
           if data[i] == delrows:
               delcnt += 1
               del_line.append(self._linename[i])
        for i in range(delcnt):
            data.remove(delrows)
        for name in del_line:
            self._linename.remove(name)

        rows = len(data)
        """
        # print rows
        # print data
        xvalueSteps = data[0]
        xvalueMin = data[0][0]
        xvalueMax = data[0][0]
        yvalueMin = data[1][0]
        yvalueMax = data[1][0]
        yvalueSteps = []
        result = []
        for j in range(columns):
            if xvalueMin > data[0][j]:
                xvalueMin = data[0][j]
            if xvalueMax < data[0][j]:
                xvalueMax = data[0][j]

        for i in range(rows - 1):
            lst = []
            for j in range(columns):
                lst.append((data[0][j], data[i + 1][j]))
                if yvalueMin > data[i + 1][j]:
                    yvalueMin = data[i + 1][j]
                if yvalueMax < data[i + 1][j]:
                    yvalueMax = data[i + 1][j]
                yvalueSteps.append(int(data[i + 1][j] * 2.5) / 2.5)
            result.append(tuple(lst))
        xvalueMin = int(xvalueMin) / 100 * 100
        xvalueMax = int(xvalueMax) / 100 * 100 + 200
        yvalueMin = int(yvalueMin) * 1.0 - 1
        if yvalueMin < 0:
            yvalueMin = 0.0
        yvalueMax = int(yvalueMax) + 2.0
        yvalueSteps.append(yvalueMin)
        yvalueSteps.append(yvalueMax)
        yvalueSteps = {}.fromkeys(yvalueSteps).keys()

        self._xvalue = (xvalueMin, xvalueMax, xvalueSteps)
        self._yvalue = (yvalueMin, yvalueMax, yvalueSteps)
        print result
        return result

    def create(self):
        lpw = self._lpstyle.width
        lph = self._lpstyle.height
        draw = Drawing(lpw, lph)
        line_cnts = len(self._linename)
        #        lp = noScaleLinePlot()
        lp = LinePlot()
        lg_line = (line_cnts + 3) / 4
        lp.x = self._lpstyle.left
        lp.y = self._lpstyle.bottom

        lp.height = lph - self._lpstyle.bottom * (lg_line + 1.5)
        lp.width = lpw - lp.x * 2
        lp.data = self._data
        lp.joinedLines = 1
        lp.strokeWidth = self._lpstyle.strokeWidth
        line_cnts = len(self._data)
        sytle_cnts = len(self._lpstyle.linestyle)
        color_paris = []
        for i in range(line_cnts):
            styleIndex = i % sytle_cnts
            lp.lines[i].strokeColor = self._lpstyle.linestyle[styleIndex][0]
            lp.lines[i].symbol = makeMarker(
                self._lpstyle.linestyle[styleIndex][1])
            lp.lines[i].strokeWidth = self._lpstyle.linestyle[styleIndex][2]
            color_paris.append(
                (self._lpstyle.linestyle[styleIndex][0], self._linename[i]))
        #            lp.lineLabels[i].strokeColor = self._lpstyle.linestyle[styleIndex][0]

        lp.lineLabelFormat = self._lpstyle.format[0]

        lp.strokeColor = self._lpstyle.strokeColor

        lp.xValueAxis.valueMin, lp.xValueAxis.valueMax, lp.xValueAxis.valueSteps = self._xvalue
        #       valueMin, valueMax, xvalueSteps = self._xvalue
        #       lp.xValueAxis.valueStep = (lp.xValueAxis.valueMax - lp.xValueAxis.valueMin)/len(xvalueSteps)
        #       lp.xValueAxis.valueSteps = map(lambda x: str(x), xvalueSteps)

        lp.yValueAxis.valueMin, lp.yValueAxis.valueMax, lp.yValueAxis.valueSteps = self._yvalue

        #       lp.xValueAxis.forceZero = 0
        #       lp.xValueAxis.avoidBoundFrac = 1
        #       lp.xValueAxis.tickDown = 3
        #       lp.xValueAxis.visibleGrid = 1
        #       lp.xValueAxis.categoryNames = '64 256 512 1400 1500 4096'.split(' ')

        lp.xValueAxis.labelTextFormat = self._lpstyle.format[1]
        lp.yValueAxis.labelTextFormat = self._lpstyle.format[2]

        delsize = int(lp.xValueAxis.valueMax / 2000)
        lp.xValueAxis.labels.fontSize = self._lpstyle.labelsfont
        lp.xValueAxis.labels.angle = 25

        lp.yValueAxis.labels.fontSize = self._lpstyle.labelsfont
        lp.lineLabels.fontSize = self._lpstyle.labelsfont - delsize
        draw.add(lp)

        lg = Legend()
        lg.colorNamePairs = color_paris
        lg.fontName = 'Helvetica'
        lg.fontSize = 7

        lg.x = self._lpstyle.left * 3
        lg.y = self._lpstyle.bottom * (1 + lg_line) + lp.height

        lg.dxTextSpace = 5
        lg.dy = 5
        lg.dx = 20
        lg.deltax = 60
        lg.deltay = 0
        lg.columnMaximum = 1
        lg.alignment = 'right'
        draw.add(lg)
        self._draw = draw


class eHorizontalLineChart(object):

    def __init__(self, data, style):
        self._lcstyle = style
        if len(data) < 1:
            return
        self._linename = data[0]
        self._data = self.analysisData(data[1:])
        if self._data:
            self.create()

    @property
    def draw(self):
        return self._draw

    def analysisData(self, data):
        columns = len(data)
        data = map(list, zip(*data))
        self._catNames = data[0]
        self._linename = self._linename[1:]
        data = data[1:]
        rows = len(data)

        yvalueMin = float(data[0][0])
        yvalueMax = float(data[0][0])
        yvalueSteps = []
        result = []

        for rowNo in range(rows):
            for columnNo in range(columns):
                data[rowNo][columnNo] = float(data[rowNo][columnNo])
                if yvalueMin > data[rowNo][columnNo]:
                    yvalueMin = data[rowNo][columnNo]
                if yvalueMax < data[rowNo][columnNo]:
                    yvalueMax = data[rowNo][columnNo]
                yvalueSteps.append(int(data[rowNo][columnNo] * 1.0) / 1.0)
            result.append(tuple(data[rowNo]))

        yvalueMin = int(yvalueMin) * 1.0 - 1
        if yvalueMin < 0:
            yvalueMin = 0.0
        yvalueMax = int(yvalueMax) + 2.0
        yvalueSteps.append(yvalueMin)
        yvalueSteps.append(yvalueMax)
        yvalueSteps = {}.fromkeys(yvalueSteps).keys()

        self._value = (yvalueMin, yvalueMax, yvalueSteps)
        print result
        return result

    def create(self):
        dw = self._lcstyle.width
        dh = self._lcstyle.height
        draw = Drawing(dw, dh)

        lc = HorizontalLineChart()
        line_cnts = len(self._linename)

        lg_line = (line_cnts + 3) / 4
        lc.height = dh - self._lcstyle.bottom * (lg_line + 1.5)
        lc.width = dw - lc.x * 2
        lc.x = self._lcstyle.left
        lc.y = self._lcstyle.bottom

        lc.data = self._data

        lc.strokeColor = self._lcstyle.strokeColor
        lc.strokeWidth = self._lcstyle.strokeWidth
        lc.useAbsolute = 1
        lc.groupSpacing = lc.width * 2.0 / len(self._catNames)
        lc.joinedLines = 1
        lc.lineLabelFormat = self._lcstyle.format[0]

        lc.valueAxis.valueMin, lc.valueAxis.valueMax, lc.valueAxis.valueSteps = self._value
        lc.valueAxis.labelTextFormat = self._lcstyle.format[1]
        lc.valueAxis.labels.fontSize = self._lcstyle.labelsfont

        lc.categoryAxis.categoryNames = self._catNames
        lc.categoryAxis.labels.boxAnchor = 'ne'
        lc.categoryAxis.labels.dx = lc.width / 2.0 / len(self._catNames)
        lc.categoryAxis.labels.dy = -6
        lc.categoryAxis.labels.angle = 10
        lc.categoryAxis.labels.fontSize = self._lcstyle.labelsfont
        #        lc.categoryAxis.visibleGrid = 1
        #        lc.categoryAxis.tickUp = 100
        #        lc.categoryAxis.tickDown = 50
        #        lc.categoryAxis.gridEnd = dh
        sytle_cnts = len(self._lcstyle.linestyle)
        color_paris = []
        for i in range(line_cnts):
            styleIndex = i % sytle_cnts
            lc.lines[i].strokeColor = self._lcstyle.linestyle[styleIndex][0]
            lc.lines[i].symbol = makeMarker(
                self._lcstyle.linestyle[styleIndex][1])
            lc.lines[i].strokeWidth = self._lcstyle.linestyle[styleIndex][2]
            color_paris.append(
                (self._lcstyle.linestyle[styleIndex][0], self._linename[i]))

        lc.lineLabels.fontSize = self._lcstyle.labelsfont - 2

        draw.add(lc)

        lg = Legend()
        lg.colorNamePairs = color_paris
        lg.fontName = 'Helvetica'
        lg.fontSize = 7
        #        lg.x = dw /2
        #        lg.y = self._lcstyle.bottom *(1.5 + lg_line)

        lg.x = self._lcstyle.left * 3
        lg.y = self._lcstyle.bottom * (1 + lg_line) + lc.height

        lg.dxTextSpace = 5
        lg.dy = 5
        lg.dx = 20
        lg.deltax = 60
        lg.deltay = 0
        lg.columnMaximum = 1
        lg.alignment = 'right'
        draw.add(lg)
        self._draw = draw


class eBarChartColumn(object):

    def __init__(self, data, style):
        self._bcstyle = style
        if len(data) < 4:
            return
        self._data = self.analysisData(data)
        if self._data:
            self.create()

    @property
    def draw(self):
        return self._draw

    def analysisData(self, data):
        self._ytitle = data[0]
        self._name = data[1]
        self._bar = data[2]
        bar_data = data[3]
        result = []
        for bar in bar_data:
            bar = map(lambda x: float(x), bar)
            result.append(tuple(bar))
        return result

    def create(self):
        dw = self._bcstyle.width
        dh = self._bcstyle.height
        draw = Drawing(dw, dh)

        bc = VerticalBarChart()
        bar_cnt = len(self._bar)
        lg_line = (bar_cnt + 3) / 4

        bc.width = dw - self._bcstyle.left - self._bcstyle.right
        bc.height = dh - self._bcstyle.top - self._bcstyle.bottom
        if bar_cnt > 1:
            bc.height -= lg_line * 15

        bc.x = self._bcstyle.left
        bc.y = self._bcstyle.bottom
        color_paris = []
        for i in range(bar_cnt):
            bc.bars[i].fillColor = self._bcstyle.pillarstyle[self._bar[i]][0]
            color_paris.append(
                (self._bcstyle.pillarstyle[
                    self._bar[i]][0],
                    self._bar[i]))

        bc.fillColor = self._bcstyle.background
        bc.barLabels.fontName = 'Helvetica'
        bc.barLabelFormat = self._bcstyle.pillarstyle[self._bar[0]][1]
        bc.barLabels.fontSize = self._bcstyle.labelsfont
        bc.barLabels.dy = self._bcstyle.labelsfont
        bc.valueAxis.labels.fontName = 'Helvetica'
        bc.valueAxis.labels.fontSize = self._bcstyle.labelsfont
        bc.valueAxis.forceZero = 1
        bc.valueAxis.valueMin = 0

        bc.data = self._data
        bc.barSpacing = self._bcstyle.barSpacing
        bc.groupSpacing = self._bcstyle.groupSpacing / bar_cnt
        bc.valueAxis.avoidBoundFrac = 1
        bc.valueAxis.gridEnd = dw - self._bcstyle.right
        bc.valueAxis.tickLeft = self._bcstyle.tick
        bc.valueAxis.visibleGrid = 1
        bc.categoryAxis.categoryNames = self._name
        bc.categoryAxis.tickDown = self._bcstyle.tick
        bc.categoryAxis.labels.fontName = 'Helvetica'
        bc.categoryAxis.labels.fontSize = self._bcstyle.labelsfont
        bc.categoryAxis.labels.dy = -27
        bc.categoryAxis.labels.angle = -90
        draw.add(bc)
        lb = Label()
        lb.fontName = 'Helvetica'
        lb.fontSize = 7
        lb.x = 12
        lb.y = 80
        lb.angle = 90
        lb.textAnchor = 'middle'
        lb.maxWidth = 100
        lb.height = 20
        lb._text = self._ytitle
        draw.add(lb)
        if bar_cnt > 1:
            lg = Legend()
            lg.colorNamePairs = color_paris
            lg.fontName = 'Helvetica'
            lg.fontSize = 7

            lg.x = self._bcstyle.left + bc.width / (bar_cnt + 1)
            lg.y = dh - self._bcstyle.top - lg_line * 5

            lg.dxTextSpace = 5
            lg.dy = 5
            lg.dx = 25
            lg.deltax = 80
            lg.deltay = 0
            lg.columnMaximum = 1
            lg.alignment = 'right'
            draw.add(lg)

        self._draw = draw


class eParagraph(object):

    def __init__(self, data, style):
        self._pstyle = style
        self._data = self.analysisData(data)
        self.create()

    def analysisData(self, data):
        result = ""
        for dstr in data:
            if self._pstyle.name == 'ps_body':
                #               dstr = "<i>" + dstr + "</i><br/>"
                dstr = dstr + "<br/>"
            else:
                dstr = dstr + "<br/>"
            result += dstr
        return result

    def create(self):
        self._para = Paragraph(self._data, self._pstyle)

    @property
    def para(self):
        return self._para
