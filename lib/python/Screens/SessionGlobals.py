# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Screens/SessionGlobals.py
# Compiled at: 2017-10-02 01:52:09
from Screens.Screen import Screen
from Components.Sources.Clock import Clock
from Components.Sources.CurrentService import CurrentService
from Components.Sources.EventInfo import EventInfo
from Components.Sources.FrontendStatus import FrontendStatus
from Components.Sources.FrontendInfo import FrontendInfo
from Components.Sources.Source import Source
from Components.Sources.TunerInfo import TunerInfo
from Components.Sources.Boolean import Boolean
from Components.Sources.RecordState import RecordState
from Components.Converter.Combine import Combine
from Components.Renderer.FrontpanelLed import FrontpanelLed
from boxbranding import getBoxType

class SessionGlobals(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        self['CurrentService'] = CurrentService(session.nav)
        self['CurrentTime'] = Clock()
        self['Event_Now'] = EventInfo(session.nav, EventInfo.NOW)
        self['Event_Next'] = EventInfo(session.nav, EventInfo.NEXT)
        self['FrontendStatus'] = FrontendStatus(service_source=session.nav.getCurrentService)
        self['FrontendInfo'] = FrontendInfo(navcore=session.nav)
        self['VideoPicture'] = Source()
        self['TunerInfo'] = TunerInfo()
        self['RecordState'] = RecordState(session)
        self['Standby'] = Boolean(fixed=False)
        from Components.SystemInfo import SystemInfo
        combine = Combine(func=lambda s: {(False, False): 0,(False, True): 1,(True, False): 2,(True, True): 3}[s[0].boolean, s[1].boolean])
        combine.connect(self['Standby'])
        combine.connect(self['RecordState'])
        PATTERN_ON = (20, 4294967295, 4294967295)
        PATTERN_OFF = (20, 0, 0)
        PATTERN_BLINK = (20, 1431655765, 2818363258)
        have_display = SystemInfo.get('FrontpanelDisplay', False)
        have_touch_sensor = SystemInfo.get('HaveTouchSensor', False)
        nr_leds = SystemInfo.get('NumFrontpanelLEDs', 0)
        if nr_leds == 1:
            FrontpanelLed(which=0, boolean=False, patterns=[PATTERN_OFF if have_display else PATTERN_ON, PATTERN_BLINK, PATTERN_OFF, PATTERN_BLINK]).connect(combine)
        elif nr_leds == 2:
            if have_touch_sensor:
                FrontpanelLed(which=0, boolean=False, patterns=[PATTERN_ON, PATTERN_BLINK, PATTERN_OFF, PATTERN_BLINK]).connect(combine)
                FrontpanelLed(which=1, boolean=False, patterns=[PATTERN_OFF, PATTERN_OFF, PATTERN_OFF, PATTERN_OFF]).connect(combine)
            else:
                FrontpanelLed(which=0, boolean=False, patterns=[PATTERN_OFF, PATTERN_BLINK, PATTERN_ON, PATTERN_BLINK]).connect(combine)
                FrontpanelLed(which=1, boolean=False, patterns=[PATTERN_ON, PATTERN_ON, PATTERN_OFF, PATTERN_OFF]).connect(combine)