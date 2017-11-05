# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/MenuEntryCompare.py
# Compiled at: 2017-10-02 01:52:07
from Components.Converter.Converter import Converter
from Components.Element import cached

class MenuEntryCompare(Converter, object):

    def __init__(self, type):
        Converter.__init__(self, type)
        self.entry_id = type

    def selChanged(self):
        self.downstream_elements.changed((self.CHANGED_ALL, 0))

    @cached
    def getBool(self):
        id = self.entry_id
        cur = self.source.current
        if cur and len(cur) > 2:
            EntryID = cur[2]
            return EntryID and id and id == EntryID
        return False

    boolean = property(getBool)

    def changed(self, what):
        if what[0] == self.CHANGED_DEFAULT:
            self.source.onSelectionChanged.append(self.selChanged)
        Converter.changed(self, what)