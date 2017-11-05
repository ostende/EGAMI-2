# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Screens/SmartConsole.py
# Compiled at: 2017-10-02 01:52:09
from Screens.Screen import Screen
from Components.Label import Label
from Screens.MessageBox import MessageBox
from Tools.HardwareInfo import HardwareInfo
from Components.Sources.StaticText import StaticText
from Components.Sources.Progress import Progress
from Components.ActionMap import ActionMap
from Components.config import config
from enigma import eTimereEnveConsoleAppContainergetDesktopeSizeePoint

class SmartConsole(Screen):

    def __init__(self, session, title=_('Command execution...'), cmdlist=[], cmdmax=None, finishedCallback=None, closeOnSuccess=False, progressmode=True):
        Screen.__init__(self, session)
        self.finishedCallback = finishedCallback
        self.closeOnSuccess = closeOnSuccess
        self.cmdmax = cmdmax or len(cmdlist)
        self.progressmode = progressmode
        self.slider = Progress(0, 1000)
        self['slider'] = self.slider
        self.activityslider = Progress(0, 1000)
        self['activityslider'] = self.activityslider
        self.status = StaticText('')
        self['status'] = self.status
        self.text = StaticText('')
        self['text'] = self.text
        self.helpinfo = StaticText('')
        self['helpinfo'] = self.helpinfo
        self.activity = 0
        self.activityTimer = eTimer()
        self.activityTimer.callback.append(self.doActivityTimer)
        self.console = StaticText(None)
        self['console'] = self.console
        self.consolestatus = StaticText(None)
        self['consolestatus'] = self.consolestatus
        self['actions'] = ActionMap(['WizardActions', 'DirectionActions', 'TimerEditActions'], {'ok': self.ok,'back': self.cancel,
           'up': self.up,
           'down': self.down,
           'left': self.left,
           'right': self.right,
           'log': self.swapMode
           }, -1)
        size = getDesktop(0).size()
        self.fullsize = eSize(size.width() - 100, size.height() - 100)
        self.fullpos = ePoint(50, 50)
        self.cmdlist = cmdlist
        self.newtitle = title
        self.block = False
        self.text_long = ''
        self.stat_long = ''
        self.ret = 0
        self.run = 0
        self.container = eConsoleAppContainer()
        self.container.appClosed.append(self.runFinished)
        self.container.dataAvail.append(self.dataAvail)
        self.flagexit = False
        self.animation = False
        self.animationstep = 1 if HardwareInfo().get_device_model() == 'dm8000' else 15
        self.onClose.append(self._onClose)
        self.onLayoutFinish.append(self._onLayoutFinish)
        return

    def _onLayoutFinish(self):
        self.setTitle(self.newtitle)
        self.position = self.instance.position()
        self.size = self.instance.size()
        self.setMode()
        self.helpinfo.setText(_('Press INFO for show logging'))
        console = self.getRendererByName('console')
        console and console.onAnimationEnd.append(self.__onAnimationEnd)
        self.instance.animationEnd.get().append(self._onAnimationEnd)
        self.startRun()

    def _onClose(self):
        self.instance.animationEnd.get().remove(self._onAnimationEnd)
        del self.container.dataAvail[:]
        del self.container.appClosed[:]
        del self.container
        console = self.getRendererByName('console')
        if console:
            console.onAnimationEnd.remove(self.__onAnimationEnd)
        if self.finishedCallback is not None:
            self.stopActivityTimer()
            self.finishedCallback()
        return

    def ok(self):
        if self.run == self.cmdmax and not self.isRunning():
            if not self.progressmode and not self.animation and self.animationstep != 1:
                self.animation = True
                self.flagexit = True
                self.console.setText(None)
                self.instance.startMoveAnimation(self.position, self.size, self.animationstep, 10, 1)
            else:
                self.close()
        else:
            self.swapMode()
        return

    def cancel(self):
        if self.run == self.cmdmax and not self.isRunning():
            if not self.progressmode and not self.animation and self.animationstep != 1:
                self.animation = True
                self.flagexit = True
                self.console.setText(None)
                self.instance.startMoveAnimation(self.position, self.size, self.animationstep, 10, 1)
            else:
                self.close()
        else:
            self.session.openWithCallback(self.cancelCB, MessageBox, _('Do you really want to end the task?'), default=False, timeout=10)
        return

    def cancelCB(self, answer):
        if answer:
            self.close()

    def swapMode(self):
        self.progressmode = not self.progressmode
        self.setMode()

    def setMode(self):
        if self.progressmode:
            self.animation = True
            self.console.setText(None)
            self.text.setText(None)
            if self.run != self.cmdmax or self.isRunning():
                self.startActivityTimer()
            self.slider.setValue(int(self.run * 1000 / self.cmdmax))
            self.status.setText(self.stat_long)
            self.consolestatus.setText(None)
            self.helpinfo.setText(_('Press INFO for show logging'))
            self.instance.startMoveAnimation(self.position, self.size, self.animationstep, 10, 1)
        elif config.usage.setup_level.index > 1:
            self.animation = True
            self.console.setText(None)
            self.text.setText(None)
            self.stopActivityTimer()
            self.slider.setValue(None)
            self.status.setText(None)
            self.consolestatus.setText(self.stat_long)
            self.helpinfo.setText(_('Press INFO for hide logging'))
            self.instance.startMoveAnimation(self.fullpos, self.fullsize, self.animationstep, 10, 1)
        return

    def left(self):
        if self.progressmode:
            self.swapMode()
        if self.animation:
            return
        self.animation = True
        self.renders['console'].scrollPageUp()

    def right(self):
        if self.progressmode:
            self.swapMode()
        if self.animation:
            return
        self.animation = True
        self.renders['console'].scrollPageDown()

    def up(self):
        if self.progressmode:
            self.swapMode()
        if self.animation:
            return
        self.animation = True
        self.renders['console'].scrollUp()

    def down(self):
        if self.progressmode:
            self.swapMode()
        if self.animation:
            return
        self.animation = True
        self.renders['console'].scrollDown()

    def doActivityTimer(self):
        self.activity += 10
        if self.activity == 1000:
            self.activity = 0
        self.activityslider.setValue(self.activity)

    def startActivityTimer(self):
        self.activityTimer.start(100, False)

    def stopActivityTimer(self):
        self.activityTimer.stop()
        self.activityslider.setValue(None)
        return

    def isRunning(self):
        return self.container.running()

    def startRun(self):
        self.startActivityTimer()
        self.runFinished(self.ret)

    def runFinished(self, retval):
        self.ret = retval
        if self.block:
            return
        else:
            if self.run < len(self.cmdlist):
                cmd = self.cmdlist[self.run]
                self.run += 1
                if isinstance(cmd, (list, tuple, dict)):
                    self.stat_long = cmd[1]
                    cmd = cmd[0]
                if self.progressmode:
                    self.slider.setValue(int(self.run * 1000 / self.cmdmax))
                    self.status.setText(self.stat_long)
                else:
                    self.consolestatus.setText(self.stat_long)
                print '[SmartConsole] executing in run', self.run, '/', self.cmdmax, ' the command:', cmd
                if self.container.execute(cmd):
                    self.runFinished(-1)
            elif self.run == self.cmdmax:
                self.stopActivityTimer()
                if not retval and self.closeOnSuccess:
                    if not self.progressmode and not self.animation and self.animationstep != 1:
                        self.animation = True
                        self.flagexit = True
                        self.console.setText(None)
                        self.instance.startMoveAnimation(self.position, self.size, self.animationstep, 10, 1)
                    else:
                        self.close()
            return
            return

    def dataAvail(self, s=''):
        self.text_long += s
        if self.animation:
            return
        if self.progressmode:
            self.text.setText(self.text_long.strip().strip('\n').strip().strip('\n'))
        else:
            self.console.setText(self.text_long.strip().strip('\n').strip().strip('\n'))

    def addCmd(self, cmdlist, cmdmax=None, finishedCallback=None, closeOnSuccess=False):
        self.block = True
        self.cmdlist = self.cmdlist + cmdlist
        self.cmdmax = cmdmax or len(self.cmdlist)
        self.finishedCallback = finishedCallback
        self.closeOnSuccess = closeOnSuccess
        self.block = False
        if not self.isRunning():
            self.runFinished(self.ret)

    def __onAnimationEnd(self):
        self.animation = False

    def _onAnimationEnd(self):
        self.animation = False
        if self.flagexit:
            self.close()
        else:
            self.dataAvail()