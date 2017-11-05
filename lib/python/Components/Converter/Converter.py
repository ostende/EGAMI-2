# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/Converter.py
# Compiled at: 2017-10-02 01:52:07
from Components.Element import Element

class Converter(Element):

    def __init__(self, arguments):
        Element.__init__(self)
        self.converter_arguments = arguments

    def __repr__(self):
        return str(type(self)) + '(' + self.converter_arguments + ')'

    def handleCommand(self, cmd):
        self.source.handleCommand(cmd)