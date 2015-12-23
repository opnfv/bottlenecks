#!/usr/bin/python
# -*- coding: utf8 -*-
from reportlab.lib.styles import PropertySet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT


class TemplateStyle(PropertySet):
    defaults = dict(
        page_height=A4[1],
        page_wight=A4[0],
        page_left=78,
        page_top=60,
        page_bottom=70,
        page_right=78,
        title_size=16,
        title_leading=1.25,
        title_font='Courier-Bold',
        body_size=10,
        body_leading=0.8,
        body_font='Courier',
        line_width=1,
        logo_width=131.2,
        logo_height=127.7
    )


class ImageStyle(PropertySet):
    defaults = dict(
        image_height=165,
        image_width=175,
        image_hAlign='CENTRE',  # LEFT,CENTRE or RIGHT
        image_vAlign='MIDDLE'  # BOTTOM,MIDDLE or TOP
    )


class TableStyle(PropertySet):
    defaults = dict(
        table_hAlign='CENTRE',  # LEFT,CENTRE or RIGHT
        table_vAlign='MIDDLE',  # BOTTOM,MIDDLE or TOP
        table_colWidths=None,
        table_rowHeights=None
    )


class LinePlotStyle(PropertySet):
    defaults = dict(
        width=430,
        height=400,
        left=30,
        bottom=20,
        strokeColor=colors.black,
        strokeWidth=1,
        format=('%4.2f', '%4.0f', '%3.1f'),
        labelsfont=7,
        linestyle=[
            (colors.red, 'Circle', 1.5),
            (colors.blue, 'Diamond', 1.5),
            (colors.gold, 'Square', 1.5),
            (colors.green, 'Triangle', 1.5),
            (colors.pink, 'FilledCircle', 1.5),
            (colors.lightblue, 'FilledDiamond', 1.5),
            (colors.lightgreen, 'FilledTriangle', 1.5)
        ]
    )


class LineChartStyle(PropertySet):
    defaults = dict(
        width=430,
        height=400,
        left=30,
        bottom=20,
        strokeColor=colors.lightgrey,
        strokeWidth=1,
        format=('%4.2f', '%3.1f'),
        labelsfont=8,
        linestyle=[
            (colors.red, 'Circle', 1.5),
            (colors.blue, 'Diamond', 1.5),
            (colors.gold, 'Square', 1.5),
            (colors.green, 'Triangle', 1.5),
            (colors.pink, 'FilledCircle', 1.5),
            (colors.lightblue, 'FilledDiamond', 1.5),
            (colors.lightgreen, 'FilledTriangle', 1.5)
        ]
    )


class BarChartStyle(PropertySet):
    defaults = dict(
        width=430,
        height=135,
        left=30,
        bottom=50,
        top=0,
        right=30,
        groupSpacing=32,
        barSpacing=4,
        tick=3,
        strokeColor=colors.lightgrey,
        strokeWidth=1,
        pillarstyle={
            "loss": (colors.lightgreen, '%4.2f'),
            "latency": (colors.indianred, '%4.1f'),
            "fastlink": (colors.pink, '%4.1f'),
            "l2switch": (colors.lightblue, '%4.1f'),
            "kernel rdp": (colors.lightgreen, '%4.1f'),
        },
        background=colors.lightgrey,
        labelsfont=6,
    )


ts_left = TableStyle(
    name='left',
    table_hAlign='LEFT',  # LEFT,CENTRE or RIGHT
    table_vAlign='BOTTOM',  # BOTTOM,MIDDLE or TOP
    table_colWidths=None,
    table_rowHeights=None
)

is_default = ImageStyle(name='default')
is_traffic = ImageStyle(name='traffic',
                        image_height=150,
                        image_width=360,
                        image_hAlign='CENTRE')

ts_default = TableStyle(name='default')
lps_default = LinePlotStyle(name='default')
lcs_default = LineChartStyle(name='default')
bcs_default = BarChartStyle(name='default')
ps_head_lv1 = ParagraphStyle(name='ps_head_lv1',
                             fontName='Courier-Bold',
                             alignment=TA_LEFT,  # TA_CENTRE,
                             fontSize=13,
                             leading=22,
                             leftIndent=0)

ps_head_lv2 = ParagraphStyle(name='ps_head_lv2',
                             fontName='Courier',
                             fontSize=12,
                             leading=20,
                             leftIndent=16)

ps_head_lv3 = ParagraphStyle(name='ps_head_lv3',
                             fontSize=11,
                             fontName='Courier',
                             leading=20,
                             leftIndent=16)

ps_head_lv4 = ParagraphStyle(name='ps_head_lv4',
                             fontSize=13,
                             fontName='Courier-Bold',
                             leading=22,
                             leftIndent=0)

ps_head_lv5 = ParagraphStyle(name='ps_head_lv5',
                             fontSize=12,
                             fontName='Courier',
                             leading=20,
                             leftIndent=16)

ps_head_lv6 = ParagraphStyle(name='ps_head_lv6',
                             fontSize=11,
                             fontName='Courier',
                             leading=20,
                             leftIndent=16)

ps_head_lv7 = ParagraphStyle(name='ps_head_lv7',
                             fontSize=11,
                             fontName='Courier',
                             leading=18,
                             leftIndent=0)

ps_head_lv8 = ParagraphStyle(name='ps_head_lv8',
                             fontSize=11,
                             fontName='Courier',
                             leading=18,
                             leftIndent=16)

ps_head_lv9 = ParagraphStyle(name='ps_head_lv9',
                             fontSize=11,
                             fontName='Courier',
                             leading=18,
                             leftIndent=32)

ps_body = ParagraphStyle(name='ps_body',
                         fontSize=11,
                         fontName='Courier',
                         leading=18,
                         leftIndent=32)

ps_space = ParagraphStyle(name='ps_space',
                          fontSize=5,
                          leading=5)
