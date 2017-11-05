# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Renderer/VVolumeText.py
# Compiled at: 2017-10-02 01:52:08
from Components.VariableText import VariableText
from enigma import eLabeleDVBVolumecontroleTimer
from Renderer import Renderer

class VVolumeText(Renderer, VariableText):

    def __init__(self):
        Renderer.__init__(self)
        VariableText.__init__(self)
        self.vol_timer = eTimer()
        self.vol_timer.callback.append(self.pollme)

    GUI_WIDGET = eLabel

    def changed(self, what):
        if not self.suspended:
            self.text = str(eDVBVolumecontrol.getInstance().getVolume())

    def pollme(self):
        self.changed(None)
        return

    def onShow(self):
        self.suspended = False
        self.vol_timer.start(200)

    def onHide(self):
        self.suspended = True
        self.vol_timer.stop()