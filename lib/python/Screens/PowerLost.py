# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Screens/PowerLost.py
# Compiled at: 2017-10-02 01:52:09
from Screen import Screen
from MessageBox import MessageBox
from Components.config import config
import Screens.Standby
from boxbranding import getMachineBrandgetMachineName

class PowerLost(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        self.showMessageBox()

    def showMessageBox(self):
        if config.usage.boot_action.value == 'normal':
            message = _('Your %s %s was not shutdown properly.\n\nDo you want to put it in %s?') % (
             getMachineBrand(), getMachineName(), config.usage.shutdownNOK_action.value)
            self.session.openWithCallback(self.MsgBoxClosed, MessageBox, message, MessageBox.TYPE_YESNO, timeout=60, default=True)
        else:
            self.MsgBoxClosed(True)

    def MsgBoxClosed(self, ret):
        if ret:
            if config.usage.shutdownNOK_action.value == 'deepstandby' and not config.usage.shutdownOK.value:
                self.session.open(Screens.Standby.TryQuitMainloop, 1)
            elif not Screens.Standby.inStandby:
                self.session.open(Screens.Standby.Standby)
        self.close()