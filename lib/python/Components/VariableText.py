# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/VariableText.py
# Compiled at: 2017-10-02 01:52:08


class VariableText(object):

    def __init__(self):
        object.__init__(self)
        self.message = ''
        self.instance = None
        return

    def setText(self, text):
        try:
            self.message = text
            if self.instance:
                self.instance.setText(self.message or '')
        except:
            self.message = ''
            self.instance.setText(self.message or '')

    def setMarkedPos(self, pos):
        if self.instance:
            self.instance.setMarkedPos(int(pos))

    def getText(self):
        return self.message

    text = property(getText, setText)

    def postWidgetCreate(self, instance):
        try:
            instance.setText(self.message or '')
        except:
            pass