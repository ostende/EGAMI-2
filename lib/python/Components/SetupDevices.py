# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/SetupDevices.py
# Compiled at: 2017-10-02 01:52:08
from config import configConfigSelectionConfigSubsectionConfigOnOffConfigText
from boxbranding import getBrandOEMgetMachineBrand
from Components.Timezones import timezones
from Components.Keyboard import keyboard
from boxbranding import getMachineBrand

def InitSetupDevices():

    def timezoneNotifier(configElement):
        timezones.activateTimezone(configElement.index)

    config.timezone = ConfigSubsection()
    config.timezone.val = ConfigSelection(default=timezones.getDefaultTimezone(), choices=timezones.getTimezoneList())
    config.timezone.val.addNotifier(timezoneNotifier)

    def keyboardNotifier(configElement):
        keyboard.activateKeyboardMap(configElement.index)

    config.keyboard = ConfigSubsection()
    config.keyboard.keymap = ConfigSelection(default=keyboard.getDefaultKeyboardMap(), choices=keyboard.getKeyboardMaplist())
    config.keyboard.keymap.addNotifier(keyboardNotifier)
    config.parental = ConfigSubsection()
    config.parental.lock = ConfigOnOff(default=False)
    config.parental.setuplock = ConfigOnOff(default=False)
    config.expert = ConfigSubsection()
    config.expert.satpos = ConfigOnOff(default=True)
    config.expert.fastzap = ConfigOnOff(default=True)
    config.expert.skipconfirm = ConfigOnOff(default=False)
    config.expert.hideerrors = ConfigOnOff(default=False)
    config.expert.autoinfo = ConfigOnOff(default=True)