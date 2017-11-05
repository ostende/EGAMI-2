# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/Combine.py
# Compiled at: 2017-10-02 01:52:07
from Converter import Converter
from Components.Element import cached

class Combine(Converter, object):
    SINGLE_SOURCE = False

    def __init__(self, arg=None, func=None):
        Converter.__init__(self, arg)
        self.func = func

    @cached
    def getValue(self):
        return self.func(self.sources)

    value = property(getValue)