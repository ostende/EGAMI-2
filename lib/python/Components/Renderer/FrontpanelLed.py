# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Renderer/FrontpanelLed.py
# Compiled at: 2017-10-02 01:52:08
from Components.Element import Element
from os import path

class FrontpanelLed(Element):

    def __init__(self, which=0, patterns=None, boolean=True):
        if not patterns:
            patterns = [(20, 0, 4294967295), (20, 1431655765, 2231143428)]
        self.which = which
        self.boolean = boolean
        self.patterns = patterns
        Element.__init__(self)

    def changed(self, *args, **kwargs):
        if self.boolean:
            val = self.source.boolean and 0 or 1
        else:
            val = self.source.value
        speed, pattern, pattern_4bit = self.patterns[val]
        if path.exists('/proc/stb/fp/led%d_pattern' % self.which):
            f = open('/proc/stb/fp/led%d_pattern' % self.which, 'w')
            f.write('%08x' % pattern)
            f.close()
        if self.which == 0:
            if path.exists('/proc/stb/fp/led_set_pattern'):
                f = open('/proc/stb/fp/led_set_pattern', 'w')
                f.write('%08x' % pattern_4bit)
                f.close()
            if path.exists('/proc/stb/fp/led_set_speed'):
                f = open('/proc/stb/fp/led_set_speed', 'w')
                f.write('%d' % speed)
                f.close()
            if path.exists('/proc/stb/fp/led_pattern_speed'):
                f = open('/proc/stb/fp/led_pattern_speed', 'w')
                f.write('%d' % speed)
                f.close()