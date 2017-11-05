# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Sources/Config.py
# Compiled at: 2017-10-02 01:52:07
from Source import Source

class Config(Source):

    def __init__(self, config):
        Source.__init__(self)
        self.__config = config

    def getConfig(self):
        return self.__config

    config = property(getConfig)

    def getHTML(self, id):
        print 'getHTML', self, id
        return self.__config.getHTML(id)

    def handleCommand(self, cmd):
        print 'ASSIGN:', cmd
        self.__config.unsafeAssign(cmd)