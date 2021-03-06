# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/ConditionalShowHide.py
# Compiled at: 2017-10-02 01:52:07
from enigma import eTimer
from Converter import Converter

class ConditionalShowHide(Converter, object):

    def __init__(self, argstr):
        Converter.__init__(self, argstr)
        args = argstr.split(',')
        self.invert = 'Invert' in args
        self.blink = 'Blink' in args
        if self.blink:
            self.blinktime = len(args) == 2 and args[1].isdigit() and int(args[1]) or 500
            self.timer = eTimer()
            self.timer.callback.append(self.blinkFunc)
        else:
            self.timer = None
        return

    def blinkFunc(self):
        if self.blinking:
            for x in self.downstream_elements:
                x.visible = not x.visible

    def startBlinking(self):
        self.blinking = True
        self.timer.start(self.blinktime)

    def stopBlinking(self):
        self.blinking = False
        for x in self.downstream_elements:
            if x.visible:
                x.hide()

        self.timer.stop()

    def calcVisibility(self):
        b = self.source.boolean
        if b is None:
            b = False
        b ^= self.invert
        return b

    def changed(self, what):
        vis = self.calcVisibility()
        if self.blink:
            if vis:
                self.startBlinking()
            else:
                self.stopBlinking()
        else:
            for x in self.downstream_elements:
                x.visible = vis

    def connectDownstream(self, downstream):
        Converter.connectDownstream(self, downstream)
        vis = self.calcVisibility()
        if self.blink:
            if vis:
                self.startBlinking()
            else:
                self.stopBlinking()
        else:
            downstream.visible = self.calcVisibility()

    def destroy(self):
        if self.timer:
            self.timer.callback.remove(self.blinkFunc)