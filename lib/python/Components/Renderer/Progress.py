# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Renderer/Progress.py
# Compiled at: 2017-10-02 01:52:08
from Components.VariableValue import VariableValue
from Renderer import Renderer
from enigma import eSlider

class Progress(VariableValue, Renderer):

    def __init__(self):
        Renderer.__init__(self)
        VariableValue.__init__(self)
        self.__start = 0
        self.__end = 100

    GUI_WIDGET = eSlider

    def changed(self, what):
        if what[0] == self.CHANGED_CLEAR:
            self.range, self.value = ((0, 1), 0)
            return
        else:
            range = self.source.range or 100
            value = self.source.value
            if value is None:
                value = 0
            if range > 2147483647:
                range = 2147483647
            if value > range:
                value = range
            if value < 0:
                value = 0
            self.range, self.value = (
             0, range), value
            return

    def postWidgetCreate(self, instance):
        instance.setRange(self.__start, self.__end)

    def setRange(self, range):
        self.__start, self.__end = range
        if self.instance is not None:
            self.instance.setRange(self.__start, self.__end)
        return

    def getRange(self):
        return (
         self.__start, self.__end)

    range = property(getRange, setRange)