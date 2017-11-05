# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/TextCase.py
# Compiled at: 2017-10-02 01:52:07
from Converter import Converter
from Components.Element import cached

class TextCase(Converter):
    UPPER = 0
    LOWER = 1

    def __init__(self, type):
        Converter.__init__(self, type)
        self.type = self.UPPER
        if type == 'ToLower':
            self.type = self.LOWER
        elif type == 'ToUpper':
            self.type = self.UPPER

    @cached
    def getText(self):
        originaltext = self.source.getText()
        if self.type == self.UPPER:
            return originaltext.decode('utf-8').upper().encode('utf-8')
        else:
            if self.type == self.LOWER:
                return originaltext.decode('utf-8').lower().encode('utf-8')
            return originaltext

    text = property(getText)