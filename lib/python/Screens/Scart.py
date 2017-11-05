# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Screens/Scart.py
# Compiled at: 2017-10-02 01:52:09
from Screen import Screen
from MessageBox import MessageBox
from Components.AVSwitch import AVSwitch
from Tools import Notifications

class Scart(Screen):

    def __init__(self, session, start_visible=True):
        Screen.__init__(self, session)
        self.msgBox = None
        self.notificationVisible = None
        self.avswitch = AVSwitch()
        if start_visible:
            self.onExecBegin.append(self.showMessageBox)
            self.msgVisible = None
        else:
            self.msgVisible = False
        return

    def showMessageBox(self):
        if self.msgVisible is None:
            self.onExecBegin.remove(self.showMessageBox)
            self.msgVisible = False
        if not self.msgVisible:
            self.msgVisible = True
            self.avswitch.setInput('SCART')
            if not self.session.in_exec:
                self.notificationVisible = True
                Notifications.AddNotificationWithCallback(self.MsgBoxClosed, MessageBox, _('If you can see this, something is wrong with\nyour scart connection. Press OK to return.'), MessageBox.TYPE_ERROR, msgBoxID='scart_msgbox')
            else:
                self.msgBox = self.session.openWithCallback(self.MsgBoxClosed, MessageBox, _('If you can see this, something is wrong with\nyour scart connection. Press OK to return.'), MessageBox.TYPE_ERROR)
        return

    def MsgBoxClosed(self, *val):
        self.msgBox = None
        self.switchToTV()
        return

    def switchToTV(self, *val):
        if self.msgVisible:
            if self.msgBox:
                self.msgBox.close()
                return
            self.avswitch.setInput('ENCODER')
            self.msgVisible = False
        if self.notificationVisible:
            self.avswitch.setInput('ENCODER')
            self.notificationVisible = False
            for notification in Notifications.current_notifications:
                try:
                    if notification[1].msgBoxID == 'scart_msgbox':
                        notification[1].close()
                except:
                    print '[Scart] other notification is open. try another one.'