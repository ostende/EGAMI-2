# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Renderer/Renderer.py
# Compiled at: 2017-10-02 01:52:08
from Components.GUIComponent import GUIComponent
from Components.Element import Element

class Renderer(GUIComponent, Element):

    def __init__(self):
        Element.__init__(self)
        GUIComponent.__init__(self)

    def onShow(self):
        self.suspended = False

    def onHide(self):
        self.suspended = True