# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Renderer/RollerLabel.py
# Compiled at: 2017-10-02 01:52:08
import skin
from Renderer import Renderer
from enigma import eLabel
from enigma import eTimer
from Components.VariableText import VariableText

class RollerLabel(VariableText, Renderer):

    def __init__(self):
        Renderer.__init__(self)
        VariableText.__init__(self)
        self.steptime = 250
        self.startdelay = 8500
        self.rollTimerText = eTimer()
        self.rollTimerText.timeout.get().append(self.rollText)

    def checkSingleAttribute(self, skinAttributes):
        attribs = []
        for attrib, value in skinAttributes:
            if attrib.find('steptime') != -1:
                self.steptime = int(value)
            elif attrib.find('startdelay') != -1:
                self.startdelay = int(value)
            elif attrib == 'css':
                from skin import cascadingStyleSheets
                styles = value.split(',')
                for style in styles:
                    for _attrib in cascadingStyleSheets[style].keys():
                        _value = cascadingStyleSheets[style][_attrib]
                        attribs = attribs + self.checkSingleAttribute([(_attrib, _value)])

            else:
                attribs.append((attrib, value))

        return attribs

    def applySkin(self, desktop, parent):
        if self.skinAttributes is not None:
            self.skinAttributes = self.checkSingleAttribute(self.skinAttributes)
        ret = Renderer.applySkin(self, desktop, parent)
        self.changed((self.CHANGED_DEFAULT,))
        return ret

    GUI_WIDGET = eLabel

    def connect(self, source):
        Renderer.connect(self, source)
        self.changed((self.CHANGED_DEFAULT,))

    def changed(self, what):
        if self.rollTimerText.isActive():
            self.rollTimerText.stop()
        if what[0] == self.CHANGED_CLEAR:
            self.text = ''
        else:
            self.text = self.source.text
        if self.text is None:
            self.text = ''
        text_list = self.text.split('\n')
        if len(text_list) > 0:
            self.text = text_list[0]
        if self.instance:
            self.idx = 0
            try:
                self.backtext = unicode(self.text, 'utf-8')
            except:
                self.backtext = self.text

            if len(self.backtext) > 16:
                try:
                    self.backtext = unicode('               ' + self.text + '               ', 'utf-8')
                except:
                    self.backtext = '               ' + self.text + '               '

                self.x = len(self.backtext)
                self.rollTimerText.start(self.startdelay)
            else:
                x = (16 - len(self.backtext)) / 2
                self.backtext = ' ' * x + self.backtext + ' ' * x
                try:
                    self.text = str(self.backtext.encode('utf-8'))
                except:
                    self.text = str(self.backtext)

        return

    def rollText(self):
        self.rollTimerText.stop()
        if self.x > 0:
            txttmp = self.backtext[self.idx:]
            x = len(txttmp)
            try:
                self.text = str(txttmp[:x].encode('utf-8'))
            except:
                self.text = str(txttmp[:x])

            self.idx = self.idx + 1
            self.x = self.x - 1
        if self.x == 0:
            self.idx = 0
            self.x = len(self.backtext)
        self.rollTimerText.start(self.steptime)