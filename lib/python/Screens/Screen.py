# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Screens/Screen.py
# Compiled at: 2017-10-02 01:52:09
from Tools.Profile import profile
from enigma import eTimerePoint
from Components.config import config
from Components.SystemInfo import SystemInfo
profile('LOAD:GUISkin')
from Components.GUISkin import GUISkin
profile('LOAD:Source')
from Components.Sources.Source import Source
profile('LOAD:GUIComponent')
from Components.GUIComponent import GUIComponent
profile('LOAD:eRCInput')
from enigma import eRCInput
topSession = None

class Screen(dict, GUISkin):
    False, SUSPEND_STOPS, SUSPEND_PAUSES = range(3)
    ALLOW_SUSPEND = False
    global_screen = None

    def __init__(self, session, parent=None, fademenu=False):
        global topSession
        dict.__init__(self)
        self.skinName = self.__class__.__name__
        self.session = session
        self.parent = parent
        self.fademenu = config.misc.fadeShowMenu.value or fademenu
        GUISkin.__init__(self)
        self.onClose = []
        self.onFirstExecBegin = []
        self.onExecBegin = []
        self.onExecEnd = []
        self.onShown = []
        self.onShow = []
        self.onHide = []
        self.active_components = []
        self.onShowCode = []
        self.onHideCode = []
        self.execing = False
        self.shown = True
        self.already_shown = False
        self.renderer = []
        self.helpList = []
        self.close_on_next_exec = None
        self.stand_alone = False
        self.keyboardMode = None
        self.aFadeInDimmed = 0
        self.aFadeInTimer = eTimer()
        if config.misc.fadeShowMenu.value:
            if self.skinName not in ('Mute', 'Volume', 'PictureInPicture', 'PictureInPictureZapping',
                                     'Dishpip', 'EGAMIMainNews', 'PiPSetup'):
                self.aFadeInTimer.callback.append(self.doaFadeIn)
        topSession = self.session
        if config.misc.enableAnimationMenuScreens.value:
            self.onShow.append(self.animateMenuOnShow)
        return

    def animateMenuOnShow(self):
        try:
            if self.skinName[0] == 'MessageBox' or self.skinName[0] == 'MessageBoxSimple' or self.skinName[0] == 'EPGSearch' or self.skinName[0].endswith('_summary') or self.skinName[0].endswith('Summary'):
                return
        except:
            pass

        if config.misc.enableAnimationMenuScreens.value and self.skinName not in ('PictureInPicture',
                                                                                  'PictureInPictureZapping',
                                                                                  'Dishpip',
                                                                                  'InfoBar',
                                                                                  'SecondInfoBar',
                                                                                  'MoviePlayer',
                                                                                  'SimpleSummary',
                                                                                  'MessageBox_summary',
                                                                                  'MessageBox',
                                                                                  'EGEmuManagerStarting',
                                                                                  'EGConnectionAnimation',
                                                                                  'UnhandledKey',
                                                                                  'EGAMIMainNews',
                                                                                  'UpdateEGAMI',
                                                                                  'QuitMainloopScreen',
                                                                                  'Volume',
                                                                                  'ChannelSelection',
                                                                                  'QuickSubtitlesConfigMenu',
                                                                                  'EMCMediaCenter',
                                                                                  'PVRState',
                                                                                  'TimeshiftState',
                                                                                  'SmartConsole',
                                                                                  'Screensaver',
                                                                                  'SubtitleDisplay',
                                                                                  'RdsInfoDisplay',
                                                                                  'Console',
                                                                                  'MessageBoxSimple',
                                                                                  'IPTVPlayerWidget'):
            start_x = config.usage.addedinfobar_offposition_x.value
            start_y = config.usage.addedinfobar_offposition_y.value
            end_x = config.usage.addedinfobar_standartposition_x.value
            end_y = config.usage.addedinfobar_standartposition_y.value
            self.instance.startMoveAnimation(ePoint(start_x, start_y), ePoint(end_x, end_y), -9, 1, 10)

    def saveKeyboardMode(self):
        rcinput = eRCInput.getInstance()
        self.keyboardMode = rcinput.getKeyboardMode()

    def setKeyboardModeAscii(self):
        rcinput = eRCInput.getInstance()
        rcinput.setKeyboardMode(rcinput.kmAscii)

    def setKeyboardModeNone(self):
        rcinput = eRCInput.getInstance()
        rcinput.setKeyboardMode(rcinput.kmNone)

    def restoreKeyboardMode(self):
        rcinput = eRCInput.getInstance()
        if self.keyboardMode is not None:
            rcinput.setKeyboardMode(self.keyboardMode)
        return

    def execBegin(self):
        self.active_components = []
        if self.close_on_next_exec is not None:
            tmp = self.close_on_next_exec
            self.close_on_next_exec = None
            self.execing = True
            self.close(*tmp)
        else:
            single = self.onFirstExecBegin
            self.onFirstExecBegin = []
            for x in self.onExecBegin + single:
                x()
                if not self.stand_alone and self.session.current_dialog != self:
                    return

        for val in self.values() + self.renderer:
            val.execBegin()
            if not self.stand_alone and self.session.current_dialog != self:
                return
            self.active_components.append(val)

        self.execing = True
        for x in self.onShown:
            x()

        return

    def execEnd(self):
        active_components = self.active_components
        if active_components is not None:
            self.active_components = None
            for val in active_components:
                val.execEnd()

        self.execing = False
        for x in self.onExecEnd:
            x()

        return

    def doClose(self):
        self.hide()
        for x in self.onClose:
            x()

        del self.helpList
        GUISkin.close(self)
        for val in self.renderer:
            val.disconnectAll()

        del self.session
        for name, val in self.items():
            try:
                val.destroy()
            except:
                pass

            del self[name]

        self.renderer = []
        self.__dict__.clear()

    def close(self, *retval):
        global topSession
        if self.parent and hasattr(self.parent, 'session'):
            topSession = self.parent.session
        if hasattr(self, 'execing') and not self.execing:
            self.close_on_next_exec = retval
        else:
            try:
                self.session.close(self, *retval)
            except:
                pass

    def setFocus(self, o):
        self.instance.setFocus(o.instance)

    def doaFadeIn(self):
        if SystemInfo['CanChangeOsdAlpha']:
            self.aFadeInDimmed = self.aFadeInDimmed + 1
            if self.shown != False:
                try:
                    f = open('/proc/stb/video/alpha', 'w')
                    f.write(str(config.av.osd_alpha.value * self.aFadeInDimmed / 10))
                    f.close()
                except:
                    pass

            if self.aFadeInDimmed < 10:
                self.aFadeInTimer.start(2, True)
            else:
                try:
                    f = open('/proc/stb/video/alpha', 'w')
                    f.write(str(config.av.osd_alpha.value))
                    f.close()
                except:
                    pass

    def show(self):
        print '[SCREENNAME] ', self.skinName
        if self.shown and self.already_shown or not self.instance:
            return
        self.shown = True
        self.already_shown = True
        if self.fademenu and self.skinName not in ('Mute', 'Volume', 'PictureInPicture',
                                                   'PictureInPictureZapping', 'Dishpip',
                                                   'EGAMIMainNews', 'PiPSetup'):
            self.aFadeInTimer.start(2, True)
            self.aFadeInDimmed = 0
        self.instance.show()
        for f in self.onShow:
            f()

        for val in self.values() + self.renderer:
            if isinstance(val, GUIComponent) or isinstance(val, Source):
                val.onShow()

        for f in self.onShowCode:
            if type(f) is not type(self.close):
                exec f in globals(), locals()
            else:
                f()

    def hide(self):
        if not self.shown or not self.instance:
            return
        for f in self.onHide:
            f()

        for val in self.values() + self.renderer:
            if isinstance(val, GUIComponent) or isinstance(val, Source):
                val.onHide()

        for f in self.onHideCode:
            if type(f) is not type(self.close):
                exec f in globals(), locals()
            else:
                f()

        if not self.shown:
            return
        self.shown = False
        self.instance.hide()
        self.restoreAlpha()

    def setAnimationMode(self, mode):
        if self.instance:
            self.instance.setAnimationMode(mode)

    def restoreAlpha(self):
        if SystemInfo['CanChangeOsdAlpha']:
            try:
                f = open('/proc/stb/video/alpha', 'w')
                f.write(str(config.av.osd_alpha.value))
                f.close()
            except:
                pass

    def __repr__(self):
        return str(type(self))

    def getRelatedScreen(self, name):
        if name == 'session':
            return self.session.screen
        else:
            if name == 'parent':
                return self.parent
            if name == 'global':
                return self.global_screen
            return None
            return None

    def getRendererByName(self, name):
        for renderer in self.renderer:
            if renderer.name and renderer.name == name:
                return renderer

        return None

    def getRenderers(self):
        _renders = dict()
        for renderer in self.renderer:
            _renders[renderer.name] = renderer

        return _renders

    renders = property(getRenderers)

    def getAdditionalWidgets(self, name):
        for widget in self.additionalWidgets:
            if widget.name == name:
                return widget

        return None

    def getWidgets(self):
        _widgets = dict()
        for widget in self.additionalWidgets:
            _widgets[widget.name] = widget

        return _widgets

    widgets = property(getWidgets)

    def callback(self, *arg):
        pass