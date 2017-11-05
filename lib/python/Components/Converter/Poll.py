# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/Poll.py
# Compiled at: 2017-10-02 01:52:07
from enigma import eTimer

class Poll(object):

    def __init__(self):
        self.__poll_timer = eTimer()
        self.__poll_timer.callback.append(self.poll)
        self.__interval = 1000
        self.__enabled = False

    def __setInterval(self, interval):
        self.__interval = interval
        if self.__enabled:
            self.__poll_timer.start(self.__interval)
        else:
            self.__poll_timer.stop()

    def __setEnable(self, enabled):
        self.__enabled = enabled
        self.poll_interval = self.__interval

    poll_interval = property(lambda self: self.__interval, __setInterval)
    poll_enabled = property(lambda self: self.__enabled, __setEnable)

    def poll(self):
        self.changed((self.CHANGED_POLL,))

    def doSuspend(self, suspended):
        if self.__enabled:
            if suspended:
                self.__poll_timer.stop()
            else:
                self.poll()
                self.poll_enabled = True

    def destroy(self):
        self.__poll_timer.callback.remove(self.poll)