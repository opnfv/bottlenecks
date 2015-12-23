#!/usr/bin/python
# -*- coding: utf8 -*-
import time

from reportlab.platypus.doctemplate import SimpleDocTemplate
from reportlab.platypus import PageBreak
from vstf.controller.reporters.report.pdf.styles import TemplateStyle, ps_head_lv1, ps_head_lv2, ps_head_lv3


class MyDocTemplate(SimpleDocTemplate):
    def __init__(self, filename, **kw):
        self.allowSplitting = 0
        SimpleDocTemplate.__init__(self, filename, **kw)

    def afterFlowable(self, flowable):
        """Registers TOC entries."""
        if flowable.__class__.__name__ == 'Paragraph':
            text = flowable.getPlainText()
            style = flowable.style.name
            if style == ps_head_lv1.name:
                self.notify('TOCEntry', (0, text, self.page - 1))
            elif style == ps_head_lv2.name:
                self.notify('TOCEntry', (1, text, self.page - 1))
            elif style == ps_head_lv3.name:
                self.notify('TOCEntry', (2, text, self.page - 1))


class PdfTemplate:
    def __init__(self, style, title, logo, header, footer, output, note=None):
        self._style = style
        self._title = title
        self._logo = logo[0]
        self._header = header[0]
        self._footer = footer
        self._output = output[0]
        self._note = note
        info = " Generated on %s " % time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())
        self._note[0] += info

    def myFirstPage(self, canvas, doc):
        raise NotImplementedError("abstract StoryDecorator")

    def myLaterPages(self, canvas, doc):
        raise NotImplementedError("abstract StoryDecorator")

    def generate(self, story):
        sizes = (self._style.page_wight, self._style.page_height)
        doc = MyDocTemplate(self._output, pagesize=sizes)
        #    doc.build(story, onFirstPage=self.myFirstPage, onLaterPages=self.myLaterPages)
        doc.multiBuild(story, onFirstPage=self.myFirstPage, onLaterPages=self.myLaterPages)


class PdfVswitch(PdfTemplate):
    def myFirstPage(self, canvas, doc):
        canvas.saveState()
        title_lines = len(self._title)
        line_size = [self._style.title_size] * title_lines
        line_size.append(0)

        canvas.drawImage(self._logo,
                         (self._style.page_wight - self._style.logo_width) / 2.0,
                         self._style.page_height / 2.0 + (1 + self._style.title_leading) * reduce(lambda x, y: x + y,
                                                                                                  line_size),
                         self._style.logo_width,
                         self._style.logo_height
                         )
        for i in range(title_lines):
            canvas.setFont(self._style.title_font, line_size[i])
            canvas.drawCentredString(self._style.page_wight / 2.0,
                                     self._style.page_height / 2.0 + (1 + self._style.title_leading) * reduce(
                                         lambda x, y: x + y, line_size[i + 1:]),
                                     self._title[i]
                                     )
        size = self._style.body_size
        canvas.setFont(self._style.body_font, size)
        note_line = len(self._note)

        for i in range(note_line):
            print self._note[i]
            canvas.drawCentredString(self._style.page_wight / 2.0,
                                     self._style.page_height / 5.0 + (1 + self._style.body_leading) * size * (
                                     note_line - i - 1),
                                     self._note[i]
                                     )
        size = self._style.body_size - 2
        canvas.setFont(self._style.body_font, size)
        canvas.drawCentredString(self._style.page_wight / 2.0,
                                 self._style.page_bottom / 2.0 + (1 + self._style.body_leading) * size,
                                 self._footer[0])
        canvas.restoreState()

    def myLaterPages(self, canvas, doc):
        canvas.saveState()
        canvas.setLineWidth(self._style.line_width)
        canvas.line(self._style.page_left,
                    self._style.page_height - self._style.page_top,
                    self._style.page_wight - self._style.page_right,
                    self._style.page_height - self._style.page_top
                    )
        size = self._style.body_size - 2
        canvas.setFont(self._style.body_font, size)
        canvas.drawCentredString(self._style.page_wight / 2.0,
                                 self._style.page_bottom - 24,
                                 "%s%s Page %2d " % (self._footer[0], " " * 8, doc.page - 1)
                                 )
        canvas.restoreState()

