# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Timezones.py
# Compiled at: 2017-10-02 01:52:08
import xml.etree.cElementTree
from Tools.Directories import SCOPE_SKINresolveFilename
from os import environunlinksymlinkpath
import time
from Tools.StbHardware import setRTCoffset

class Timezones:

    def __init__(self):
        self.timezones = []
        self.readTimezonesFromFile()

    def readTimezonesFromFile(self):
        try:
            file = open(resolveFilename(SCOPE_SKIN, 'timezone.xml'))
            root = xml.etree.cElementTree.parse(file).getroot()
            file.close()
            for zone in root.findall('zone'):
                self.timezones.append((zone.get('name', ''), zone.get('zone', '')))

        except:
            pass

        if len(self.timezones) == 0:
            self.timezones = [
             ('UTC', 'UTC')]

    def activateTimezone(self, index):
        if len(self.timezones) <= index:
            return
        environ['TZ'] = self.timezones[index][1]
        try:
            unlink('/etc/localtime')
        except OSError:
            pass

        try:
            symlink('/usr/share/zoneinfo/%s' % self.timezones[index][1], '/etc/localtime')
        except OSError:
            pass

        try:
            time.tzset()
        except:
            from enigma import e_tzset
            e_tzset()

        if path.exists('/proc/stb/fp/rtc_offset'):
            setRTCoffset()

    def getTimezoneList(self):
        return [ str(x[0]) for x in self.timezones ]

    def getDefaultTimezone(self):
        t = '(GMT+01:00) Amsterdam, Berlin, Bern, Rome, Vienna'
        for a, b in self.timezones:
            if a == t:
                return a

        return self.timezones[0][0]


timezones = Timezones()