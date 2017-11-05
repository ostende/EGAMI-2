# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Screens/StartWizard.py
# Compiled at: 2017-10-02 01:52:09
from Wizard import wizardManager
from Screens.WizardLanguage import WizardLanguage
from Screens.VideoWizard import VideoWizard
from Screens.Rc import Rc
from Screens.Screen import Screen
from boxbranding import getBoxType
from Components.Pixmap import Pixmap
from Components.config import configConfigBooleanconfigfile
from LanguageSelection import LanguageWizard
config.misc.firstrun = ConfigBoolean(default=True)
config.misc.languageselected = ConfigBoolean(default=True)
config.misc.videowizardenabled = ConfigBoolean(default=True)
config.misc.networkwizardenabled = ConfigBoolean(default=True)

class StartWizard(WizardLanguage, Rc):

    def __init__(self, session, silent=True, showSteps=False, neededTag=None):
        self.xmlfile = ['startwizard.xml']
        WizardLanguage.__init__(self, session, showSteps=False)
        Rc.__init__(self)
        self['wizard'] = Pixmap()
        Screen.setTitle(self, _('Welcome...'))

    def markDone(self):
        if getBoxType() == 'dm8000':
            config.misc.rcused.value = 0
        else:
            config.misc.rcused.value = 1
        config.misc.rcused.save()
        config.misc.firstrun.value = 0
        config.misc.firstrun.save()
        configfile.save()

    def EGAMI_SpeedUP_Wizard(self):
        from EGAMI.EGAMI_Green import EGAMISpeedUpWizard
        self.session.openWithCallback(self.EGAMI_close_end, EGAMISpeedUpWizard, True)

    def EGAMI_close_end(self):
        from Components.PluginComponent import plugins
        from Tools.Directories import SCOPE_PLUGINSresolveFilename
        plugins.firstRun = True
        plugins.clearPluginList()
        from Screens.MessageBox import MessageBox
        try:
            mybox = self.session.open(MessageBox, _('EGAMI is speeding up! Please wait...'), MessageBox.TYPE_INFO, 5)
            mybox.setTitle(_('Info'))
            plugins.readPluginList(resolveFilename(SCOPE_PLUGINS))
        except:
            self.close()

    def EGAMI_SkinSelector_Wizard(self):
        from EGAMI.EGAMI_Green import EGAMISkinWizard
        self.session.open(EGAMISkinWizard, True)


wizardManager.registerWizard(VideoWizard, config.misc.videowizardenabled.value, priority=0)
wizardManager.registerWizard(LanguageWizard, config.misc.languageselected.value, priority=2)
wizardManager.registerWizard(StartWizard, config.misc.firstrun.value, priority=20)