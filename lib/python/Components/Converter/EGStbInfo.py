# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/EGStbInfo.py
# Compiled at: 2017-10-02 01:52:07
from Components.Converter.Converter import Converter
from Components.Element import cachedElementError
from Components.About import about
from boxbranding import getBoxTypegetMachineBrandgetMachineNamegetDriverDategetImageVersion

class EGStbInfo(Converter, object):
    BOXTYPE = 1
    MACHINEBRAND = 2
    MACHINENAME = 3
    DRIVERSDATE = 4
    IMAGEVERSION = 5
    ALL = 6

    def __init__(self, type):
        Converter.__init__(self, type)
        if type == 'getBoxType':
            self.type = self.BOXTYPE
        elif type == 'getMachineBrand':
            self.type = self.MACHINEBRAND
        elif type == 'getMachineName':
            self.type = self.MACHINENAME
        elif type == 'getDriverDate':
            self.type = self.DRIVERSDATE
        elif type == 'getImageVersion':
            self.type = self.IMAGEVERSION
        elif type == 'All':
            self.type = self.ALL
        else:
            self.type = self.ALL

    @cached
    def getText(self):
        if self.type == self.BOXTYPE:
            return getBoxType()
        if self.type == self.MACHINEBRAND:
            return getMachineBrand()
        if self.type == self.MACHINENAME:
            return getMachineName()
        if self.type == self.DRIVERSDATE:
            return getDriverDate()
        if self.type == self.IMAGEVERSION:
            return 'EGAMI %s' % about.getImageVersionString()
        if self.type == self.ALL:
            return 'EGAMI %s - %s %s' % (about.getImageVersionString(), getMachineBrand(), getMachineName())

    text = property(getText)