# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Screens/FactoryReset.py
# Compiled at: 2017-10-02 01:52:09
from boxbranding import getMachineBrandgetMachineName
from Screens.MessageBox import MessageBox
from Screens.ParentalControlSetup import ProtectedScreen
from Components.config import config

class FactoryReset(MessageBox, ProtectedScreen):

    def __init__(self, session):
        MessageBox.__init__(self, session, _('When you perform a factory reset, you will lose ALL of your configuration data\n(including bouquets, services, satellite data ...)\nAfter completion of the factory reset, your %s %s will restart automatically!\n\nDo you really want to do a factory reset?') % (
         getMachineBrand(), getMachineName()), MessageBox.TYPE_YESNO, default=False)
        self.setTitle(_('Factory reset'))
        self.skinName = 'MessageBox'
        ProtectedScreen.__init__(self)

    def isProtected(self):
        return config.ParentalControl.setuppinactive.value and (not config.ParentalControl.config_sections.main_menu.value and not config.ParentalControl.config_sections.configuration.value or hasattr(self.session, 'infobar') and self.session.infobar is None) and config.ParentalControl.config_sections.manufacturer_reset.value