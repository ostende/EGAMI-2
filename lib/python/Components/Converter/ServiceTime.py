# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/ServiceTime.py
# Compiled at: 2017-10-02 01:52:07
from Converter import Converter
from Components.Element import cachedElementError
from enigma import iServiceInformation

class ServiceTime(Converter, object):
    STARTTIME = 0
    ENDTIME = 1
    DURATION = 2

    def __init__(self, type):
        Converter.__init__(self, type)
        if type == 'EndTime':
            self.type = self.ENDTIME
        elif type == 'StartTime':
            self.type = self.STARTTIME
        elif type == 'Duration':
            self.type = self.DURATION
        else:
            raise ElementError("'%s' is not <StartTime|EndTime|Duration> for ServiceTime converter" % type)

    @cached
    def getTime(self):
        service = self.source.service
        info = self.source.info
        if not info or not service:
            return None
        else:
            if self.type == self.STARTTIME:
                return info.getInfo(service, iServiceInformation.sTimeCreate)
            if self.type == self.ENDTIME:
                begin = info.getInfo(service, iServiceInformation.sTimeCreate)
                len = info.getLength(service) + 10
                return begin + len
            if self.type == self.DURATION:
                return info.getLength(service) + 10
            return None

    time = property(getTime)