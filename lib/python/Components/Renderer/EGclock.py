# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Renderer/EGclock.py
# Compiled at: 2017-10-02 01:52:08
from Components.VariableValue import VariableValue
from Renderer import Renderer
from enigma import eGauge

class EGclock(VariableValue, Renderer):

    def __init__(self):
        Renderer.__init__(self)
        VariableValue.__init__(self)

    GUI_WIDGET = eGauge

    def changed(self, what):
        if what[0] == self.CHANGED_CLEAR:
            return
        else:
            value = self.source.value
            if value is None:
                value = 0
            self.setValue(value)
            return

    GUI_WIDGET = eGauge

    def postWidgetCreate(self, instance):
        instance.setValue(0)

    def setValue(self, value):
        if self.instance is not None:
            self.instance.setValue(value)
        return