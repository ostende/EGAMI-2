# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/TemplatedMultiContent.py
# Compiled at: 2017-10-02 01:52:07
from Components.Converter.StringList import StringList

class TemplatedMultiContent(StringList):

    def __init__(self, args):
        StringList.__init__(self, args)
        from enigma import eListboxPythonMultiContentgFontRT_HALIGN_LEFTRT_HALIGN_CENTERRT_HALIGN_RIGHTRT_VALIGN_TOPRT_VALIGN_CENTERRT_VALIGN_BOTTOMRT_WRAPBT_SCALE
        from Components.MultiContent import MultiContentEntryTextMultiContentEntryPixmapMultiContentEntryPixmapAlphaTestMultiContentEntryPixmapAlphaBlendMultiContentTemplateColorMultiContentEntryProgress
        l = locals()
        del l['self']
        del l['args']
        self.active_style = None
        self.template = eval(args, {}, l)
        if 'template' not in self.template:
            self.template['template'] = self.template['templates']['default'][1]
            self.template['itemHeight'] = self.template['template'][0]
        return

    def changed(self, what):
        if not self.content:
            from enigma import eListboxPythonMultiContent
            self.content = eListboxPythonMultiContent()
            index = 0
            for f in self.template['fonts']:
                self.content.setFont(index, f)
                index += 1

        if what[0] == self.CHANGED_SPECIFIC and what[1] == 'style':
            pass
        elif self.source:
            try:
                tmp = []
                src = self.source.list
                for x in range(len(src)):
                    if type(src[x]) != tuple and type(src[x]) != list:
                        tmp.append((src[x],))
                    else:
                        tmp.append(src[x])

            except Exception as error:
                print '[TemplatedMultiContent] - %s' % error
                tmp = self.source.list

            self.content.setList(tmp)
        self.setTemplate()
        self.downstream_elements.changed(what)

    def setTemplate(self):
        if self.source:
            style = self.source.style
            if style == self.active_style:
                return
            templates = self.template.get('templates')
            template = self.template.get('template')
            itemheight = self.template['itemHeight']
            selectionEnabled = self.template.get('selectionEnabled', True)
            scrollbarMode = self.template.get('scrollbarMode', 'showOnDemand')
            if templates and style and style in templates:
                template = templates[style][1]
                itemheight = templates[style][0]
                if len(templates[style]) > 2:
                    selectionEnabled = templates[style][2]
                if len(templates[style]) > 3:
                    scrollbarMode = templates[style][3]
            self.content.setTemplate(template)
            self.content.setItemHeight(itemheight)
            self.selectionEnabled = selectionEnabled
            self.scrollbarMode = scrollbarMode
            self.active_style = style