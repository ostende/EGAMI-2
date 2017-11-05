# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/StringListSelection.py
# Compiled at: 2017-10-02 01:52:07
from Components.Converter.Converter import Converter
from Components.Element import cached

class StringListSelection(Converter, object):

    def __init__(self, args):
        Converter.__init__(self, args)

    def selChanged(self):
        self.downstream_elements.changed((self.CHANGED_ALL, 0))

    @cached
    def getText(self):
        cur = self.source.current
        if cur and len(cur):
            return cur[0]
        else:
            return None

    text = property(getText)

    def changed(self, what):
        if what[0] == self.CHANGED_DEFAULT:
            self.source.onSelectionChanged.append(self.selChanged)
        Converter.changed(self, what)