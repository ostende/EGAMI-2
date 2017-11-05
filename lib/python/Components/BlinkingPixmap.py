# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/BlinkingPixmap.py
# Compiled at: 2017-10-02 01:52:08
from Pixmap import PixmapConditional
from ConditionalWidget import BlinkingWidgetConditionalBlinkingWidget

class BlinkingPixmap(BlinkingWidget):

    def __init__(self):
        Widget.__init__(self)


class BlinkingPixmapConditional(BlinkingWidgetConditional, PixmapConditional):

    def __init__(self):
        BlinkingWidgetConditional.__init__(self)
        PixmapConditional.__init__(self)