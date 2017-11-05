# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Screens/TextBox.py
# Compiled at: 2017-10-02 01:52:09
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.ScrollLabel import ScrollLabel

class TextBox(Screen):

    def __init__(self, session, text='', title=None):
        Screen.__init__(self, session)
        self.text = text
        self['text'] = ScrollLabel(self.text)
        self['actions'] = ActionMap(['OkCancelActions', 'DirectionActions'], {'cancel': self.cancel,
           'ok': self.ok,
           'up': self['text'].pageUp,
           'down': self['text'].pageDown
           }, -1)
        if title:
            self.setTitle(title)

    def ok(self):
        self.close()

    def cancel(self):
        self.close()