# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Sources/Clock.py
# Compiled at: 2017-10-02 01:52:07
from Components.Element import cached
from enigma import eTimer
from time import time as getTime
from Source import Source

class Clock(Source):

    def __init__(self):
        Source.__init__(self)
        self.clock_timer = eTimer()
        self.clock_timer.callback.append(self.poll)
        self.clock_timer.start(1000)

    @cached
    def getClock(self):
        return getTime()

    time = property(getClock)

    def poll(self):
        self.changed((self.CHANGED_POLL,))

    def doSuspend(self, suspended):
        if suspended:
            self.clock_timer.stop()
        else:
            self.clock_timer.start(1000)
            self.poll()

    def destroy(self):
        self.clock_timer.callback.remove(self.poll)
        Source.destroy(self)