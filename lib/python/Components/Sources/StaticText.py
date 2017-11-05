# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Sources/StaticText.py
# Compiled at: 2017-10-02 01:52:07
from Source import Source

class StaticText(Source):

    def __init__(self, text='', filter=lambda x: x):
        Source.__init__(self)
        self.__text = text
        self.filter = filter

    def handleCommand(self, cmd):
        self.text = self.filter(cmd)

    def getText(self):
        return self.__text

    def setText(self, text):
        self.__text = text
        self.changed((self.CHANGED_ALL,))

    text = property(getText, setText)