# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Screens/ClockDisplay.py
# Compiled at: 2017-10-02 01:52:09
from Screen import Screen

class ClockDisplay(Screen):

    def okbutton(self):
        self.session.close()

    def __init__(self, session, clock):
        Screen.__init__(self, session)
        self['theClock'] = clock
        b = Button('bye')
        b.onClick = [self.okbutton]
        self['okbutton'] = b
        self['title'] = Header('clock dialog: here you see the current uhrzeit!')