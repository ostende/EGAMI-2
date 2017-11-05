# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/StaticMultiList.py
# Compiled at: 2017-10-02 01:52:07
from enigma import eListboxPythonMultiContent
from Components.Converter.StringList import StringList

class StaticMultiList(StringList):

    def changed(self, what):
        if not self.content:
            self.content = eListboxPythonMultiContent()
            if self.source:
                self.content.setItemHeight(self.source.item_height)
                index = 0
                for f in self.source.fonts:
                    self.content.setFont(index, f)
                    index += 1

        if self.source:
            self.content.setList(self.source.list)
        print 'downstream_elements:', self.downstream_elements
        self.downstream_elements.changed(what)