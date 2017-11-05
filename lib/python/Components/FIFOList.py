# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/FIFOList.py
# Compiled at: 2017-10-02 01:52:08
from Components.MenuList import MenuList

class FIFOList(MenuList):

    def __init__(self, menulist=None, length=10):
        if not menulist:
            menulist = []
        self.list = menulist
        self.len = length
        MenuList.__init__(self, self.list)

    def addItem(self, item):
        self.list.append(item)
        self.l.setList(self.list[-self.len:])

    def clear(self):
        del self.list[:]
        self.l.setList(self.list)

    def getCurrentSelection(self):
        return self.list and self.getCurrent() or None

    def listAll(self):
        self.l.setList(self.list)
        self.selectionEnabled(True)