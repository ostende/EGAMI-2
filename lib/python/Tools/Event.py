# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Tools/Event.py
# Compiled at: 2017-10-02 01:52:09


class Event:

    def __init__(self, start=None, stop=None):
        self.list = []
        self.start = start
        self.stop = stop

    def __call__(self, *args, **kwargs):
        for x in self.list:
            x(*args, **kwargs)

    def listen(self, fnc):
        was_empty = len(self.list) == 0
        self.list.append(fnc)
        if was_empty:
            if self.start:
                self.start()

    def unlisten(self, fnc):
        self.list.remove(fnc)
        if len(self.list) == 0:
            if self.stop:
                self.stop()