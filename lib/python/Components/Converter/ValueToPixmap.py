# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/ValueToPixmap.py
# Compiled at: 2017-10-02 01:52:07
from Components.Converter.Converter import Converter
from Components.Element import cachedElementError
from Tools.Directories import SCOPE_SKIN_IMAGESCOPE_ACTIVE_SKINresolveFilename
from Tools.LoadPixmap import LoadPixmap

class ValueToPixmap(Converter, object):
    LANGUAGE_CODE = 0
    PATH = 1

    def __init__(self, type):
        Converter.__init__(self, type)
        if type == 'LanguageCode':
            self.type = self.LANGUAGE_CODE
        elif type == 'Path':
            self.type = self.PATH
        else:
            raise ElementError("'%s' is not <LanguageCode|Path> for ValueToPixmap converter" % type)

    @cached
    def getPixmap(self):
        if self.source:
            val = self.source.text
            if val in (None, ''):
                return
        if self.type == self.PATH:
            return LoadPixmap(val)
        else:
            if self.type == self.LANGUAGE_CODE:
                png = LoadPixmap(cached=True, path=resolveFilename(SCOPE_ACTIVE_SKIN, 'countries/' + val[3:].lower() + '.png'))
                if png is None:
                    png = LoadPixmap(cached=True, path=resolveFilename(SCOPE_ACTIVE_SKIN, 'countries/' + val + '.png'))
                    if png is None:
                        png = LoadPixmap(cached=True, path=resolveFilename(SCOPE_ACTIVE_SKIN, 'countries/missing.png'))
                        if png is None:
                            png = LoadPixmap(cached=True, path=resolveFilename(SCOPE_SKIN_IMAGE, 'countries/missing.png'))
                return png
            return

    pixmap = property(getPixmap)

    def changed(self, what):
        if what[0] != self.CHANGED_SPECIFIC or what[1] == self.type:
            Converter.changed(self, what)