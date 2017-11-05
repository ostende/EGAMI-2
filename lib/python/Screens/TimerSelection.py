# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Screens/TimerSelection.py
# Compiled at: 2017-10-02 01:52:09
from Screens.Screen import Screen
from Components.TimerList import TimerList
from Components.ActionMap import ActionMap

class TimerSelection(Screen):

    def __init__(self, session, list):
        Screen.__init__(self, session)
        self.setTitle(_('Timer selection'))
        self.list = list
        self['timerlist'] = TimerList(self.list)
        self['actions'] = ActionMap(['OkCancelActions'], {'ok': self.selected,
           'cancel': self.leave
           }, -1)

    def leave(self):
        self.close(None)
        return

    def selected(self):
        self.close(self['timerlist'].getCurrentIndex())