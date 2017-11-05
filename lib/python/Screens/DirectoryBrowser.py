# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Screens/DirectoryBrowser.py
# Compiled at: 2017-10-02 01:52:09
from Components.FileList import FileList
from Components.Sources.StaticText import StaticText
from Components.ActionMap import ActionMap
from Screens.Screen import Screen

class DirectoryBrowser(Screen):
    skin = '<screen name="DirectoryBrowser" position="center,center" size="520,440" title=" " >\n\t\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="0,0" size="140,40" alphatest="on" />\n\t\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="140,0" size="140,40" alphatest="on" />\n\t\t\t<widget source="key_red" render="Label" position="0,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t\t<widget source="key_green" render="Label" position="140,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />\n\t\t\t<widget source="curdir" render="Label" position="5,50" size="510,20"  font="Regular;20" halign="left" valign="center" backgroundColor="background" transparent="1" noWrap="1" />\n\t\t\t<widget name="filelist" position="5,80" size="510,345" scrollbarMode="showOnDemand" />\n\t\t</screen>'

    def __init__(self, session, curdir, matchingPattern=None):
        Screen.__init__(self, session)
        self['Title'].setText(_('Choose dir'))
        self['key_red'] = StaticText(_('Cancel'))
        self['key_green'] = StaticText(_('Save'))
        self['curdir'] = StaticText(_('current:  %s') % (curdir or ''))
        self.filelist = FileList(curdir, matchingPattern=matchingPattern, enableWrapAround=True)
        self.filelist.onSelectionChanged.append(self.__selChanged)
        self['filelist'] = self.filelist
        self['FilelistActions'] = ActionMap(['SetupActions', 'ColorActions'], {'green': self.keyGreen,
           'red': self.keyRed,
           'ok': self.keyOk,
           'cancel': self.keyRed
           })
        self.onLayoutFinish.append(self.__layoutFinished)

    def __layoutFinished(self):
        pass

    def getCurrentSelected(self):
        dirname = self.filelist.getCurrentDirectory()
        filename = self.filelist.getFilename()
        if not filename and not dirname:
            cur = ''
        elif not filename:
            cur = dirname
        elif not dirname:
            cur = filename
        elif not self.filelist.canDescent() or len(filename) <= len(dirname):
            cur = dirname
        else:
            cur = filename
        return cur or ''

    def __selChanged(self):
        self['curdir'].setText(_('current:  %s') % self.getCurrentSelected())

    def keyOk(self):
        if self.filelist.canDescent():
            self.filelist.descent()

    def keyGreen(self):
        if self.filelist.canDescent() and self.getCurrentSelected():
            self.close(self.getCurrentSelected())

    def keyRed(self):
        self.close(False)