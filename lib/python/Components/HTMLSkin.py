# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/HTMLSkin.py
# Compiled at: 2017-10-02 01:52:08


class HTMLSkin:
    order = ()

    def __init__(self, order):
        self.order = order

    def produceHTML(self):
        res = '<html>\n'
        for name in self.order:
            res += self[name].produceHTML()

        res += '</html>\n'
        return res