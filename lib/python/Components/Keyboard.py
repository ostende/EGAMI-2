# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Keyboard.py
# Compiled at: 2017-10-02 01:52:08
from Components.Console import Console
import os
import re
from enigma import eEnv

class Keyboard:

    def __init__(self):
        self.keyboardmaps = []
        self.kpath = eEnv.resolve('${datadir}/keymaps')
        eq = re.compile('^\\s*(\\w+)\\s*=\\s*(.*)\\s*$')
        for keymapfile in os.listdir(self.kpath):
            if keymapfile.endswith('.info'):
                mapfile = None
                mapname = None
                for line in open(os.path.join(self.kpath, keymapfile)):
                    m = eq.match(line)
                    if m:
                        key, val = m.groups()
                        if key == 'kmap':
                            mapfile = val
                        if key == 'name':
                            mapname = val
                        if mapfile is not None and mapname is not None:
                            self.keyboardmaps.append((mapfile, mapname))

        return

    def activateKeyboardMap(self, index):
        try:
            keymap = self.keyboardmaps[index]
            print '[Keyboard] Activating keymap:', keymap[1]
            keymappath = os.path.join(self.kpath, keymap[0])
            if os.path.exists(keymappath):
                Console().ePopen('loadkmap < ' + str(keymappath))
        except:
            print '[Keyboard] Selected keymap does not exist!'

    def getKeyboardMaplist(self):
        return self.keyboardmaps

    def getDefaultKeyboardMap(self):
        return 'default.kmap'


keyboard = Keyboard()