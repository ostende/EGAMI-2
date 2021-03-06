# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Slider.py
# Compiled at: 2017-10-02 01:52:08
from HTMLComponent import HTMLComponent
from GUIComponent import GUIComponent
from VariableValue import VariableValue
from enigma import eSlider

class Slider(VariableValue, HTMLComponent, GUIComponent):

    def __init__(self, min, max):
        VariableValue.__init__(self)
        GUIComponent.__init__(self)
        self.min = min
        self.max = max

    GUI_WIDGET = eSlider

    def postWidgetCreate(self, instance):
        instance.setRange(self.min, self.max)