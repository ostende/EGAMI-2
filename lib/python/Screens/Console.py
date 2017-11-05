# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Screens/Console.py
# Compiled at: 2017-10-02 01:52:09
from enigma import eConsoleAppContainer
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.ScrollLabel import ScrollLabel

class Console(Screen):

    def __init__(self, session, title='Console', cmdlist=None, finishedCallback=None, closeOnSuccess=False):
        Screen.__init__(self, session)
        self.finishedCallback = finishedCallback
        self.closeOnSuccess = closeOnSuccess
        self.errorOcurred = False
        self['text'] = ScrollLabel('')
        self['actions'] = ActionMap(['WizardActions', 'DirectionActions'], {'ok': self.cancel,
           'back': self.cancel,
           'up': self['text'].pageUp,
           'down': self['text'].pageDown
           }, -1)
        self.cmdlist = cmdlist
        self.newtitle = title
        self.onShown.append(self.updateTitle)
        self.container = eConsoleAppContainer()
        self.run = 0
        self.container.appClosed.append(self.runFinished)
        self.container.dataAvail.append(self.dataAvail)
        self.onLayoutFinish.append(self.startRun)

    def updateTitle(self):
        self.setTitle(self.newtitle)

    def doExec(self, cmd):
        if isinstance(cmd, (list, tuple)):
            return self.container.execute(cmd[0], *cmd)
        else:
            return self.container.execute(cmd)

    def startRun(self):
        self['text'].setText(_('Execution progress:') + '\n\n')
        print 'Console: executing in run', self.run, ' the command:', self.cmdlist[self.run]
        if self.doExec(self.cmdlist[self.run]):
            self.runFinished(-1)

    def runFinished(self, retval):
        if retval:
            self.errorOcurred = True
        self.run += 1
        if self.run != len(self.cmdlist):
            if self.doExec(self.cmdlist[self.run]):
                self.runFinished(-1)
        else:
            lastpage = self['text'].isAtLastPage()
            str = self['text'].getText()
            str += _('Execution finished!!')
            self['text'].setText(str)
            if lastpage:
                self['text'].lastPage()
            if self.finishedCallback is not None:
                self.finishedCallback()
            if not self.errorOcurred and self.closeOnSuccess:
                self.cancel()
        return

    def cancel(self):
        if self.run == len(self.cmdlist):
            self.close()
            self.container.appClosed.remove(self.runFinished)
            self.container.dataAvail.remove(self.dataAvail)

    def dataAvail(self, str):
        lastpage = self['text'].isAtLastPage()
        self['text'].setText(self['text'].getText() + str)
        if lastpage:
            self['text'].lastPage()