# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/ValueBitTest.py
# Compiled at: 2017-10-02 01:52:07
from Converter import Converter
from Components.Element import cached

class ValueBitTest(Converter, object):

    def __init__(self, arg):
        Converter.__init__(self, arg)
        self.value = int(arg)

    @cached
    def getBoolean(self):
        return self.source.value & self.value and True or False

    boolean = property(getBoolean)