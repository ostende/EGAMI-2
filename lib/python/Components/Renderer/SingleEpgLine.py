# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Renderer/SingleEpgLine.py
# Compiled at: 2017-10-02 01:52:08
from Components.VariableText import VariableText
from enigma import eLabeleEPGCache
from Renderer import Renderer
from time import localtime

class SingleEpgLine(Renderer, VariableText):

    def __init__(self):
        Renderer.__init__(self)
        VariableText.__init__(self)
        self.epgcache = eEPGCache.getInstance()

    GUI_WIDGET = eLabel

    def changed(self, what):
        event = self.source.event
        if event is None:
            self.text = ''
            return
        else:
            service = self.source.service
            text = ''
            evt = None
            if self.epgcache is not None:
                evt = self.epgcache.lookupEvent(['IBDCT', (service.toString(), 0, -1, -1)])
            if evt:
                maxx = 0
                for x in evt:
                    if maxx > 0:
                        if x[4]:
                            t = localtime(x[1])
                            text = text + '%02d:%02d %s | ' % (t[3], t[4], x[4])
                        else:
                            text = text + 'n/a | '
                    maxx += 1
                    if maxx > 7:
                        break

            self.text = text
            return