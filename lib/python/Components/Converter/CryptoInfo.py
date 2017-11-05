# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/CryptoInfo.py
# Compiled at: 2017-10-02 01:52:07
from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.config import config
from Tools.GetEcmInfo import GetEcmInfo
from Poll import Poll

class CryptoInfo(Poll, Converter, object):

    def __init__(self, type):
        Converter.__init__(self, type)
        Poll.__init__(self)
        self.type = type
        self.active = False
        if int(config.usage.show_cryptoinfo.value) > 0:
            self.visible = True
        else:
            self.visible = False
        self.textvalue = ''
        self.poll_interval = 1000
        self.poll_enabled = True
        self.ecmdata = GetEcmInfo()

    @cached
    def getText(self):
        if int(config.usage.show_cryptoinfo.value) < 1:
            self.visible = False
            data = ''
        else:
            self.visible = True
            if self.type == 'VerboseInfo':
                data = self.ecmdata.getEcmData()[0]
            else:
                data = self.ecmdata.getInfo(self.type)
        return data

    text = property(getText)