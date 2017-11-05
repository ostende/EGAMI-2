# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Sources/Source.py
# Compiled at: 2017-10-02 01:52:07
from Components.Element import Element

class Source(Element):

    def execBegin(self):
        pass

    def execEnd(self):
        pass

    def onShow(self):
        pass

    def onHide(self):
        pass

    def destroy(self):
        self.__dict__.clear()

    boolean = True


class ObsoleteSource(Source):

    def __init__(self, new_source, description=None, removal_date='as soon as possible'):
        self.new_source = new_source
        self.description = description
        self.removal_date = removal_date