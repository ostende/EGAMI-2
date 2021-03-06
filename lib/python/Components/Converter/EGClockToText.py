# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/EGClockToText.py
# Compiled at: 2017-10-02 01:52:07
from Converter import Converter
from time import localtimestrftime
from Components.Element import cached
from Components.config import *
from Components.ConfigList import *

class EGClockToText(Converter, object):
    DEFAULT = 0
    WITH_SECONDS = 1
    IN_MINUTES = 2
    DATE = 3
    FORMAT = 4
    AS_LENGTH = 5
    TIMESTAMP = 6

    def __init__(self, type):
        Converter.__init__(self, type)
        if type == 'WithSeconds':
            self.type = self.WITH_SECONDS
        elif type == 'InMinutes':
            self.type = self.IN_MINUTES
        elif type == 'Date':
            self.type = self.DATE
        elif type == 'AsLength':
            self.type = self.AS_LENGTH
        elif type == 'Timestamp':
            self.type = self.TIMESTAMP
        elif str(type).find('Format') != -1:
            self.type = self.FORMAT
            self.fmt_string = type[7:]
        else:
            self.type = self.DEFAULT

    @cached
    def getText(self):
        time = self.source.time
        if time is None:
            return ''
        else:
            if self.type == self.IN_MINUTES:
                return '%d min' % (time / 60)
            if self.type == self.AS_LENGTH:
                return '%d:%02d' % (time / 60, time % 60)
            if self.type == self.TIMESTAMP:
                return str(time)
            t = localtime(time)
            if self.type == self.WITH_SECONDS:
                return '%2d:%02d:%02d' % (t.tm_hour, t.tm_min, t.tm_sec)
            if self.type == self.DEFAULT:
                return '%02d:%02d' % (t.tm_hour, t.tm_min)
            if self.type == self.DATE:
                dateFormat = config.infobar.dateformat.value
                a = _('January') + _('February') + _('March') + _('April') + _('May') + _('June')
                b = _('July') + _('August') + _('September') + _('October') + _('November') + _('December')
                if dateFormat == 'DDNNMMYY':
                    return strftime(_(strftime('%A', t)) + ' ' + _(strftime('%d', t)) + ' ' + _(strftime('%B', t)) + ' ' + _(strftime('%Y', t)))
                if dateFormat == 'NNMMYY':
                    return strftime(_(strftime('%d', t)) + ' ' + _(strftime('%B', t)) + ' ' + _(strftime('%Y', t)))
                if dateFormat == 'MMNNYY':
                    return strftime(_(strftime('%B', t)) + ' ' + _(strftime('%d', t)) + ' ' + _(strftime('%Y', t)))
                if dateFormat == 'MMNNDDYY':
                    return strftime(_(strftime('%B', t)) + ' ' + _(strftime('%d', t)) + ' ' + _(strftime('%A', t)) + ' ' + _(strftime('%Y', t)))
            elif self.type == self.FORMAT:
                spos = self.fmt_string.find('%')
                if spos > 0:
                    s1 = self.fmt_string[:spos]
                    s2 = strftime(self.fmt_string[spos:], t)
                    return str(s1 + s2)
                else:
                    return strftime(self.fmt_string, t)

            else:
                return '???'
            return

    text = property(getText)