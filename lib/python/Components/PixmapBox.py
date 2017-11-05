# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/PixmapBox.py
# Compiled at: 2017-10-02 01:52:08
from GUIComponent import GUIComponent
from enigma import ePixmapBox
from Tools.Directories import resolveFilenameSCOPE_CURRENT_SKIN
from os import path
from skin import loadPixmap

class PixmapBox(GUIComponent):

    def __init__(self):
        GUIComponent.__init__(self)

    GUI_WIDGET = ePixmapBox

    def applySkin(self, desktop, screen):
        if self.skinAttributes is not None:
            skin_path_prefix = getattr(screen, 'skin_path', path)
            attribs = []
            for attrib, value in self.skinAttributes:
                if attrib == 'pixmaps':
                    index = 0
                    pixmaps = value.split(',')
                    for p in pixmaps:
                        self.instance.setPixmap(loadPixmap(resolveFilename(SCOPE_CURRENT_SKIN, p, path_prefix=skin_path_prefix), desktop), index, 0)
                        index += 1

                else:
                    attribs.append((attrib, value))

            self.skinAttributes = attribs
        return GUIComponent.applySkin(self, desktop, screen)

    def setVisible(self, status, index):
        self.instance.setVisible(status, index)