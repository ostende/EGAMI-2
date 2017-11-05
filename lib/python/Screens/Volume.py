# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Screens/Volume.py
# Compiled at: 2017-10-02 01:52:09
from Screens.Screen import Screen
from Components.VolumeBar import VolumeBar

class Volume(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        self.volumeBar = VolumeBar()
        self['Volume'] = self.volumeBar

    def setValue(self, vol):
        print '[Volume] setValue', vol
        self.volumeBar.setValue(vol)