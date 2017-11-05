# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Sources/CanvasSource.py
# Compiled at: 2017-10-02 01:52:07
from Source import Source

class CanvasSource(Source):

    def __init__(self):
        Source.__init__(self)
        self.sequence = 0
        self.clear()

    def clear(self):
        self.sequence += 1
        self._drawlist = (self.sequence, [])

    def get_drawlist(self):
        return self._drawlist

    drawlist = property(get_drawlist)

    def fill(self, x, y, width, height, color):
        self.drawlist[1].append((1, x, y, width, height, color))

    def writeText(self, x, y, width, height, fg, bg, font, text, flags=0):
        self.drawlist[1].append((2, x, y, width, height, fg, bg, font, text, flags))

    def line(self, x0, y0, x1, y1, color):
        self.drawlist[1].append((3, x0, y0, x1, y1, color))

    def rline(self, ox, oy, x0, y0, x1, y1, angle, clockwise, color):
        self.drawlist[1].append((4, ox, oy, x0, y0, x1, y1, angle, clockwise, color))

    def flush(self):
        self.changed((self.CHANGED_DEFAULT,))