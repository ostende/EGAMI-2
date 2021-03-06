# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/PerServiceDisplay.py
# Compiled at: 2017-10-02 01:52:08
from GUIComponent import GUIComponent
from VariableText import VariableText
from VariableValue import VariableValue
from enigma import iPlayableService
from enigma import eLabeleSlidereTimer

class PerServiceBase(object):
    EventMap = {}

    @staticmethod
    def event(ev):
        func_list = PerServiceBase.EventMap.setdefault(ev, [])
        for func in func_list:
            if func[0]:
                func[1](ev)
            else:
                func[1]()

    def __init__(self, navcore, eventmap, with_event=False):
        self.navcore = navcore
        self.eventmap = eventmap
        self.poll_timer = eTimer()
        self.with_event = with_event
        self.poll_timer.callback.append(self.poll)
        EventMap = PerServiceBase.EventMap
        if not len(EventMap):
            self.navcore.event.append(PerServiceBase.event)
        EventMap = EventMap.setdefault
        for x in eventmap.iteritems():
            EventMap(x[0], []).append((with_event, x[1]))

        evEndEntry = eventmap.get(iPlayableService.evEnd)
        if evEndEntry:
            if with_event:
                evEndEntry(iPlayableService.evEnd)
            else:
                evEndEntry()

    def destroy(self):
        EventMap = PerServiceBase.EventMap.setdefault
        for x in self.eventmap.iteritems():
            EventMap(x[0], []).remove((self.with_event, x[1]))

    def enablePolling(self, interval=60000):
        if interval:
            self.poll_timer.start(interval)
        else:
            self.poll_timer.stop()

    def disablePolling(self):
        self.enablePolling(interval=0)

    def poll(self):
        pass


class PerServiceDisplay(PerServiceBase, VariableText, GUIComponent):

    def __init__(self, navcore, eventmap):
        GUIComponent.__init__(self)
        VariableText.__init__(self)
        PerServiceBase.__init__(self, navcore, eventmap)

    def destroy(self):
        PerServiceBase.destroy(self)
        GUIComponent.destroy(self)

    GUI_WIDGET = eLabel


class PerServiceDisplayProgress(PerServiceBase, VariableValue, GUIComponent):

    def __init__(self, navcore, eventmap):
        GUIComponent.__init__(self)
        VariableValue.__init__(self)
        PerServiceBase.__init__(self, navcore, eventmap)
        self.eventmap = eventmap
        self.navcore = navcore
        self.navcore.event.append(self.event)
        self.event(iPlayableService.evEnd)

    GUI_WIDGET = eSlider

    def destroy(self):
        PerServiceBase.destroy(self)
        GUIComponent.destroy(self)