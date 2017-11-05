# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Sources/HbbtvApplication.py
# Compiled at: 2017-10-02 01:52:07
from Source import Source
from Components.Element import cached

class HbbtvApplication(Source):

    def __init__(self):
        Source.__init__(self)
        self._available = False
        self._appname = ''
        self._useait = True

    def setApplicationName(self, name):
        self._appname = name
        self._available = False
        if name is not None and name != '':
            self._available = True
        self.changed((self.CHANGED_ALL,))
        return

    def getUseAit(self):
        return self._useait

    @cached
    def getBoolean(self):
        return self._available

    boolean = property(getBoolean)

    @cached
    def getName(self):
        return self._appname

    name = property(getName)