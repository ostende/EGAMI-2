# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/ScrollLabel.py
# Compiled at: 2017-10-02 01:52:08
import skin
from HTMLComponent import HTMLComponent
from GUIComponent import GUIComponent
from enigma import eLabeleWidgeteSliderfontRenderClassePointeSizeeTimer

class ScrollLabel(HTMLComponent, GUIComponent):

    def __init__(self, text=''):
        GUIComponent.__init__(self)
        self.step = 1
        self.steptime = 40
        self.startdelay = 3000
        self._position = ePoint(0, 0)
        self._size = eSize(0, 0)
        self.animation = False
        self.astartdelay = 3000
        self.aposition = ePoint(0, 0)
        self.asize = eSize(0, 0)
        self.message = text
        self.instance = None
        self.long_text = None
        self.right_text = None
        self.text_height = 0
        self.page_height = 0
        self.scrollbar = None
        self.pages = None
        self.total = None
        self.split = False
        self.splitchar = '|'
        self.column = 0
        self.lineheight = None
        self.scrollbarmode = 'showOnDemand'
        self.autoScroll = False
        self.updateTimer = eTimer()
        self.updateTimer.callback.append(self.lineScroll)
        self.aupdateTimer = eTimer()
        self.aupdateTimer.callback.append(self.animationLabel)
        self.onAnimationEnd = []
        self.onAnimationEnd.append(self._animationEnd)
        self.widget_attribs = []
        self.longtext_attribs = []
        self.scrollbar_attribs = []
        return

    def applySkin(self, desktop, parent):
        scrollbarWidth = 10
        itemHeight = 30
        scrollbarBorderWidth = 1
        ret = False
        if self.skinAttributes is not None:
            widget_attribs = []
            scrollbar_attribs = []
            remove_attribs = []
            for attrib, value in self.skinAttributes:
                if 'itemHeight' in attrib:
                    itemHeight = int(value)
                    remove_attribs.append((attrib, value))
                if 'scrollbarMode' in attrib:
                    self.scrollbarmode = value
                    remove_attribs.append((attrib, value))
                if 'borderColor' in attrib or 'borderWidth' in attrib:
                    scrollbar_attribs.append((attrib, value))
                if 'transparent' in attrib or 'backgroundColor' in attrib:
                    widget_attribs.append((attrib, value))
                if 'scrollbarSliderForegroundColor' in attrib:
                    scrollbar_attribs.append((attrib, value))
                    remove_attribs.append((attrib, value))
                if 'scrollbarSliderBorderColor' in attrib:
                    scrollbar_attribs.append((attrib, value))
                    remove_attribs.append((attrib, value))
                if 'scrollbarSliderPicture' in attrib:
                    scrollbar_attribs.append((attrib, value))
                    remove_attribs.append((attrib, value))
                if 'scrollbarBackgroundPicture' in attrib:
                    scrollbar_attribs.append((attrib, value))
                    remove_attribs.append((attrib, value))
                if 'scrollbarWidth' in attrib:
                    scrollbarWidth = int(value)
                    remove_attribs.append((attrib, value))
                if 'scrollbarSliderBorderWidth' in attrib:
                    scrollbarBorderWidth = int(value)
                    remove_attribs.append((attrib, value))
                if 'split' in attrib:
                    self.split = int(value)
                    if self.split:
                        self.right_text = eLabel(self.instance)
                if 'colposition' in attrib:
                    self.column = int(value)
                if 'dividechar' in attrib:
                    self.splitchar = value
                if attrib == 'step':
                    self.step = int(value)
                if attrib == 'steptime':
                    self.steptime = int(value)
                if attrib == 'position':
                    self._position = skin.parsePosition(value, ((1, 1), (1, 1)))
                    self.widget_attribs.append((attrib, value))
                if attrib == 'size':
                    self._size = skin.parseSize(value, ((1, 1), (1, 1)))
                    self.longtext_attribs.append((attrib, value))
                if 'startdelay' in attrib:
                    if value.startswith('config.'):
                        value = int(configfile.getResolvedKey(value)) * 1000
                    self.startdelay = int(value)
                if 'animation' in attrib:
                    self.animation = True
                if 'astartdelay' in attrib:
                    if value.startswith('config.'):
                        value = int(configfile.getResolvedKey(value)) * 1000
                    self.astartdelay = int(value)
                if 'aposition' in attrib:
                    self.aposition = skin.parsePosition(value, ((1, 1), (1, 1)))
                if 'asize' in attrib:
                    self.asize = skin.parseSize(value, ((1, 1), (1, 1)))
                if 'autoScroll' in attrib:
                    if value == '1' in attrib:
                        self.autoScroll = True
                    else:
                        self.autoScroll = False
                if attrib in ('borderColor', 'borderWidth', 'sliderLengthTip', 'sliderBackground',
                              'sliderForeground', 'sliderPointer'):
                    self.scrollbar_attribs.append((attrib, value))
                if attrib in ('font', 'transparent', 'foregroundColor', 'backgroundColor',
                              'valign', 'halign'):
                    self.longtext_attribs.append((attrib, value))

            for attrib, value in remove_attribs:
                self.skinAttributes.remove((attrib, value))

            if self.split:
                skin.applyAllAttributes(self.long_text, desktop, self.skinAttributes + [('halign', 'left')], parent.scale)
                skin.applyAllAttributes(self.right_text, desktop, self.skinAttributes + [('transparent', '1'), ('halign', 'left' and self.column or 'right')], parent.scale)
            else:
                skin.applyAllAttributes(self.long_text, desktop, self.skinAttributes, parent.scale)
            skin.applyAllAttributes(self.instance, desktop, widget_attribs, parent.scale)
            skin.applyAllAttributes(self.scrollbar, desktop, scrollbar_attribs + widget_attribs, parent.scale)
            ret = True
        s = self.long_text.size()
        self.instance.move(self._position)
        self.resize(self._size)
        self.lineheight = fontRenderClass.getInstance().getLineHeight(self.long_text.getFont())
        if not self.lineheight:
            self.lineheight = itemHeight
        lines = int(s.height() / self.lineheight)
        self.pageHeight = int(lines * self.lineheight)
        self.instance.resize(eSize(s.width(), self.pageHeight + int(self.lineheight / 6)))
        self.scrollbar.move(ePoint(s.width() - scrollbarWidth, 0))
        self.scrollbar.resize(eSize(scrollbarWidth, self.pageHeight + int(self.lineheight / 6)))
        self.scrollbar.setOrientation(eSlider.orVertical)
        self.scrollbar.setMode(eSlider.modeScrollbar)
        self.scrollbar.setRange(0, 100)
        self.scrollbar.setBorderWidth(scrollbarBorderWidth)
        self.long_text.move(ePoint(0, 0))
        self.long_text.resize(eSize(s.width() - 30, self.pageHeight))
        if self.split:
            self.right_text.move(ePoint(self.column, 0))
            self.right_text.resize(eSize(s.width() - self.column - 30, self.pageHeight))
        self.setText(self.message)
        return ret

    def setText(self, text):
        self.message = text
        if self.long_text is not None:
            self.long_text.move(ePoint(0, 0))
            if self.animation and self.astartdelay != 0:
                self.aupdateTimer.stop()
                self.instance.move(self._position)
                self.resize(self._size)
            if self.message is None:
                self.long_text.setText('')
                if self.animation:
                    self.long_text.hide()
                    self.hide()
            else:
                self.long_text.setText(self.message)
                if self.animation:
                    self.long_text.show()
                    self.show()
            self.page_height = int(self.instance.size().height())
            self.text_height = int(self.long_text.calculateSize().height() + fontRenderClass.getInstance().getLineHeight(self.long_text.getFont()))
            if self.scrollbarmode == 'showAlways' or self.scrollbarmode == 'showOnDemand':
                if self.autoScroll:
                    self.long_text.resize(eSize(self.instance.size().width(), self.text_height))
                    self.scrollbar.hide()
                    if self.text_height > self.page_height:
                        if self.animation and self.astartdelay != 0:
                            self.aupdateTimer.start(self.astartdelay, True)
                        else:
                            self.updateTimer.start(self.startdelay)
                    else:
                        self.updateTimer.stop()
                elif self.text_height > self.page_height:
                    self.long_text.resize(eSize(self.instance.size().width() - 20, self.text_height))
                    self.scrollbar.show()
                    self.updateScrollbar()
                else:
                    self.long_text.resize(eSize(self.instance.size().width(), self.text_height))
                    self.scrollbar.hide()
            else:
                self.long_text.resize(eSize(self.instance.size().width(), self.text_height))
                self.scrollbar.hide()
        return

    def appendText(self, text):
        old_text = self.getText()
        if old_text is not None and len(str(old_text)) > 0:
            self.message += text
        else:
            self.message = text
        if self.long_text is not None:
            self.long_text.move(ePoint(0, 0))
            if self.animation and self.astartdelay != 0:
                self.aupdateTimer.stop()
                self.instance.move(self._position)
                self.resize(self._size)
            if self.message is None:
                self.long_text.setText('')
                if self.animation:
                    self.long_text.hide()
                    self.hide()
            else:
                self.long_text.setText(self.message)
                if self.animation:
                    self.long_text.show()
                    self.show()
            self.page_height = int(self.instance.size().height())
            if self.scrollbarmode == 'showAlways' or self.scrollbarmode == 'showOnDemand':
                if self.autoScroll:
                    self.long_text.resize(eSize(self.instance.size().width(), self.text_height))
                    self.text_height = int(self.long_text.calculateSize().height() + fontRenderClass.getInstance().getLineHeight(self.long_text.getFont()))
                    self.scrollbar.hide()
                    if self.text_height > self.page_height:
                        if self.animation and self.astartdelay != 0:
                            self.aupdateTimer.start(self.astartdelay, True)
                        else:
                            self.updateTimer.start(self.startdelay)
                    else:
                        self.updateTimer.stop()
                else:
                    self.long_text.resize(eSize(self.instance.size().width(), self.text_height))
                    self.text_height = int(self.long_text.calculateSize().height() + fontRenderClass.getInstance().getLineHeight(self.long_text.getFont()))
                    if self.text_height > self.page_height:
                        self.long_text.resize(eSize(self.instance.size().width(), self.text_height))
                        self.text_height = int(self.long_text.calculateSize().height() + fontRenderClass.getInstance().getLineHeight(self.long_text.getFont()))
                        self.scrollbar.show()
                        self.updateScrollbar()
                    else:
                        self.scrollbar.hide()
            else:
                self.scrollbar.hide()
        return

    def updateScrollbar(self):
        if self.page_height == 0:
            self.scrollbar.hide()
            return
        total = self.text_height / self.page_height
        if self.text_height % self.page_height > 0:
            total += 1
        vis = 100 / total
        start = vis * -self.long_text.position().y() / self.page_height
        self.scrollbar.setStartEnd(start, start + vis)

    def getText(self):
        return self.message

    def GUIcreate(self, parent):
        self.instance = eWidget(parent)
        self.scrollbar = eSlider(self.instance)
        self.long_text = eLabel(self.instance)
        self.instance.animationEnd.get().append(self.animationEnd)

    def GUIdelete(self):
        self.instance.animationEnd.get().remove(self.animationEnd)
        self.long_text = None
        self.scrollbar = None
        self.instance = None
        return

    def animationEnd(self):
        for f in self.onAnimationEnd:
            f()

    def pageUp(self):
        if self.long_text is not None:
            if self.text_height > self.page_height:
                if self.updateTimer.isActive():
                    self.updateTimer.stop()
                if self.aupdateTimer.isActive():
                    self.aupdateTimer.stop()
                self.long_text.resize(eSize(self.instance.size().width() - 20, self.text_height))
                self.text_height = int(self.long_text.calculateSize().height() + fontRenderClass.getInstance().getLineHeight(self.long_text.getFont()))
                self.scrollbar.show()
                curPos = self.long_text.position()
                if curPos.y() < 0:
                    self.long_text.move(ePoint(curPos.x(), curPos.y() + self.page_height))
                    self.updateScrollbar()
        return

    def pageDown(self):
        if self.long_text is not None:
            if self.text_height > self.page_height:
                if self.updateTimer.isActive():
                    self.updateTimer.stop()
                if self.aupdateTimer.isActive():
                    self.aupdateTimer.stop()
                self.long_text.resize(eSize(self.instance.size().width() - 20, self.text_height))
                self.text_height = int(self.long_text.calculateSize().height() + fontRenderClass.getInstance().getLineHeight(self.long_text.getFont()))
                self.scrollbar.show()
                curPos = self.long_text.position()
                if self.text_height >= abs(curPos.y() - self.page_height):
                    self.long_text.move(ePoint(curPos.x(), curPos.y() - self.page_height))
                    self.updateScrollbar()
        return

    def lastPage(self):
        if self.page_height == 0:
            self.scrollbar.hide()
            return
        if self.updateTimer.isActive():
            self.updateTimer.stop()
        if self.aupdateTimer.isActive():
            self.aupdateTimer.stop()
        total = self.text_height / self.page_height
        if self.text_height % self.page_height > 0:
            total += 1
        i = 1
        while i < total:
            self.pageDown()
            self.updateScrollbar()
            i += 1

    def isAtLastPage(self):
        if self.total is not None:
            curPos = self.long_text.position()
            return self.total - self.pageHeight < abs(curPos.y() - self.pageHeight)
        else:
            return True
            return

    def produceHTML(self):
        return self.getText()

    def lineScroll(self):
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

    def _animationEnd(self):
        self.page_height = int(self.instance.size().height())
        self.text_height = int(self.long_text.calculateSize().height() + fontRenderClass.getInstance().getLineHeight(self.long_text.getFont()))
        self.long_text.resize(eSize(self.instance.size().width(), self.text_height))
        if self.text_height > self.page_height:
            self.updateTimer.start(self.startdelay)
        else:
            self.updateTimer.stop()