# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Tools/CList.py
# Compiled at: 2017-10-02 01:52:09


class CList(list):

    def __getattr__(self, attr):
        return CList([ getattr(a, attr) for a in self ])

    def __call__(self, *args, **kwargs):
        for x in self:
            x(*args, **kwargs)