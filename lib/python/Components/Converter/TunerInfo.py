# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/TunerInfo.py
# Compiled at: 2017-10-02 01:52:07
from Components.Sources.TunerInfo import TunerInfo as TunerInfoSource
from Components.Converter.Converter import Converter
from Components.Element import cached

class TunerInfo(Converter, object):

    def __init__(self, type):
        Converter.__init__(self, type)
        self.type = {'TunerUseMask': TunerInfoSource.FE_USE_MASK,'TunerAvailable': TunerInfoSource.TUNER_AVAILABLE
           }[type]

    @cached
    def getBoolean(self):
        if self.type == TunerInfoSource.FE_USE_MASK:
            return self.source.getTunerUseMask() and True or False

    boolean = property(getBoolean)

    @cached
    def getText(self):
        if self.type == TunerInfoSource.FE_USE_MASK:
            return str(self.source.getTunerUseMask())
        return ''

    text = property(getText)

    @cached
    def getValue(self):
        if self.type == TunerInfoSource.FE_USE_MASK:
            return self.source.getTunerUseMask()
        if self.type == TunerInfoSource.TUNER_AVAILABLE:
            return self.source.getTunerAmount()
        return -1

    value = property(getValue)

    def changed(self, what):
        if what[0] != self.CHANGED_SPECIFIC or what[1] == self.type:
            Converter.changed(self, what)