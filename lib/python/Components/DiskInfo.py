# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/DiskInfo.py
# Compiled at: 2017-10-02 01:52:08
from GUIComponent import GUIComponent
from VariableText import VariableText
from os import statvfs
from enigma import eLabel

class DiskInfo(VariableText, GUIComponent):
    FREE = 0
    USED = 1
    SIZE = 2

    def __init__(self, path, type, update=True):
        GUIComponent.__init__(self)
        VariableText.__init__(self)
        self.type = type
        self.path = path
        if update:
            self.update()

    def update(self):
        try:
            stat = statvfs(self.path)
        except OSError:
            return -1

        if self.type == self.FREE:
            try:
                percent = '(' + str(100 * stat.f_bavail // stat.f_blocks) + '%)'
                free = stat.f_bfree * stat.f_bsize
                if free < 10000000:
                    free = _('%d kB') % (free >> 10)
                elif free < 10000000000:
                    free = _('%d MB') % (free >> 20)
                else:
                    free = _('%d Gb') % (free >> 30)
                self.setText(' '.join((free, percent, _('free diskspace'))))
            except:
                self.setText('-?-')

    GUI_WIDGET = eLabel