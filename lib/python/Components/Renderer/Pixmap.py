# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Renderer/Pixmap.py
# Compiled at: 2017-10-02 01:52:08
from Renderer import Renderer
from enigma import ePixmap

class Pixmap(Renderer):

    def __init__(self):
        Renderer.__init__(self)

    GUI_WIDGET = ePixmap

    def postWidgetCreate(self, instance):
        self.changed((self.CHANGED_DEFAULT,))

    def changed(self, what):
        if what[0] != self.CHANGED_CLEAR:
            if self.source and hasattr(self.source, 'pixmap'):
                if self.instance:
                    self.instance.setPixmap(self.source.pixmap)