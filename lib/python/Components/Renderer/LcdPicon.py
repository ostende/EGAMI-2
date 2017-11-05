# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Renderer/LcdPicon.py
# Compiled at: 2017-10-02 01:52:08
import os
import re
import unicodedata
from Renderer import Renderer
from enigma import ePixmapePicLoad
from Tools.Alternatives import GetWithAlternative
from Tools.Directories import pathExistsSCOPE_ACTIVE_SKINresolveFilename
from Components.Harddisk import harddiskmanager
from boxbranding import getBoxTypegetMachineBuild
from ServiceReference import ServiceReference
searchPaths = []
lastLcdPiconPath = None

def initLcdPiconPaths():
    global searchPaths
    searchPaths = []
    for mp in ('/usr/share/enigma2/', '/'):
        onMountpointAdded(mp)

    for part in harddiskmanager.getMountedPartitions():
        onMountpointAdded(part.mountpoint)


def onMountpointAdded(mountpoint):
    try:
        if getBoxType() in ('vuultimo', 'et10000', 'mutant2400', 'quadbox2400') or getMachineBuild() in 'inihdp':
            path = os.path.join(mountpoint, 'piconlcd') + '/'
        else:
            path = os.path.join(mountpoint, 'picon') + '/'
        if os.path.isdir(path) and path not in searchPaths:
            for fn in os.listdir(path):
                if fn.endswith('.png'):
                    print '[LcdPicon] adding path:', path
                    searchPaths.append(path)
                    break

    except Exception as ex:
        print '[LcdPicon] Failed to investigate %s:' % mountpoint, ex


def onMountpointRemoved(mountpoint):
    if getBoxType() in ('vuultimo', 'et10000', 'mutant2400', 'quadbox2400') or getMachineBuild() in 'inihdp':
        path = os.path.join(mountpoint, 'piconlcd') + '/'
    else:
        path = os.path.join(mountpoint, 'picon') + '/'
    try:
        searchPaths.remove(path)
        print '[LcdPicon] removed path:', path
    except:
        pass


def onPartitionChange(why, part):
    if why == 'add':
        onMountpointAdded(part.mountpoint)
    elif why == 'remove':
        onMountpointRemoved(part.mountpoint)


def findLcdPicon(serviceName):
    global lastLcdPiconPath
    if lastLcdPiconPath is not None:
        pngname = lastLcdPiconPath + serviceName + '.png'
        if pathExists(pngname):
            return pngname
        else:
            return ''

    else:
        pngname = ''
        for path in searchPaths:
            if pathExists(path) and not path.startswith('/media/net') and not path.startswith('/media/autofs'):
                pngname = path + serviceName + '.png'
                if pathExists(pngname):
                    lastLcdPiconPath = path
                    break
            elif pathExists(path):
                pngname = path + serviceName + '.png'
                if pathExists(pngname):
                    lastLcdPiconPath = path
                    break

        if pathExists(pngname):
            return pngname
        return ''
    return


def getLcdPiconName(serviceName):
    sname = '_'.join(GetWithAlternative(serviceName).split(':', 10)[:10])
    pngname = findLcdPicon(sname)
    if not pngname:
        fields = sname.split('_', 3)
        if len(fields) > 2 and fields[2] != '1':
            fields[2] = '1'
        if len(fields) > 0 and fields[0] != '1':
            fields[0] = '1'
        pngname = findLcdPicon('_'.join(fields))
    if not pngname:
        name = ServiceReference(serviceName).getServiceName()
        name = unicodedata.normalize('NFKD', unicode(name, 'utf_8', errors='ignore')).encode('ASCII', 'ignore')
        name = re.sub('[^a-z0-9]', '', name.replace('&', 'and').replace('+', 'plus').replace('*', 'star').lower())
        if len(name) > 0:
            pngname = findLcdPicon(name)
            if not pngname and len(name) > 2 and name.endswith('hd'):
                pngname = findLcdPicon(name[:-2])
    return pngname


class LcdPicon(Renderer):

    def __init__(self):
        Renderer.__init__(self)
        self.PicLoad = ePicLoad()
        self.PicLoad.PictureData.get().append(self.updatePicon)
        self.piconsize = (0, 0)
        self.pngname = ''
        self.lastPath = None
        if getBoxType() in ('vuultimo', 'et10000', 'mutant2400', 'quadbox2400') or getMachineBuild() in 'inihdp':
            pngname = findLcdPicon('lcd_picon_default')
        else:
            pngname = findLcdPicon('picon_default')
        self.defaultpngname = None
        if not pngname:
            if getBoxType() in ('vuultimo', 'et10000', 'mutant2400', 'quadbox2400') or getMachineBuild() in 'inihdp':
                tmp = resolveFilename(SCOPE_ACTIVE_SKIN, 'lcd_picon_default.png')
            else:
                tmp = resolveFilename(SCOPE_ACTIVE_SKIN, 'picon_default.png')
            if pathExists(tmp):
                pngname = tmp
            elif getBoxType() in ('vuultimo', 'et10000', 'mutant2400', 'quadbox2400') or getMachineBuild() in 'inihdp':
                pngname = resolveFilename(SCOPE_ACTIVE_SKIN, 'lcd_picon_default.png')
            else:
                pngname = resolveFilename(SCOPE_ACTIVE_SKIN, 'picon_default.png')
        if os.path.getsize(pngname):
            self.defaultpngname = pngname
        return

    def addPath(self, value):
        if pathExists(value):
            if not value.endswith('/'):
                value += '/'
            if value not in searchPaths:
                searchPaths.append(value)

    def applySkin(self, desktop, parent):
        attribs = self.skinAttributes[:]
        for attrib, value in self.skinAttributes:
            if attrib == 'path':
                self.addPath(value)
                attribs.remove((attrib, value))
            elif attrib == 'size':
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
            pngname = ''
            if what[0] == 1 or what[0] == 3:
                pngname = getLcdPiconName(self.source.text)
                if not pathExists(pngname):
                    pngname = self.defaultpngname
                if self.pngname != pngname:
                    if pngname:
                        self.PicLoad.setPara((self.piconsize[0], self.piconsize[1], 0, 0, 1, 1, '#FF000000'))
                        self.PicLoad.startDecode(pngname)
                    else:
                        self.instance.hide()
                    self.pngname = pngname


harddiskmanager.on_partition_list_change.append(onPartitionChange)
initLcdPiconPaths()