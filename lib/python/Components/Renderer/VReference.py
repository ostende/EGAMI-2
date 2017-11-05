# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Renderer/VReference.py
# Compiled at: 2017-10-02 01:52:08
from Renderer import Renderer
from enigma import eLabel
from Components.VariableText import VariableText
from enigma import eServiceReference

class VReference(VariableText, Renderer):

    def __init__(self):
        Renderer.__init__(self)
        VariableText.__init__(self)

    GUI_WIDGET = eLabel

    def connect(self, source):
        Renderer.connect(self, source)
        self.changed((self.CHANGED_DEFAULT,))

    def changed(self, what):
        if self.instance:
            if what[0] == self.CHANGED_CLEAR:
                self.text = 'Reference not found !'
            else:
                service = self.source.service
                sname = service.toString()
                pos = sname.rfind(':')
                if pos != -1:
                    self.text = 'Reference: ' + sname[:-1]
                else:
                    self.text = 'Reference reading error !'