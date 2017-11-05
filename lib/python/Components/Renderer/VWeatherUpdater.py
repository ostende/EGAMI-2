# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Renderer/VWeatherUpdater.py
# Compiled at: 2017-10-02 01:52:08
from Renderer import Renderer
from enigma import eLabel

class VWeatherUpdater(Renderer):

    def __init__(self):
        Renderer.__init__(self)

    GUI_WIDGET = eLabel