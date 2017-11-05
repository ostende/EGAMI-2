# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/VideoWindow.py
# Compiled at: 2017-10-02 01:52:08
from GUIComponent import GUIComponent
from enigma import eVideoWidgeteSize

class VideoWindow(GUIComponent):

    def __init__(self, decoder=1, fb_width=720, fb_height=576):
        GUIComponent.__init__(self)
        self.decoder = decoder
        self.fb_width = fb_width
        self.fb_height = fb_height

    GUI_WIDGET = eVideoWidget

    def postWidgetCreate(self, instance):
        instance.setDecoder(self.decoder)
        instance.setFBSize(eSize(self.fb_width, self.fb_height))