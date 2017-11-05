# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Renderer/ScrollLabel.py
# Compiled at: 2017-10-02 01:52:08
from skin import applyAllAttributesparsePositionparseSize
from Components.VariableText import VariableText
from Components.config import configfile
from Renderer import Renderer
from enigma import eLabeleSlidereWidgetePointeSizegFontfontRenderClasseTimer

class ScrollLabel(VariableText, Renderer):

    def __init__(self):
        Renderer.__init__(self)
        VariableText.__init__(self)
        self.step = 1
        self.steptime = 40
        self.startdelay = 3000
        self._position = ePoint(0, 0)
        self._size = eSize(0, 0)
        self.astartdelay = 3000
        self.aposition = ePoint(0, 0)
        self.asize = ePoint(0, 0)
        self.scrolldelay = 3000
        self.message = ''
        self.long_text = None
        self.text_height = 0
        self.page_height = 0
        self.scrollbar = None
        self.autoScroll = True
        self.scrollbarmode = 'shownever'
        self.sliderlengthtip = 0
        self.valignbottom = False
        self.animationScreen = False
        self.animationLongText = False
        self.scrollbarTimer = eTimer()
        self.scrollbarTimer.callback.append(self.scrollbarHide)
        self.updateTimer = eTimer()
        self.updateTimer.callback.append(self.scrollLine)
        self.aupdateTimer = eTimer()
        self.aupdateTimer.callback.append(self.animationLabel)
        self.onAnimationEnd = []
        self.onAnimationEnd.append(self._animationEnd)
        self.widget_attribs = []
        self.longtext_attribs = []
        self.scrollbar_attribs = []
        return

    def postWidgetCreate(self, instance):
        self.long_text = eLabel(instance)
        self.long_text.animationEnd.get().append(self.animationEnd)
        self.scrollbar = eSlider(instance)
        instance.animationEnd.get().append(self.animationEnd)

    def preWidgetRemove(self, instance):
        self.long_text.animationEnd.get().remove(self.animationEnd)
        instance.animationEnd.get().remove(self.animationEnd)
        self.long_text = None
        self.scrollbar = None
        return

    def spreadSingleAttribute(self, skinAttributes):
        for attrib, value in skinAttributes:
            if attrib == 'step':
                self.step = int(value)
            elif attrib == 'steptime':
                self.steptime = int(value)
            elif attrib == 'position':
                self._position = parsePosition(value, ((1, 1), (1, 1)))
                self.widget_attribs.append((attrib, value))
            elif attrib == 'size':
                self._size = parseSize(value, ((1, 1), (1, 1)))
                self.longtext_attribs.append((attrib, value))
            elif attrib == 'startdelay':
                if value.startswith('config.'):
                    value = int(configfile.getResolvedKey(value)) * 1000
                self.startdelay = int(value)
            elif attrib == 'animation':
                self.animationScreen = True
            elif attrib == 'astartdelay':
                if value.startswith('config.'):
                    value = int(configfile.getResolvedKey(value)) * 1000
                self.astartdelay = int(value)
            elif attrib == 'aposition':
                self.aposition = parsePosition(value, ((1, 1), (1, 1)))
            elif attrib == 'asize':
                self.asize = parseSize(value, ((1, 1), (1, 1)))
            elif attrib == 'autoScroll':
                self.autoScroll = value == '1'
            elif attrib == 'align':
                if 'bottom' in value.split(','):
                    self.valignbottom = True
                self.longtext_attribs.append((attrib, value))
            elif attrib == 'valign':
                if 'bottom' in value.split(','):
                    self.valignbottom = True
                self.longtext_attribs.append((attrib, value))
            elif attrib == 'scrollbarMode':
                self.scrollbarmode = value.lower()
            elif attrib == 'sliderLengthTip':
                self.sliderlengthtip = int(value)
                self.scrollbar_attribs.append((attrib, value))
            elif attrib in ('borderColor', 'borderWidth', 'sliderBackground', 'sliderForeground',
                            'sliderPointer'):
                self.scrollbar_attribs.append((attrib, value))
            elif attrib in ('font', 'transparent', 'foregroundColor', 'backgroundColor',
                            'halign'):
                self.longtext_attribs.append((attrib, value))
            elif attrib == 'css':
                from skin import cascadingStyleSheets
                styles = value.split(',')
                for style in styles:
                    for _attrib in cascadingStyleSheets[style].keys():
                        _value = cascadingStyleSheets[style][_attrib]
                        self.spreadSingleAttribute([(_attrib, _value)])

            else:
                self.widget_attribs.append((attrib, value))

    def applySkin(self, desktop, parent):
        ret = False
        if self.skinAttributes is not None:
            self.spreadSingleAttribute(self.skinAttributes)
            applyAllAttributes(self.instance, desktop, self.widget_attribs, parent.scale)
            applyAllAttributes(self.long_text, desktop, self.longtext_attribs, parent.scale)
            applyAllAttributes(self.scrollbar, desktop, self.scrollbar_attribs + self.widget_attribs, parent.scale)
            ret = True
        self.instance.move(self._position)
        self.resize(self._size)
        self.long_text.move(ePoint(0, 0))
        self.scrollbar.move(ePoint(self._size.width() - self.sliderlengthtip * 2, 1))
        self.scrollbar.resize(eSize(self.sliderlengthtip * 2, self._size.height() - 2))
        self.scrollbar.setOrientation(eSlider.orVertical)
        self.scrollbar.setMode(eSlider.modeScrollbar)
        self.scrollbar.setRange(0, 1000)
        self.scrollbar.hide()
        self.changed((self.CHANGED_DEFAULT,))
        return ret

    GUI_WIDGET = eWidget

    def connect(self, source):
        Renderer.connect(self, source)
        self.changed((self.CHANGED_DEFAULT,))

    def changed(self, what):
        if what[0] == self.CHANGED_CLEAR:
            if self.long_text is not None:
                self.long_text.move(ePoint(0, 0))
                if self.animationScreen and self.astartdelay != 0:
                    self.aupdateTimer.stop()
                    self.instance.move(self._position)
                    self.resize(self._size)
                    self.long_text.hide()
                    self.scrollbar.hide()
                    self.hide()
                self.message = ''
                self.long_text.setText('')
                self.long_text.resize(self.instance.size())
                self.updateTimer.stop()
        elif self.long_text is not None:
            if self.source.text is None:
                self.message = ''
                self.long_text.setText('')
                self.long_text.hide()
                self.scrollbar.hide()
                self.hide()
            else:
                if self.message == self.source.text:
                    return
                self.message = self.source.text
                self.long_text.setText(self.source.text)
                self.long_text.show()
                self.show()
            if self.animationScreen and self.astartdelay != 0:
                self.aupdateTimer.stop()
                self.instance.move(self._position)
                self.resize(self._size)
            self.page_height = int(self.instance.size().height())
            self.text_height = int(self.long_text.calculateSize().height() + fontRenderClass.getInstance().getLineHeight(self.long_text.getFont()))
            if self.text_height > self.page_height:
                self.long_text.resize(eSize(self.instance.size().width(), self.text_height))
                if self.autoScroll:
                    self.long_text.move(ePoint(0, 0))
                    if self.animationScreen and self.astartdelay != 0:
                        self.aupdateTimer.start(self.astartdelay, True)
                    else:
                        self.updateTimer.start(self.startdelay)
                elif self.valignbottom:
                    self.long_text.move(ePoint(0, self.page_height - self.text_height))
            else:
                self.long_text.move(ePoint(0, 0))
                self.long_text.resize(eSize(self.instance.size().width(), self.instance.size().height()))
                self.updateTimer.stop()
            self.updateScrollbar()
        return

    def scrollbarHide(self):
        self.scrollbar.hide()

    def updateScrollbar(self):
        if self.autoScroll or self.text_height < self.page_height or self.page_height == 0 or self.scrollbarmode == 'shownever':
            self.scrollbar.hide()
            return
        self.scrollbar.show()
        vlen = self.page_height * 1000 / self.text_height
        start = -self.long_text.position().y() * 1000 / self.text_height
        end = start + vlen
        if start < 0:
            start = 0
        if end > 1000:
            end = 1000
        self.scrollbar.setStartEnd(start, end)
        if self.scrollbarmode == 'showondemand':
            self.scrollbarTimer.stop()
            if self.scrolldelay > 0:
                self.scrollbarTimer.start(self.scrolldelay, True)

    def pageUp(self):
        self.scrollPageUp()

    def scrollPageUp(self):
        if self.long_text is not None and self.text_height > self.page_height:
            curPos = self.long_text.position()
            if curPos.y() + self.page_height > 0:
                offset = self.step
            else:
                offset = curPos.y() + self.page_height
            newPos = ePoint(curPos.x(), offset)
            self.animationLongText = True
            self.long_text.startMoveAnimation(newPos, 5, 1, 1)
        return

    def pageDown(self):
        self.scrollPageDown()

    def scrollPageDown(self):
        if self.long_text is not None and self.text_height > self.page_height:
            curPos = self.long_text.position()
            if curPos.y() + self.text_height - self.page_height < self.page_height:
                offset = self.page_height - self.text_height - self.step
            else:
                offset = curPos.y() - self.page_height
            newPos = ePoint(curPos.x(), offset)
            self.animationLongText = True
            self.long_text.startMoveAnimation(newPos, 5, 1, 1)
        return

    def up(self):
        self.scrollUp()

    def scrollUp(self):
        if self.long_text is not None and self.text_height > self.page_height:
            curPos = self.long_text.position()
            newPos = ePoint(curPos.x(), curPos.y() + self.step)
            self.animationLongText = True
            self.long_text.startMoveAnimation(newPos, 5, 1, 1)
        return

    def down(self):
        self.scrollDown()

    def scrollDown(self):
        if self.long_text is not None and self.text_height > self.page_height:
            curPos = self.long_text.position()
            newPos = ePoint(curPos.x(), curPos.y() - self.step)
            self.animationLongText = True
            self.long_text.startMoveAnimation(newPos, 5, 1, 1)
        return

    def scrollLine(self):
        if self.long_text is not None:
            if self.text_height > self.page_height:
                curPos = self.long_text.position()
                if self.text_height - self.step >= abs(curPos.y() - self.step):
                    self.long_text.move(ePoint(curPos.x(), curPos.y() - self.step))
                else:
                    self.long_text.move(ePoint(curPos.x(), self.page_height))
                self.updateTimer.start(self.steptime)
            else:
                self.updateTimer.stop()
        return

    def animationLabel(self):
        self.instance.startMoveAnimation(self.aposition, self.asize, 15, 10, 1)

    def animationEnd(self):
        for f in self.onAnimationEnd:
            f()

        return 0

    def _animationEnd(self):
        if self.autoScroll:
            self.page_height = int(self.instance.size().height())
            self.text_height = int(self.long_text.calculateSize().height() + fontRenderClass.getInstance().getLineHeight(self.long_text.getFont()))
            self.long_text.resize(eSize(self.instance.size().width(), self.text_height))
            self.updateScrollbar()
            if self.text_height > self.page_height:
                self.updateTimer.start(self.startdelay)
            else:
                self.updateTimer.stop()
        elif self.animationLongText:
            self.updateScrollbar()
            self.animationLongText = False
            curPos = self.long_text.position()
            if curPos.y() > 0:
                newPos = ePoint(curPos.x(), 0)
                self.long_text.startMoveAnimation(newPos, 5, 1, 1)
            elif curPos.y() + self.text_height < self.page_height:
                newPos = ePoint(curPos.x(), self.page_height - self.text_height)
                self.long_text.startMoveAnimation(newPos, 5, 1, 1)