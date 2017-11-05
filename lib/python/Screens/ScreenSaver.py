# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Screens/ScreenSaver.py
# Compiled at: 2017-10-02 01:52:09
from Screens.Screen import Screen
from Components.MovieList import AUDIO_EXTENSIONS
from Components.ServiceEventTracker import ServiceEventTracker
from Components.Pixmap import Pixmap
from enigma import ePointeTimeriPlayableService
import os
import random

class Screensaver(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        self.moveLogoTimer = eTimer()
        self.moveLogoTimer.callback.append(self.doMovePicture)
        self.onShow.append(self.__onShow)
        self.onHide.append(self.__onHide)
        self.__event_tracker = ServiceEventTracker(screen=self, eventmap={iPlayableService.evStart: self.serviceStarted
           })
        self['picture'] = Pixmap()
        self.onLayoutFinish.append(self.layoutFinished)

    def layoutFinished(self):
        picturesize = self['picture'].getSize()
        self.maxx = self.instance.size().width() - picturesize[0]
        self.maxy = self.instance.size().height() - picturesize[1]
        self.doMovePicture()

    def __onHide(self):
        self.moveLogoTimer.stop()

    def __onShow(self):
        self.moveLogoTimer.startLongTimer(5)

    def serviceStarted(self):
        if self.shown:
            ref = self.session.nav.getCurrentlyPlayingServiceOrGroup()
            if ref:
                ref = ref.toString().split(':')
                if os.path.splitext(ref[10])[1].lower() not in AUDIO_EXTENSIONS:
                    self.hide()

    def doMovePicture(self):
        self.posx = random.randint(1, self.maxx)
        self.posy = random.randint(1, self.maxy)
        self['picture'].instance.move(ePoint(self.posx, self.posy))
        self.moveLogoTimer.startLongTimer(9)