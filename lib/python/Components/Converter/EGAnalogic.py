# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/EGAnalogic.py
# Compiled at: 2017-10-02 01:52:07
from Components.Converter.Converter import Converter
from Components.Element import cached
from time import localtimestrftime

class EGAnalogic(Converter, object):

    def __init__(self, type):
        Converter.__init__(self, type)
        if type == 'Seconds':
            self.type = 1
        elif type == 'Minutes':
            self.type = 2
        elif type == 'Hours':
            self.type = 3
        else:
            self.type = -1

    @cached
    def getValue(self):
        time = self.source.time
        if time is None:
            return 0
        else:
            t = localtime(time)
            if self.type == 1:
                return int(t.tm_sec * 100 / 60)
            if self.type == 2:
                return int(t.tm_min * 100 / 60)
            if self.type == 3:
                return int(t.tm_hour * 100 / 12 + t.tm_min / 8)
            return

    value = property(getValue)