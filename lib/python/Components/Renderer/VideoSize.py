# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Renderer/VideoSize.py
# Compiled at: 2017-10-02 01:52:08
from Components.VariableText import VariableText
from enigma import eLabeliServiceInformation
from Renderer import Renderer

class VideoSize(Renderer, VariableText):

    def __init__(self):
        Renderer.__init__(self)
        VariableText.__init__(self)

    GUI_WIDGET = eLabel

    def changed(self, what):
        service = self.source.service
        info = service and service.info()
        if info is None:
            self.text = ''
            return
        else:
            xresol = info.getInfo(iServiceInformation.sVideoWidth)
            yresol = info.getInfo(iServiceInformation.sVideoHeight)
            if xresol > 0:
                self.text = str(xresol) + 'x' + str(yresol)
            else:
                self.text = ''
            return