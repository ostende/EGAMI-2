# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Screens/StreamingClientsInfo.py
# Compiled at: 2017-10-02 01:52:09
from Screen import Screen
from Components.About import about
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from Components.Converter.ClientsStreaming import ClientsStreaming
from Components.config import config
from Components.Sources.StaticText import StaticText
from enigma import eTimereStreamServer
import skin

class StreamingClientsInfo(Screen):

    def __init__(self, session, menu_path=''):
        Screen.__init__(self, session)
        self.timer = eTimer()
        screentitle = _('Streaming clients info')
        menu_path += screentitle
        if config.usage.show_menupath.value == 'large':
            title = menu_path
            self['menu_path_compressed'] = StaticText('')
        elif config.usage.show_menupath.value == 'small':
            title = screentitle
            self['menu_path_compressed'] = StaticText(menu_path.endswith(' / ') or menu_path + ' >' if 1 else menu_path[:-3] + ' >' or '')
        else:
            title = screentitle
            self['menu_path_compressed'] = StaticText('')
        Screen.setTitle(self, title)
        self['ScrollLabel'] = ScrollLabel()
        self['lab1'] = Label(_('EGAMI %s') % about.getImageVersionString())
        self['key_red'] = Button(_('Close'))
        self['key_blue'] = Button()
        self['actions'] = ActionMap(['ColorActions', 'SetupActions', 'DirectionActions'], {'cancel': self.exit,
           'ok': self.exit,
           'red': self.exit,
           'blue': self.stopStreams,
           'up': self['ScrollLabel'].pageUp,
           'down': self['ScrollLabel'].pageDown
           })
        self.onLayoutFinish.append(self.start)

    def exit(self):
        self.stop()
        self.close()

    def start(self):
        if self.update_info not in self.timer.callback:
            self.timer.callback.append(self.update_info)
        self.timer.startLongTimer(0)

    def stop(self):
        if self.update_info in self.timer.callback:
            self.timer.callback.remove(self.update_info)
        self.timer.stop()

    def update_info(self):
        clients = ClientsStreaming('INFO_RESOLVE')
        text = clients.getText()
        self['ScrollLabel'].setText(text or _('No clients streaming'))
        self['key_blue'].setText(text and _('Stop Streams') or '')
        self.timer.startLongTimer(5)

    def stopStreams(self):
        streamServer = eStreamServer.getInstance()
        if not streamServer:
            return
        for x in streamServer.getConnectedClients():
            streamServer.stopStream()