# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Sources/ServiceEvent.py
# Compiled at: 2017-10-02 01:52:07
from Components.Element import cached
from enigma import eServiceCenter
from Source import Source

class ServiceEvent(Source, object):

    def __init__(self):
        Source.__init__(self)
        self.service = None
        return

    @cached
    def getCurrentService(self):
        return self.service

    @cached
    def getCurrentEvent(self):
        return self.service and self.info and self.info.getEvent(self.service)

    @cached
    def getInfo(self):
        return self.service and eServiceCenter.getInstance().info(self.service)

    event = property(getCurrentEvent)
    info = property(getInfo)

    def newService(self, ref):
        if not self.service or not ref or self.service != ref:
            self.service = ref
            if not ref:
                self.changed((self.CHANGED_CLEAR,))
            else:
                self.changed((self.CHANGED_ALL,))