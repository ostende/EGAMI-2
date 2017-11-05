# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Screens/FixedMenu.py
# Compiled at: 2017-10-02 01:52:09
from Screen import Screen
from Components.Sources.List import List
from Components.ActionMap import ActionMap
from Components.Sources.StaticText import StaticText

class FixedMenu(Screen):

    def okbuttonClick(self):
        selection = self['menu'].getCurrent()
        if selection and len(selection) > 1:
            selection[1]()

    def __init__(self, session, title, list):
        Screen.__init__(self, session)
        self['menu'] = List(list)
        self['actions'] = ActionMap(['OkCancelActions'], {'ok': self.okbuttonClick,
           'cancel': self.close
           })
        self['title'] = StaticText(title)