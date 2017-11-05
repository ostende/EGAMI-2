# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Renderer/NextEpgInfo.py
# Compiled at: 2017-10-02 01:52:08
from Components.VariableText import VariableText
from Renderer import Renderer
from enigma import eLabeleEPGCacheeServiceReference
from time import localtimestrftime

class NextEpgInfo(Renderer, VariableText):

    def __init__(self):
        Renderer.__init__(self)
        VariableText.__init__(self)
        self.epgcache = eEPGCache.getInstance()
        self.numberOfItems = 1

    GUI_WIDGET = eLabel

    def changed(self, what):
        self.text = ''
        reference = self.source.service
        info = reference and self.source.info
        if info:
            currentEvent = self.source.getCurrentEvent()
            if currentEvent:
                if not self.epgcache.startTimeQuery(eServiceReference(reference.toString()), currentEvent.getBeginTime() + currentEvent.getDuration()):
                    if self.numberOfItems == 1:
                        event = self.epgcache.getNextTimeEntry()
                        if event:
                            self.text = '%s: %s' % (pgettext("now/next: 'next' event label", 'Next'), event.getEventName())
                    else:
                        for x in range(self.numberOfItems):
                            event = self.epgcache.getNextTimeEntry()
                            if event:
                                self.text = '%s\n%s %s' % (self.text, strftime('%H:%M', localtime(event.getBeginTime())), event.getEventName())

                        self.text = self.text and '%s%s' % (pgettext("now/next: 'next' event label", 'Next'), self.text) or ''

    def applySkin(self, desktop, parent):
        for attrib, value in self.skinAttributes:
            if attrib == 'NumberOfItems':
                self.numberOfItems = int(value)
                self.skinAttributes.remove((attrib, value))

        return Renderer.applySkin(self, desktop, parent)