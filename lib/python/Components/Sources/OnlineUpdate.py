# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Sources/OnlineUpdate.py
# Compiled at: 2017-10-02 01:52:07
from Source import Source
from Components.Element import cached
from Components.OnlineUpdateCheck import versioncheck
from enigma import eTimer

class OnlineUpdateStableCheck(Source):

    def __init__(self):
        Source.__init__(self)
        self.check_timer = eTimer()
        self.check_timer.callback.append(self.poll)
        self.check_timer.start(60000)

    @cached
    def getBoolean(self):
        return versioncheck.getStableUpdateAvailable()

    boolean = property(getBoolean)

    def poll(self):
        self.changed((self.CHANGED_POLL,))

    def doSuspend(self, suspended):
        if suspended:
            self.check_timer.stop()
        else:
            self.check_timer.start(3600000)
            self.poll()

    def destroy(self):
        self.check_timer.callback.remove(self.poll)
        Source.destroy(self)


class OnlineUpdateUnstableCheck(Source):

    def __init__(self):
        Source.__init__(self)
        self.check_timer = eTimer()
        self.check_timer.callback.append(self.poll)
        self.check_timer.start(60000)

    @cached
    def getBoolean(self):
        return versioncheck.getUnstableUpdateAvailable()

    boolean = property(getBoolean)

    def poll(self):
        self.changed((self.CHANGED_POLL,))

    def doSuspend(self, suspended):
        if suspended:
            self.check_timer.stop()
        else:
            self.check_timer.start(3600000)
            self.poll()

    def destroy(self):
        self.check_timer.callback.remove(self.poll)
        Source.destroy(self)