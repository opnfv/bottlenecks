##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


from sys import stdout, modules

doc_type = '<!DOCTYPE HTML>\n'
default_title = "Html Page"
charset = '<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />\n'

html4_tags = {
    'a',
    'abbr',
    'acronym',
    'address',
    'area',
    'b',
    'base',
    'bdo',
    'big',
    'blockquote',
    'body',
    'br',
    'button',
    'caption',
    'cite',
    'code',
    'col',
    'colgroup',
    'dd',
    'del',
    'div',
    'dfn',
    'dl',
    'dt',
    'em',
    'fieldset',
    'form',
    'frame',
    'frameset',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'head',
    'hr',
    'html',
    'i',
    'iframe',
    'img',
    'input',
    'ins',
    'kbd',
    'label',
    'legend',
    'li',
    'link',
    'map',
    'menu',
    'menuitem',
    'meta',
    'noframes',
    'noscript',
    'object',
    'ol',
    'optgroup',
    'option',
    'p',
    'param',
    'pre',
    'q',
    'samp',
    'script',
    'select',
    'small',
    'span',
    'strong',
    'style',
    'sub',
    'sup',
    'table',
    'tbody',
    'td',
    'textarea',
    'tfoot',
    'th',
    'thead',
    'title',
    'tr',
    'tt',
    'ul',
    'var'}
disused_tags = {'isindex', 'font', 'dir', 's', 'strike',
                'u', 'center', 'basefont', 'applet', 'xmp'}
html5_tags = {
    'article',
    'aside',
    'audio',
    'bdi',
    'canvas',
    'command',
    'datalist',
    'details',
    'dialog',
    'embed',
    'figcaption',
    'figure',
    'footer',
    'header',
    'keygen',
    'mark',
    'meter',
    'nav',
    'output',
    'progress',
    'rp',
    'rt',
    'ruby',
    'section',
    'source',
    'summary',
    'details',
    'time',
    'track',
    'video',
    'wbr'}

nl = '\n'
tags = html4_tags | disused_tags | html5_tags

__all__ = [x.title() for x in tags] + ['PyHtml', 'space']

self_close = {'input', 'img', 'link', 'br'}


def space(n):
    return ' ' * n


class Tag(list):
    tag_name = ''

    def __init__(self, *args, **kwargs):
        self.attributes = kwargs
        if self.tag_name:
            name = self.tag_name
            self.is_seq = False
        else:
            name = 'sequence'
            self.is_seq = True
        self._id = kwargs.get('id', name)
        for arg in args:
            self.add_obj(arg)

    def __iadd__(self, obj):
        if isinstance(obj, Tag) and obj.is_seq:
            for o in obj:
                self.add_obj(o)
        else:
            self.add_obj(obj)
        return self

    def add_obj(self, obj):
        if not isinstance(obj, Tag):
            obj = str(obj)
        _id = self.set_id(obj)
        setattr(self, _id, obj)
        self.append(obj)

    def set_id(self, obj):
        if isinstance(obj, Tag):
            _id = obj._id
            obj_lst = filter(lambda t: isinstance(
                t, Tag) and t._id.startswith(_id), self)
        else:
            _id = 'content'
            obj_lst = filter(lambda t: not isinstance(t, Tag), self)
        length = len(obj_lst)
        if obj_lst:
            _id = '%s_%03i' % (_id, length)
        if isinstance(obj, Tag):
            obj._id = _id
        return _id

    def __add__(self, obj):
        if self.tag_name:
            return Tag(self, obj)
        self.add_obj(obj)
        return self

    def __lshift__(self, obj):
        if isinstance(obj, Tag):
            self += obj
            return obj
        print "unknown obj: %s " % obj
        return self

    def render(self):
        result = ''
        if self.tag_name:
            result += '<%s%s%s>' % (self.tag_name,
                                    self._render_attr(),
                                    self._self_close() * ' /')
        if not self._self_close():
            isnl = True
            for c in self:
                if isinstance(c, Tag):
                    result += isnl * nl
                    isnl = False
                    result += c.render()
                else:
                    result += c
            if self.tag_name:
                result += '</%s>' % self.tag_name
        result += nl
        return result

    def _render_attr(self):
        result = ''
        for key, value in self.attributes.iteritems():
            if key != 'txt' and key != 'open':
                if key == 'cl':
                    key = 'class'
                result += ' %s="%s"' % (key, value)
        return result

    def _self_close(self):
        return self.tag_name in self_close

"""
def tag_factory(tag):
    class F(Tag):
        tag_name = tag

    F.__name__ = tag.title()
    return F


THIS = modules[__name__]

for t in tags:
    setattr(THIS, t.title(), tag_factory(t))
"""
THIS = modules[__name__]
for t in tags:
    obj = type(t.title(), (Tag, ), {'tag_name': t})
    setattr(THIS, t.title(), obj)


def _render_style(style):
    result = ''
    for item in style:
        result += item
        result += '\n{\n'
        values = style[item]
        for key, value in values.iteritems():
            result += "    %s: %s;\n" % (key, value)
        result += '}\n'
    if result:
        result = '\n' + result
    return result


class PyHtml(Tag):
    tag_name = 'html'

    def __init__(self, title=default_title):
        self._id = 'html'
        self += Head()
        self += Body()
        self.attributes = dict(xmlns='http://www.w3.org/1999/xhtml', lang='en')
        self.head += Title(title)

    def __iadd__(self, obj):
        if isinstance(obj, Head) or isinstance(obj, Body):
            self.add_obj(obj)
        elif isinstance(obj, Meta) or isinstance(obj, Link):
            self.head += obj
        else:
            self.body += obj
            _id = self.set_id(obj)
            setattr(self, _id, obj)
        return self

    def add_js(self, *arg):
        for f in arg:
            self.head += Script(type='text/javascript', src=f)

    def add_css(self, *arg):
        for f in arg:
            self.head += Link(rel='stylesheet', type='text/css', href=f)

    def output(self, name=''):
        if name:
            fil = open(name, 'w')
        else:
            fil = stdout
        fil.write(self.as_string())
        fil.flush()
        if name:
            fil.close()

    def as_string(self):
        return doc_type + self.render()

    def add_style(self, style):
        self.head += Style(_render_style(style))

    def add_table(self, data):
        table = self << Table()
        rows = len(data)
        cols = len(zip(*data))

        for i in range(rows):
            tr = table << Tr()
            tr << Th(data[i][0])
            for j in range(1, cols):
                tr << Td(data[i][j])
