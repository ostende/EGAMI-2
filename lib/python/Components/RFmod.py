# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/RFmod.py
# Compiled at: 2017-10-02 01:52:08
from config import configConfigSelectionConfigSubsectionConfigOnOffConfigSliderConfigNothing
from enigma import eRFmod
from Components.SystemInfo import SystemInfo
RFMOD_CHANNEL_MIN = 21
RFMOD_CHANNEL_MAX = 70

class RFmod:

    def __init__(self):
        pass

    def setFunction(self, value):
        eRFmod.getInstance().setFunction(not value)

    def setTestmode(self, value):
        eRFmod.getInstance().setTestmode(value)

    def setSoundFunction(self, value):
        eRFmod.getInstance().setSoundFunction(not value)

    def setSoundCarrier(self, value):
        eRFmod.getInstance().setSoundCarrier(value)

    def setChannel(self, value):
        eRFmod.getInstance().setChannel(value)

    def setFinetune(self, value):
        eRFmod.getInstance().setFinetune(value)


def InitRFmod():
    detected = eRFmod.getInstance().detected()
    SystemInfo['RfModulator'] = detected
    config.rfmod = ConfigSubsection()
    if detected:
        config.rfmod.enable = ConfigOnOff(default=False)
        config.rfmod.test = ConfigOnOff(default=False)
        config.rfmod.sound = ConfigOnOff(default=True)
        config.rfmod.soundcarrier = ConfigSelection(choices=[('4500', '4.5 MHz'), ('5500', '5.5 MHz'), ('6000', '6.0 MHz'), ('6500', '6.5 MHz')], default='5500')
        config.rfmod.channel = ConfigSelection(default='36', choices=[ '%d' % x for x in range(RFMOD_CHANNEL_MIN, RFMOD_CHANNEL_MAX) ])
        config.rfmod.finetune = ConfigSlider(default=5, limits=(1, 10))
        iRFmod = RFmod()

        def setFunction(configElement):
            iRFmod.setFunction(configElement.value)

        def setTestmode(configElement):
            iRFmod.setTestmode(configElement.value)

        def setSoundFunction(configElement):
            iRFmod.setSoundFunction(configElement.value)

        def setSoundCarrier(configElement):
            iRFmod.setSoundCarrier(configElement.index)

        def setChannel(configElement):
            iRFmod.setChannel(int(configElement.value))

        def setFinetune(configElement):
            iRFmod.setFinetune(configElement.value - 5)

        config.rfmod.enable.addNotifier(setFunction)
        config.rfmod.test.addNotifier(setTestmode)
        config.rfmod.sound.addNotifier(setSoundFunction)
        config.rfmod.soundcarrier.addNotifier(setSoundCarrier)
        config.rfmod.channel.addNotifier(setChannel)
        config.rfmod.finetune.addNotifier(setFinetune)
    else:
        config.rfmod.enable = ConfigNothing()
        config.rfmod.test = ConfigNothing()
        config.rfmod.sound = ConfigNothing()
        config.rfmod.soundcarrier = ConfigNothing()
        config.rfmod.channel = ConfigNothing()
        config.rfmod.finetune = ConfigNothing()