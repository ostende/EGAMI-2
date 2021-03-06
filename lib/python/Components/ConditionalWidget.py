# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/ConditionalWidget.py
# Compiled at: 2017-10-02 01:52:08
from GUIComponent import GUIComponent
from enigma import eTimer

class ConditionalWidget(GUIComponent):

    def __init__(self, withTimer=True):
        GUIComponent.__init__(self)
        self.setConnect(None)
        if withTimer:
            self.conditionCheckTimer = eTimer()
            self.conditionCheckTimer.callback.append(self.update)
            self.conditionCheckTimer.start(1000)
        return

    def postWidgetCreate(self, instance):
        self.visible = 0

    def setConnect(self, conditionalFunction):
        self.conditionalFunction = conditionalFunction

    def activateCondition(self, condition):
        if condition:
            self.visible = 1
        else:
            self.visible = 0

    def update(self):
        if self.conditionalFunction is not None:
            try:
                self.activateCondition(self.conditionalFunction())
            except:
                self.conditionalFunction = None
                self.activateCondition(False)

        return


class BlinkingWidget(GUIComponent):

    def __init__(self):
        GUIComponent.__init__(self)
        self.blinking = False
        self.setBlinkTime(500)
        self.timer = eTimer()
        self.timer.callback.append(self.blink)

    def setBlinkTime(self, time):
        self.blinktime = time

    def blink(self):
        if self.blinking:
            self.visible = not self.visible

    def startBlinking(self):
        self.blinking = True
        self.timer.start(self.blinktime)

    def stopBlinking(self):
        self.blinking = False
        if self.visible:
            self.hide()
        self.timer.stop()


class BlinkingWidgetConditional(BlinkingWidget, ConditionalWidget):

    def __init__(self):
        BlinkingWidget.__init__(self)
        ConditionalWidget.__init__(self)

    def activateCondition(self, condition):
        if condition:
            if not self.blinking:
                self.startBlinking()
        elif self.blinking:
            self.stopBlinking()