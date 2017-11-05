# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Sources/RecordState.py
# Compiled at: 2017-10-02 01:52:07
from Source import Source
from Components.Element import cached
from enigma import iRecordableServicepNavigation
import Components.RecordingConfig
from Components.config import config

class RecordState(Source):

    def __init__(self, session):
        Source.__init__(self)
        self.records_running = 0
        self.session = session
        session.nav.record_event.append(self.gotRecordEvent)
        self.gotRecordEvent(None, None)
        return

    def gotRecordEvent(self, service, event):
        prev_records = self.records_running
        if event in (iRecordableService.evEnd, iRecordableService.evStart, None):
            recs = self.session.nav.getRecordings(False, Components.RecordingConfig.recType(config.recording.show_rec_symbol_for_rec_types.getValue()))
            self.records_running = len(recs)
            if self.records_running != prev_records:
                self.changed((self.CHANGED_ALL,))
        return

    def destroy(self):
        self.session.nav.record_event.remove(self.gotRecordEvent)
        Source.destroy(self)

    @cached
    def getBoolean(self):
        return self.records_running and True or False

    boolean = property(getBoolean)

    @cached
    def getValue(self):
        return self.records_running

    value = property(getValue)