# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Sources/Progress.py
# Compiled at: 2017-10-02 01:52:07
from Source import Source

class Progress(Source):

    def __init__(self, value=0, valuerange=100):
        Source.__init__(self)
        self.__value = value
        self.range = valuerange

    def getValue(self):
        return self.__value

    def setValue(self, value):
        self.__value = value
        self.changed((self.CHANGED_ALL,))

    def setRange(self, range=100):
        self.range = range
        self.changed((self.CHANGED_ALL,))

    def getRange(self):
        return self.range

    value = property(getValue, setValue)