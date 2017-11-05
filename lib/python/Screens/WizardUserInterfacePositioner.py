# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Screens/WizardUserInterfacePositioner.py
# Compiled at: 2017-10-02 01:52:09
from Screens.Screen import Screen
from Screens.Wizard import wizardManagerWizardSummary
from Screens.WizardLanguage import WizardLanguage
from Screens.Rc import Rc
from Screens.MessageBox import MessageBox
from Components.Pixmap import PixmapMovingPixmapMultiPixmap
from Components.Sources.Boolean import Boolean
from Tools.Directories import resolveFilenameSCOPE_SKIN
from Components.config import configconfigfile
from Components.Console import Console

class UserInterfacePositionerWizard(WizardLanguage, Rc):

    def __init__(self, session, interface=None):
        self.xmlfile = resolveFilename(SCOPE_SKIN, 'userinterfacepositionerwizard.xml')
        WizardLanguage.__init__(self, session, showSteps=False, showStepSlider=False)
        Rc.__init__(self)
        self.skinName = 'StartWizard'
        self.session = session
        Screen.setTitle(self, _('Welcome...'))
        self.Console = Console()
        self['wizard'] = Pixmap()
        self['HelpWindow'] = Pixmap()
        self['HelpWindow'].hide()
        self['VKeyIcon'] = Boolean(False)
        self.NextStep = None
        self.Text = None
        self.onLayoutFinish.append(self.layoutFinished)
        self.onClose.append(self.__onClose)
        return

    def layoutFinished(self):
        self.Console.ePopen('/usr/bin/showiframe /usr/share/enigma2/hd-testcard.mvi')

    def exitWizardQuestion(self, ret=False):
        if ret:
            self.markDone()
            self.close()

    def markDone(self):
        pass

    def back(self):
        WizardLanguage.back(self)

    def __onClose(self):
        self.Console.ePopen('/usr/bin/showiframe /usr/share/backdrop.mvi')