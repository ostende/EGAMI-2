# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/GUISkin.py
# Compiled at: 2017-10-02 01:52:08
from GUIComponent import GUIComponent
from skin import applyAllAttributes
from Tools.CList import CList
from Components.config import config
from Sources.StaticText import StaticText

class GUISkin:
    __module__ = __name__

    def __init__(self):
        self['Title'] = StaticText()
        self.onLayoutFinish = []
        self.onAnimationEnd = []
        self.summaries = CList()
        self.instance = None
        self.desktop = None
        return

    def animationEnd(self):
        for f in self.onAnimationEnd:
            f()

    def createGUIScreen(self, parent, desktop, updateonly=False):
        for val in self.renderer:
            if isinstance(val, GUIComponent):
                if not updateonly:
                    val.GUIcreate(parent)
                if not val.applySkin(desktop, self):
                    print 'warning, skin is missing renderer', val, 'in', self

        for key in self:
            val = self[key]
            if isinstance(val, GUIComponent):
                if not updateonly:
                    val.GUIcreate(parent)
                depr = val.deprecationInfo
                if val.applySkin(desktop, self):
                    if depr:
                        print "WARNING: OBSOLETE COMPONENT '%s' USED IN SKIN. USE '%s' INSTEAD!" % (key, depr[0])
                        print 'OBSOLETE COMPONENT WILL BE REMOVED %s, PLEASE UPDATE!' % depr[1]
                elif not depr:
                    print 'warning, skin is missing element', key, 'in', self

        for w in self.additionalWidgets:
            if not updateonly:
                w.instance = w.widget(parent)
            applyAllAttributes(w.instance, desktop, w.skinAttributes, self.scale)

        for f in self.onLayoutFinish:
            if type(f) is not type(self.close):
                exec f in globals(), locals()
            else:
                f()

        if config.misc.fadeShowMenu.value and parent:
            parent.animationEnd.get().append(self.animationEnd)

    def deleteGUIScreen(self):
        if self.instance and config.misc.fadeShowMenu.value:
            self.instance.animationEnd.get().remove(self.animationEnd)
        for name, val in self.items():
            if isinstance(val, GUIComponent):
                val.GUIdelete()

    def close(self):
        self.deleteGUIScreen()

    def createSummary(self):
        return None

    def addSummary(self, summary):
        if summary is not None:
            self.summaries.append(summary)
        return

    def removeSummary(self, summary):
        if summary is not None:
            self.summaries.remove(summary)
        return

    def setTitle(self, title):
        try:
            if self.instance:
                self.instance.setTitle(title)
            self['Title'].text = title
            self.summaries.setTitle(title)
        except:
            pass

    def getTitle(self):
        return self['Title'].text

    title = property(getTitle, setTitle)

    def setDesktop(self, desktop):
        self.desktop = desktop

    def applySkin(self):
        z = 0
        baseres = (1280, 720)
        idx = 0
        skin_title_idx = -1
        title = self.title
        for key, value in self.skinAttributes:
            if key == 'zPosition':
                z = int(value)
            elif key == 'title':
                skin_title_idx = idx
                if title:
                    self.skinAttributes[skin_title_idx] = (
                     'title', title)
                else:
                    self['Title'].text = value
                    self.summaries.setTitle(value)
            elif key == 'baseResolution':
                baseres = tuple([ int(x) for x in value.split(',') ])
            idx += 1

        self.scale = (
         (
          baseres[0], baseres[0]), (baseres[1], baseres[1]))
        if not self.instance:
            from enigma import eWindow
            self.instance = eWindow(self.desktop, z)
        if skin_title_idx == -1 and title:
            self.skinAttributes.append(('title', title))
        self.skinAttributes.sort(key=lambda a: {'position': 1}.get(a[0], 0))
        applyAllAttributes(self.instance, self.desktop, self.skinAttributes, self.scale)
        self.createGUIScreen(self.instance, self.desktop)