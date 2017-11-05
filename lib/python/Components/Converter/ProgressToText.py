# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/ProgressToText.py
# Compiled at: 2017-10-02 01:52:07
from Components.Converter.Converter import Converter
from Components.Element import cached

class ProgressToText(Converter, object):

    def __init__(self, type):
        Converter.__init__(self, type)
        self.in_percent = 'InPercent' in type.split(',')

    @cached
    def getText(self):
        r = self.source.range
        v = self.source.value
        if self.in_percent:
            if r:
                return '%d %%' % (v * 100 / r)
            else:
                return None

        else:
            return '%d / %d' % (v, r)
        return None

    text = property(getText)