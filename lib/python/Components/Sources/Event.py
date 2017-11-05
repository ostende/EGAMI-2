# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Sources/Event.py
# Compiled at: 2017-10-02 01:52:07
from Source import Source

class Event(Source, object):

    def __init__(self):
        Source.__init__(self)
        self.evt = None
        return

    def getCurrentEvent(self):
        return self.evt

    event = property(getCurrentEvent)

    def newEvent(self, event):
        if not self.evt or self.evt != event:
            self.evt = event
            if not event:
                self.changed((self.CHANGED_CLEAR,))
            else:
                self.changed((self.CHANGED_ALL,))