# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/ProgressBar.py
# Compiled at: 2017-10-02 01:52:08
from HTMLComponent import HTMLComponent
from GUIComponent import GUIComponent
from VariableValue import VariableValue
from enigma import eSlider

class ProgressBar(VariableValue, HTMLComponent, GUIComponent, object):

    def __init__(self):
        GUIComponent.__init__(self)
        VariableValue.__init__(self)
        self.__start = 0
        self.__end = 100

    GUI_WIDGET = eSlider

    def postWidgetCreate(self, instance):
        instance.setRange(self.__start, self.__end)

    def setRange(self, range):
        __start, __end = range
        if self.instance is not None:
            self.instance.setRange(__start, __end)
        return

    def getRange(self):
        return (
         self.__start, self.__end)

    range = property(getRange, setRange)