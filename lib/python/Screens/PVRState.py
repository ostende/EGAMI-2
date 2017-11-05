# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Screens/PVRState.py
# Compiled at: 2017-10-02 01:52:09
from Screen import Screen
from Components.Label import Label
from Components.Pixmap import PixmapMultiPixmap

class PVRState(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        self['eventname'] = Label()
        self['state'] = Label()
        self['speed'] = Label()
        self['statusicon'] = MultiPixmap()


class TimeshiftState(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        self['eventname'] = Label()
        self['state'] = Label()
        self['speed'] = Label()
        self['statusicon'] = MultiPixmap()
        self['PTSSeekBack'] = Pixmap()
        self['PTSSeekPointer'] = Pixmap()