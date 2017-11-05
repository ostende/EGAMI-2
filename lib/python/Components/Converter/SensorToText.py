# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/SensorToText.py
# Compiled at: 2017-10-02 01:52:07
from Components.Converter.Converter import Converter

class SensorToText(Converter, object):

    def __init__(self, arguments):
        Converter.__init__(self, arguments)

    def getText(self):
        if self.source.getValue() is None:
            return ''
        else:
            mark = ' '
            unit = self.source.getUnit()
            if unit in ('C', 'F'):
                mark = str('\xc2\xb0')
            return '%d%s%s' % (self.source.getValue(), mark, unit)

    text = property(getText)