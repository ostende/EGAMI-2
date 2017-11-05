# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Renderer/EGStbInfo.py
# Compiled at: 2017-10-02 01:52:08
from Renderer import Renderer
from enigma import ePixmapePicLoad
from Tools.Directories import pathExistsSCOPE_SKIN_IMAGESCOPE_ACTIVE_SKINresolveFilename
from Tools.Directories import fileExists
import os
from boxbranding import getMachineBuild

def getBoxPicture():
    pngname = '/usr/share/enigma2/' + getMachineBuild() + '.png'
    if fileExists(pngname):
        return pngname
    else:
        return ''


class EGStbInfo(Renderer):

    def __init__(self):
        Renderer.__init__(self)
        self.PicLoad = ePicLoad()
        self.PicLoad.PictureData.get().append(self.updatePicon)
        self.piconsize = (0, 0)
        self.lastPath = None
        self.pngname = getBoxPicture()
        return

    def applySkin(self, desktop, parent):
        attribs = self.skinAttributes[:]
        for attrib, value in self.skinAttributes:
            if attrib == 'size':
                self.piconsize = value

        self.skinAttributes = attribs
        return Renderer.applySkin(self, desktop, parent)

    GUI_WIDGET = ePixmap

    def postWidgetCreate(self, instance):
        self.changed((self.CHANGED_DEFAULT,))

    def updatePicon(self, picInfo=None):
        ptr = self.PicLoad.getData()
        if ptr is not None:
            self.instance.setPixmap(ptr.__deref__())
            self.instance.show()
        return

    def changed(self, what):
        if self.instance:
            if fileExists(self.pngname):
                self.instance.setScale(1)
                self.instance.setPixmapFromFile(self.pngname)
                self.instance.show()
            else:
                self.instance.hide()