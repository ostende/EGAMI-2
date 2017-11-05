# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Screens/SimpleSummary.py
# Compiled at: 2017-10-02 01:52:09
from Screens.Screen import Screen

class SimpleSummary(Screen):
    skin = '\n\t<screen position="0,0" size="132,64">\n\t\t<widget source="global.CurrentTime" render="Label" position="56,46" size="82,18" font="Regular;16">\n\t\t\t<convert type="ClockToText">WithSeconds</convert>\n\t\t</widget>\n\t\t<widget source="parent.Title" render="Label" position="6,4" size="120,42" font="Regular;18" />\n\t</screen>'

    def __init__(self, session, parent):
        Screen.__init__(self, session, parent=parent)
        names = parent.skinName
        if not isinstance(names, list):
            names = [
             names]
        self.skinName = [ x + '_summary' for x in names ]
        self.skinName.append('SimpleSummary')
        self.skin = parent.__dict__.get('skin_summary', self.skin)

    def updateProgress(self):
        pass

    def updateService(self):
        pass