# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Screens/WizardLanguage.py
# Compiled at: 2017-10-02 01:52:09
from Screens.Wizard import Wizard
from Components.Label import Label
from Components.Language import language

class WizardLanguage(Wizard):

    def __init__(self, session, showSteps=True, showStepSlider=True, showList=True, showConfig=True):
        Wizard.__init__(self, session, showSteps, showStepSlider, showList, showConfig)
        self['languagetext'] = Label()
        self.updateLanguageDescription()

    def red(self):
        self.resetCounter()
        self.languageSelect()

    def languageSelect(self):
        print '[WizardLanguage] languageSelect'
        newlanguage = language.getActiveLanguageIndex() + 1
        if newlanguage >= len(language.getLanguageList()):
            newlanguage = 0
        language.activateLanguageIndex(newlanguage)
        self.updateTexts()

    def updateLanguageDescription(self):
        print language.getLanguageList()[language.getActiveLanguageIndex()]
        self['languagetext'].setText(self.getTranslation(language.getLanguageList()[language.getActiveLanguageIndex()][1][0]))

    def updateTexts(self):
        print '[WizardLanguage] updateTexts'
        self.updateText(firstset=True)
        self.updateValues()
        self.updateLanguageDescription()