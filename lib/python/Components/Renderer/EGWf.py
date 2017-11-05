# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Renderer/EGWf.py
# Compiled at: 2017-10-02 01:52:08
from Renderer import Renderer
from enigma import ePixmapeEnv
from Tools.Directories import fileExistsSCOPE_SKIN_IMAGESCOPE_CURRENT_SKINresolveFilename
from Components.config import ConfigTextconfigConfigSubsection

class EGWf(Renderer):

    def __init__(self):
        Renderer.__init__(self)
        self.path = 'picon'
        self.nameCache = {}
        self.pngname = ''

    def applySkin(self, desktop, parent):
        attribs = []
        for attrib, value in self.skinAttributes:
            if attrib == 'path':
                self.path = value
            else:
                attribs.append((attrib, value))

        self.skinAttributes = attribs
        return Renderer.applySkin(self, desktop, parent)

    GUI_WIDGET = ePixmap

    def changed(self, what):
        if self.instance:
            pngname = 'xxx'
            if what[0] != self.CHANGED_CLEAR:
                pngname = self.source.text
                self.nameCache[pngname] = pngname
            if self.pngname != pngname:
                if pngname == '':
                    self.instance.hide()
                else:
                    self.instance.show()
                    self.instance.setPixmapFromFile(pngname)
                self.pngname = pngname