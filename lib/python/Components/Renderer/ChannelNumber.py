# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Renderer/ChannelNumber.py
# Compiled at: 2017-10-02 01:52:08
from Components.VariableText import VariableText
from enigma import eLabeliPlayableService
from Renderer import Renderer

class ChannelNumber(Renderer, VariableText):

    def __init__(self):
        Renderer.__init__(self)
        VariableText.__init__(self)
        self.text = '---'

    GUI_WIDGET = eLabel

    def changed(self, what):
        if what == True or what[0] == self.CHANGED_SPECIFIC and what[1] == iPlayableService.evStart:
            service = self.source.serviceref
            num = service and service.getChannelNum() or None
            if num:
                self.text = str(num)
            else:
                self.text = '---'
        return