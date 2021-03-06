# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Sources/StreamService.py
# Compiled at: 2017-10-02 01:52:07
from Source import Source
from Components.Element import cached
from enigma import eServiceReferencepNavigation

class StreamService(Source):

    def __init__(self, navcore):
        Source.__init__(self)
        self.ref = None
        self.__service = None
        self.navcore = navcore
        return

    def serviceEvent(self, event):
        pass

    @cached
    def getService(self):
        return self.__service

    service = property(getService)

    def handleCommand(self, cmd):
        print 'StreamService handle command', cmd
        self.ref = eServiceReference(cmd)

    def recordEvent(self, service, event):
        if service is self.__service:
            return
        print 'RECORD event for us:', service
        self.changed((self.CHANGED_ALL,))

    def execBegin(self):
        if self.ref is None:
            print 'StreamService has no service ref set.'
            return
        else:
            print 'StreamService execBegin', self.ref.toString()
            try:
                self.__service = self.navcore.recordService(self.ref, False, pNavigation.isStreaming)
            except:
                self.__service = self.navcore.recordService(self.ref)

            self.navcore.record_event.append(self.recordEvent)
            if self.__service is not None:
                self.__service.prepareStreaming()
                self.__service.start()
            return

    def execEnd(self):
        print 'StreamService execEnd', self.ref.toString()
        self.navcore.record_event.remove(self.recordEvent)
        if self.__service is not None:
            self.navcore.stopRecordService(self.__service)
            self.__service = None
        return