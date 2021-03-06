# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Screens/HelpMenu.py
# Compiled at: 2017-10-02 01:52:09
from Screens.Screen import Screen
from Components.Label import Label
from Components.ActionMap import ActionMap
from Components.HelpMenuList import HelpMenuList
from Screens.Rc import Rc

class HelpMenu(Screen, Rc):

    def __init__(self, session, list):
        Screen.__init__(self, session)
        Screen.setTitle(self, _('Help'))
        self.onSelChanged = []
        self['list'] = HelpMenuList(list, self.close)
        self['list'].onSelChanged.append(self.SelectionChanged)
        Rc.__init__(self)
        self['long_key'] = Label('')
        self['actions'] = ActionMap(['WizardActions'], {'ok': self['list'].ok,
           'back': self.close
           }, -1)
        self.onLayoutFinish.append(self.SelectionChanged)

    def SelectionChanged(self):
        self.clearSelectedKeys()
        selection = self['list'].getCurrent()
        if selection:
            selection = selection[3]
        print '[HelpMenu] selection:', selection
        longText = ''
        if selection and len(selection) > 1:
            if selection[1] == 'SHIFT':
                self.selectKey('SHIFT')
            elif selection[1] == 'long':
                longText = _('Long key press')
        self['long_key'].setText(longText)
        self.selectKey(selection[0])
        print '[HelpMenu] select arrow'


class HelpableScreen:

    def __init__(self):
        self['helpActions'] = ActionMap(['HelpActions'], {'displayHelp': self.showHelp
           })

    def showHelp(self):
        try:
            if self.secondInfoBarScreen and self.secondInfoBarScreen.shown:
                self.secondInfoBarScreen.hide()
        except:
            pass

        self.session.openWithCallback(self.callHelpAction, HelpMenu, self.helpList)

    def callHelpAction(self, *args):
        if args:
            actionmap, context, action = args
            actionmap.action(context, action)