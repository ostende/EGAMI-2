# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Screens/Menu.py
# Compiled at: 2017-10-02 01:52:09
from Screens.Screen import Screen
from Screens.ParentalControlSetup import ProtectedScreen
from Components.Sources.List import List
from Components.ActionMap import NumberActionMapActionMap
from Components.Sources.StaticText import StaticText
from Components.config import configfile
from Components.PluginComponent import plugins
from Components.config import configConfigDictionarySetNoSave
from Components.SystemInfo import SystemInfo
from Components.Label import Label
from Tools.BoundFunction import boundFunction
from Plugins.Plugin import PluginDescriptor
from Tools.Directories import resolveFilenameSCOPE_SKINSCOPE_CURRENT_SKIN
from Tools.LoadPixmap import LoadPixmap
from enigma import eTimer
import xml.etree.cElementTree
from Screens.Setup import SetupgetSetupTitlegetSetupTitleLevel
from Components.Pixmap import PixmapMovingPixmap
from Components.Sources.StaticText import StaticText
import os
from Components.Button import Button
mainmenu = _('Main menu')
lastMenuID = None

def MenuEntryPixmap(entryID, png_cache, lastMenuID):
    png = png_cache.get(entryID, None)
    if png is None:
        pngPath = resolveFilename(SCOPE_CURRENT_SKIN, 'mainmenu/' + entryID + '.png')
        pos = config.skin.primary_skin.value.rfind('/')
        if pos > -1:
            current_skin = config.skin.primary_skin.value[:pos + 1]
        else:
            current_skin = ''
        if current_skin in pngPath and current_skin or not current_skin:
            png = LoadPixmap(pngPath, cached=True)
        if png is None:
            if lastMenuID is not None:
                png = png_cache.get(lastMenuID, None)
        png_cache[entryID] = png
    if png is None:
        png = png_cache.get('missing', None)
        if png is None:
            png = LoadPixmap(resolveFilename(SCOPE_CURRENT_SKIN, 'mainmenu/missing.png'), cached=True)
            png_cache['missing'] = png
    return png


file = open(resolveFilename(SCOPE_SKIN, 'menu.xml'), 'r')
mdom = xml.etree.cElementTree.parse(file)
file.close()

class title_History():

    def __init__(self):
        self.thistory = ''

    def reset(self):
        self.thistory = ''

    def reducehistory(self):
        history_len = len(self.thistory.split('>'))
        if history_len < 3:
            self.reset()
            return
        if self.thistory == '':
            return
        result = self.thistory.rsplit('>', 2)
        if result[0] == '':
            self.reset()
            return
        self.thistory = result[0] + '> '


t_history = title_History()

class MenuUpdater():

    def __init__(self):
        self.updatedMenuItems = {}

    def addMenuItem(self, id, pos, text, module, screen, weight, description):
        if not self.updatedMenuAvailable(id):
            self.updatedMenuItems[id] = []
        self.updatedMenuItems[id].append([text, pos, module, screen, weight, description])

    def delMenuItem(self, id, pos, text, module, screen, weight, description):
        self.updatedMenuItems[id].remove([text, pos, module, screen, weight, description])

    def updatedMenuAvailable(self, id):
        return self.updatedMenuItems.has_key(id)

    def getUpdatedMenu(self, id):
        return self.updatedMenuItems[id]


menuupdater = MenuUpdater()

class MenuSummary(Screen):
    pass


class Menu(Screen, ProtectedScreen):
    ALLOW_SUSPEND = True
    png_cache = {}

    def okbuttonClick(self):
        global lastMenuID
        self.resetNumberKey()
        selection = self['menu'].getCurrent()
        if selection is not None and selection[1] is not None:
            lastMenuID = selection[2]
            selection[1]()
        return

    def execText(self, text):
        exec text

    def runScreen(self, arg):
        if arg[0] != '':
            exec 'from ' + arg[0] + ' import *'
        self.openDialog(*eval(arg[1]))

    def nothing(self):
        pass

    def gotoStandby(self, *res):
        from Screens.Standby import Standby2
        self.session.open(Standby2)
        self.close(True)

    def openDialog(self, *dialog):
        self.session.openWithCallback(self.menuClosed, *dialog)

    def openSetup(self, dialog):
        self.session.openWithCallback(self.menuClosed, Setup, dialog)

    def addMenu(self, destList, node):
        requires = node.get('requires')
        if requires:
            if requires[0] == '!':
                if SystemInfo.get(requires[1:], False):
                    return
            elif not SystemInfo.get(requires, False):
                return
        MenuTitle = _(node.get('text', '??').encode('UTF-8'))
        entryID = node.get('entryID', 'undefined')
        weight = node.get('weight', 50)
        description = node.get('description', '').encode('UTF-8') or None
        description = description and _(description)
        menupng = MenuEntryPixmap(entryID, self.png_cache, lastMenuID)
        x = node.get('flushConfigOnClose')
        if x:
            a = boundFunction(self.session.openWithCallback, self.menuClosedWithConfigFlush, Menu, node)
        else:
            a = boundFunction(self.session.openWithCallback, self.menuClosed, Menu, node)
        destList.append((MenuTitle, a, entryID, weight, description, menupng))
        return

    def menuClosedWithConfigFlush(self, *res):
        configfile.save()
        self.menuClosed(*res)

    def menuClosed(self, *res):
        global lastMenuID
        if res and res[0]:
            lastMenuID = None
            self.close(True)
        return

    def addItem(self, destList, node):
        requires = node.get('requires')
        if requires:
            if requires[0] == '!':
                if SystemInfo.get(requires[1:], False):
                    return
            elif not SystemInfo.get(requires, False):
                return
        configCondition = node.get('configcondition')
        if configCondition and not eval(configCondition + '.value'):
            return
        else:
            item_text = node.get('text', '').encode('UTF-8')
            entryID = node.get('entryID', 'undefined')
            weight = node.get('weight', 50)
            description = node.get('description', '').encode('UTF-8') or ''
            description = description and _(description)
            menupng = MenuEntryPixmap(entryID, self.png_cache, lastMenuID)
            for x in node:
                if x.tag == 'screen':
                    module = x.get('module')
                    screen = x.get('screen')
                    if screen is None:
                        screen = module
                    if module:
                        module = 'Screens.' + module
                    else:
                        module = ''
                    args = x.text or ''
                    screen += ', ' + args
                    destList.append((_(item_text or '??'), boundFunction(self.runScreen, (module, screen)), entryID, weight, description, menupng))
                    return
                if x.tag == 'plugin':
                    extensions = x.get('extensions')
                    system = x.get('system')
                    screen = x.get('screen')
                    if extensions:
                        module = extensions
                    elif system:
                        module = system
                    if screen is None:
                        screen = module
                    if extensions:
                        module = 'Plugins.Extensions.' + extensions + '.plugin'
                    elif system:
                        module = 'Plugins.SystemPlugins.' + system + '.plugin'
                    else:
                        module = ''
                    args = x.text or ''
                    screen += ', ' + args
                    destList.append((_(item_text or '??'), boundFunction(self.runScreen, (module, screen)), entryID, weight, description, menupng))
                    return
                if x.tag == 'code':
                    destList.append((_(item_text or '??'), boundFunction(self.execText, x.text), entryID, weight, description, menupng))
                    return
                if x.tag == 'setup':
                    id = x.get('id')
                    if item_text == '':
                        if getSetupTitleLevel(id) > config.usage.setup_level.index:
                            return
                        item_text = _(getSetupTitle(id))
                    else:
                        item_text = _(item_text)
                    destList.append((item_text, boundFunction(self.openSetup, id), entryID, weight, description, menupng))
                    return

            destList.append((item_text, self.nothing, entryID, weight, description, menupng))
            return

    def sortByName(self, listentry):
        return listentry[0].lower()

    def __init__(self, session, parent):
        Screen.__init__(self, session)
        self.sort_mode = False
        self.selected_entry = None
        self.sub_menu_sort = None
        self['green'] = Label()
        self['yellow'] = Label()
        self['blue'] = Label()
        m_list = []
        menuID = None
        for x in parent:
            if not x.tag:
                continue
            if x.tag == 'item':
                item_level = int(x.get('level', 0))
                if item_level <= config.usage.setup_level.index:
                    self.addItem(m_list, x)
                    count += 1
            elif x.tag == 'menu':
                item_level = int(x.get('level', 0))
                if item_level <= config.usage.setup_level.index:
                    self.addMenu(m_list, x)
                    count += 1
            elif x.tag == 'id':
                menuID = x.get('val')
                count = 0
            if menuID is not None:
                if menuupdater.updatedMenuAvailable(menuID):
                    for x in menuupdater.getUpdatedMenu(menuID):
                        if x[1] == count:
                            description = x.get('description', '').encode('UTF-8') or None
                            description = description and _(description)
                            menupng = MenuEntryPixmap(menuID, self.png_cache, lastMenuID)
                            m_list.append((x[0], boundFunction(self.runScreen, (x[2], x[3] + ', ')), x[4], description, menupng))
                            count += 1

        self.menuID = menuID
        if config.ParentalControl.configured.value:
            ProtectedScreen.__init__(self)
        if menuID is not None:
            for l in plugins.getPluginsForMenu(menuID):
                plugin_menuid = l[2]
                for x in m_list:
                    if x[2] == plugin_menuid:
                        m_list.remove(x)
                        break

                description = plugins.getDescriptionForMenuEntryID(menuID, plugin_menuid)
                menupng = MenuEntryPixmap(l[2], self.png_cache, lastMenuID)
                if len(l) > 6 and l[6]:
                    m_list.append((l[0], boundFunction(l[1], self.session, self.close), l[2], l[3] or 50, description, menupng))
                else:
                    m_list.append((l[0], boundFunction(l[1], self.session), l[2], l[3] or 50, description, menupng))

        self.skinName = []
        skfile = '/usr/share/enigma2/' + config.skin.primary_skin.value
        f1 = open(skfile, 'r')
        self.sktxt = f1.read()
        f1.close()
        if menuID is not None:
            if '<screen name="Animmain" ' in self.sktxt and config.usage.menutype.value == 'horzanim':
                self.skinName.append('Animmain')
            elif '<screen name="Iconmain" ' in self.sktxt and config.usage.menutype.value == 'horzicon':
                if '<screen name="Iconmain" ' in self.sktxt:
                    self.skinName.append('Iconmain')
            else:
                self.skinName.append('menu_' + menuID)
        self.skinName.append('Menu')
        self.menuID = menuID
        ProtectedScreen.__init__(self)
        if config.usage.menu_sort_mode.value == 'user' and menuID == 'mainmenu':
            plugin_list = []
            id_list = []
            for l in plugins.getPlugins([PluginDescriptor.WHERE_PLUGINMENU, PluginDescriptor.WHERE_EXTENSIONSMENU, PluginDescriptor.WHERE_EVENTINFO]):
                l.id = l.name.lower().replace(' ', '_')
                if l.id not in id_list:
                    id_list.append(l.id)
                    plugin_list.append((l.name, boundFunction(l.__call__, session), l.id, 200, '', ''))

        self.list = m_list
        if menuID is not None and config.usage.menu_sort_mode.value == 'user':
            self.sub_menu_sort = NoSave(ConfigDictionarySet())
            self.sub_menu_sort.value = config.usage.menu_sort_weight.getConfigValue(self.menuID, 'submenu') or {}
            idx = 0
            for x in self.list:
                entry = list(self.list.pop(idx))
                m_weight = self.sub_menu_sort.getConfigValue(entry[2], 'sort') or entry[3]
                entry.append(m_weight)
                self.list.insert(idx, tuple(entry))
                self.sub_menu_sort.changeConfigValue(entry[2], 'sort', m_weight)
                idx += 1

            self.full_list = list(m_list)
        if config.usage.menu_sort_mode.value == 'a_z':
            m_list.sort(key=self.sortByName)
        elif config.usage.menu_sort_mode.value == 'user':
            self['blue'].setText(_('Edit mode on'))
            self.hide_show_entries()
            m_list = self.list
        else:
            m_list.sort(key=lambda x: int(x[3]))
        if config.usage.menu_show_numbers.value:
            m_list = [ (str(x[0] + 1) + ' ' + x[1][0], x[1][1], x[1][2]) for x in enumerate(m_list) ]
        self['menu'] = List(m_list)
        self['menu'].enableWrapAround = True
        if config.usage.menu_sort_mode.value == 'user':
            self['menu'].onSelectionChanged.append(self.selectionChanged)
        self['actions'] = NumberActionMap(['OkCancelActions', 'MenuActions', 'NumberActions'], {'ok': self.okbuttonClick,
           'cancel': self.closeNonRecursive,
           'menu': self.closeRecursive,
           '0': self.keyNumberGlobal,
           '1': self.keyNumberGlobal,
           '2': self.keyNumberGlobal,
           '3': self.keyNumberGlobal,
           '4': self.keyNumberGlobal,
           '5': self.keyNumberGlobal,
           '6': self.keyNumberGlobal,
           '7': self.keyNumberGlobal,
           '8': self.keyNumberGlobal,
           '9': self.keyNumberGlobal
           })
        if config.usage.menu_sort_mode.value == 'user':
            self['MoveActions'] = ActionMap(['WizardActions'], {'left': self.keyLeft,
               'right': self.keyRight,
               'up': self.keyUp,
               'down': self.keyDown
               }, -1)
            self['EditActions'] = ActionMap(['ColorActions'], {'green': self.keyGreen,
               'yellow': self.keyYellow,
               'blue': self.keyBlue
               })
        a = parent.get('title', '').encode('UTF-8') or None
        a = a and _(a)
        if a is None:
            a = _(parent.get('text', '').encode('UTF-8'))
        else:
            t_history.reset()
        self['title'] = StaticText(a)
        Screen.setTitle(self, a)
        self.menu_title = a
        self['thistory'] = StaticText(t_history.thistory)
        history_len = len(t_history.thistory)
        self['title0'] = StaticText('')
        self['title1'] = StaticText('')
        self['title2'] = StaticText('')
        if history_len < 13:
            self['title0'] = StaticText(a)
        elif history_len < 21:
            self['title0'] = StaticText('')
            self['title1'] = StaticText(a)
        else:
            self['title0'] = StaticText('')
            self['title1'] = StaticText('')
            self['title2'] = StaticText(a)
        if t_history.thistory == '':
            t_history.thistory = str(a) + ' > '
        else:
            t_history.thistory = t_history.thistory + str(a) + ' > '
        if '<screen name="Animmain" ' in self.sktxt and config.usage.menutype.value == 'horzanim':
            self.onShown.append(self.openTestA)
        elif '<screen name="Iconmain" ' in self.sktxt and config.usage.menutype.value == 'horzicon':
            if '<screen name="Iconmain" ' in self.sktxt:
                self.onShown.append(self.openTestB)
        self.number = 0
        self.nextNumberTimer = eTimer()
        self.nextNumberTimer.callback.append(self.okbuttonClick)
        return

    def openTestA(self):
        self.session.open(AnimMain, self.list, self.menu_title)
        self.close()

    def openTestB(self):
        self.session.open(IconMain, self.list, self.menu_title)
        self.close()

    def isProtected(self):
        if config.ParentalControl.setuppinactive.value:
            if config.ParentalControl.config_sections.main_menu.value and self.menuID == 'mainmenu':
                return True
            if config.ParentalControl.config_sections.configuration.value and self.menuID == 'setup':
                return True
            if config.ParentalControl.config_sections.timer_menu.value and self.menuID == 'timermenu':
                return True
            if config.ParentalControl.config_sections.standby_menu.value and self.menuID == 'shutdown':
                return True

    def keyNumberGlobal(self, number):
        self.number = self.number * 10 + number
        if self.number and self.number <= len(self['menu'].list):
            self['menu'].setIndex(self.number - 1)
            if len(self['menu'].list) < 10 or self.number >= 10:
                self.okbuttonClick()
            else:
                self.nextNumberTimer.start(1500, True)
        else:
            self.number = 0

    def resetNumberKey(self):
        self.nextNumberTimer.stop()
        self.number = 0

    def closeNonRecursive(self):
        self.resetNumberKey()
        t_history.reducehistory()
        self.close(False)

    def closeRecursive(self):
        self.resetNumberKey()
        t_history.reset()
        self.close(True)

    def createSummary(self):
        return MenuSummary

    def isProtected(self):
        if config.ParentalControl.setuppinactive.value:
            if config.ParentalControl.config_sections.main_menu.value:
                return self.menuID == 'mainmenu'
            if config.ParentalControl.config_sections.configuration.value and self.menuID == 'setup':
                return True
            if config.ParentalControl.config_sections.timer_menu.value and self.menuID == 'timermenu':
                return True
            if config.ParentalControl.config_sections.standby_menu.value and self.menuID == 'shutdown':
                return True

    def updateList(self):
        self.sub_menu_sort = NoSave(ConfigDictionarySet())
        self.sub_menu_sort.value = config.usage.menu_sort_weight.getConfigValue(self.menuID, 'submenu') or None
        idx = 0
        for x in self.list:
            entry = list(self.list.pop(idx))
            m_weight = self.sub_menu_sort.getConfigValue(entry[2], 'sort') or entry[3]
            entry.append(m_weight)
            self.list.insert(idx, tuple(entry))
            self.sub_menu_sort.changeConfigValue(entry[2], 'sort', m_weight)
            if not self.sort_mode and self.sub_menu_sort.getConfigValue(entry[2], 'hidden'):
                self.list.remove(x)
            idx += 1

        return

    def keyLeft(self):
        self.cur_idx = self['menu'].getSelectedIndex()
        self['menu'].pageUp()
        if self.sort_mode and self.selected_entry is not None:
            self.moveAction()
        return

    def keyRight(self):
        self.cur_idx = self['menu'].getSelectedIndex()
        self['menu'].pageDown()
        if self.sort_mode and self.selected_entry is not None:
            self.moveAction()
        return

    def keyDown(self):
        self.cur_idx = self['menu'].getSelectedIndex()
        self['menu'].down()
        if self.sort_mode and self.selected_entry is not None:
            self.moveAction()
        return

    def keyUp(self):
        self.cur_idx = self['menu'].getSelectedIndex()
        self['menu'].up()
        if self.sort_mode and self.selected_entry is not None:
            self.moveAction()
        return

    def keyOk(self):
        if self.sort_mode and len(self.list):
            m_entry = selection = self['menu'].getCurrent()
            select = False
            if self.selected_entry is None:
                select = True
            elif self.selected_entry != m_entry[2]:
                select = True
            if not select:
                self['green'].setText(_('Move mode on'))
                self.selected_entry = None
            else:
                self['green'].setText(_('Move mode off'))
            idx = 0
            for x in self.list:
                if m_entry[2] == x[2] and select == True:
                    self.selected_entry = m_entry[2]
                    break
                elif m_entry[2] == x[2] and select == False:
                    self.selected_entry = None
                    break
                idx += 1

        elif not self.sort_mode:
            self.okbuttonClick()
        return

    def moveAction(self):
        tmp_list = list(self.list)
        entry = tmp_list.pop(self.cur_idx)
        newpos = self['menu'].getSelectedIndex()
        tmp_list.insert(newpos, entry)
        self.list = list(tmp_list)
        self['menu'].updateList(self.list)

    def keyBlue(self):
        if config.usage.menu_sort_mode.value == 'user':
            self.toggleSortMode()

    def keyYellow(self):
        if self.sort_mode:
            m_entry = selection = self['menu'].getCurrent()[2]
            hidden = self.sub_menu_sort.getConfigValue(m_entry, 'hidden') or 0
            if hidden:
                self.sub_menu_sort.removeConfigValue(m_entry, 'hidden')
                self['yellow'].setText(_('hide'))
            else:
                self.sub_menu_sort.changeConfigValue(m_entry, 'hidden', 1)
                self['yellow'].setText(_('show'))

    def keyGreen(self):
        if self.sort_mode:
            self.keyOk()

    def keyCancel(self):
        if self.sort_mode:
            self.toggleSortMode()
        else:
            self.closeNonRecursive()

    def resetSortOrder(self, key=None):
        config.usage.menu_sort_weight.value = {'mainmenu': {'submenu': {}}}
        config.usage.menu_sort_weight.save()
        self.closeRecursive()

    def toggleSortMode(self):
        if self.sort_mode:
            self['green'].setText('')
            self['yellow'].setText('')
            self['blue'].setText(_('Edit mode on'))
            self.sort_mode = False
            i = 10
            idx = 0
            for x in self.list:
                self.sub_menu_sort.changeConfigValue(x[2], 'sort', i)
                if len(x) >= 7:
                    entry = list(x)
                    entry[6] = i
                    entry = tuple(entry)
                    self.list.pop(idx)
                    self.list.insert(idx, entry)
                if self.selected_entry is not None:
                    if x[2] == self.selected_entry:
                        self.selected_entry = None
                i += 10
                idx += 1

            self.full_list = list(self.list)
            config.usage.menu_sort_weight.changeConfigValue(self.menuID, 'submenu', self.sub_menu_sort.value)
            config.usage.menu_sort_weight.save()
            self.hide_show_entries()
            self['menu'].setList(self.list)
        else:
            self['green'].setText(_('Move mode on'))
            self['blue'].setText(_('Edit mode off'))
            self.sort_mode = True
            self.hide_show_entries()
            self['menu'].updateList(self.list)
            self.selectionChanged()
        return

    def hide_show_entries(self):
        m_list = list(self.full_list)
        if not self.sort_mode:
            rm_list = []
            for entry in m_list:
                if self.sub_menu_sort.getConfigValue(entry[2], 'hidden'):
                    rm_list.append(entry)

            for entry in rm_list:
                if entry in m_list:
                    m_list.remove(entry)

        if not len(m_list):
            m_list.append(('', None, 'dummy', '10', 10, '', None))
        m_list.sort(key=lambda listweight: int(listweight[6]))
        self.list = list(m_list)
        return None

    def selectionChanged(self):
        if self.sort_mode:
            selection = self['menu'].getCurrent()[2]
            if self.sub_menu_sort.getConfigValue(selection, 'hidden'):
                self['yellow'].setText(_('show'))
            else:
                self['yellow'].setText(_('hide'))
        else:
            self['yellow'].setText('')


class AnimMain(Screen):

    def __init__(self, session, tlist, menuTitle):
        Screen.__init__(self, session)
        self.skinName = 'Animmain'
        self.tlist = tlist
        ipage = 1
        list = []
        nopic = len(tlist)
        self.pos = []
        self.index = 0
        title = menuTitle
        self['title'] = Button(title)
        list = []
        tlist = []
        self['label1'] = StaticText()
        self['label2'] = StaticText()
        self['label3'] = StaticText()
        self['label4'] = StaticText()
        self['label5'] = StaticText()
        self['red'] = Button(_('Exit'))
        self['green'] = Button(_('Select'))
        self['yellow'] = Button(_('Config'))
        self['actions'] = NumberActionMap(['OkCancelActions', 'MenuActions', 'DirectionActions', 'NumberActions', 'ColorActions'], {'ok': self.okbuttonClick,
           'cancel': self.closeNonRecursive,
           'left': self.key_left,
           'right': self.key_right,
           'up': self.key_up,
           'down': self.key_down,
           'red': self.cancel,
           'green': self.okbuttonClick,
           'yellow': self.key_menu,
           'menu': self.closeRecursive,
           '1': self.keyNumberGlobal,
           '2': self.keyNumberGlobal,
           '3': self.keyNumberGlobal,
           '4': self.keyNumberGlobal,
           '5': self.keyNumberGlobal,
           '6': self.keyNumberGlobal,
           '7': self.keyNumberGlobal,
           '8': self.keyNumberGlobal,
           '9': self.keyNumberGlobal
           })
        nop = len(self.tlist)
        self.nop = nop
        nh = 1
        if nop == 1:
            nh = 1
        elif nop == 2:
            nh = 2
        elif nop == 3:
            nh = 2
        elif nop == 4:
            nh = 3
        elif nop == 5:
            nh = 3
        else:
            nh = int(float(nop) / 2)
        self.index = nh
        i = 0
        self.onShown.append(self.openTest)

    def key_menu(self):
        pass

    def cancel(self):
        self.close()

    def paintFrame(self):
        pass

    def getname(self, name):
        if 'AutoBouquetsMaker' in name:
            name = 'AutoBouquets\nMakerProvider'
        if len(name) > 14:
            if '-' in name or '/' in name or ' ' in name:
                name = name.replace('-', '/')
                name = name.replace(' /', '/')
                name = name.replace('/ ', '/')
                name = name.replace(' ', '\n')
            else:
                name = name[:14] + '/' + name[12:]
        if 'A/V' not in name:
            name = name.replace('/', '\n')
        if 'di\n' in name:
            name = name.replace('di\n', 'di ')
        if 'de\n' in name:
            name = name.replace('de\n', 'de ')
        if 'la\n' in name:
            name = name.replace('la\n', 'la ')
        return name

    def openTest(self):
        i = self.index
        if i - 3 > -1:
            name1 = self.getname(self.tlist[i - 3][0])
        else:
            name1 = ' '
        if i - 2 > -1:
            name2 = self.getname(self.tlist[i - 2][0])
        else:
            name2 = ' '
        name3 = self.getname(self.tlist[i - 1][0])
        if i < self.nop:
            name4 = self.getname(self.tlist[i][0])
        else:
            name4 = ' '
        if i + 1 < self.nop:
            name5 = self.getname(self.tlist[i + 1][0])
        else:
            name5 = ' '
        self['label1'].setText(name1)
        self['label2'].setText(name2)
        self['label3'].setText(name3)
        self['label4'].setText(name4)
        self['label5'].setText(name5)

    def key_left(self):
        self.index -= 1
        if self.index < 1:
            self.index = 1
            return
        self.openTest()

    def key_right(self):
        self.index += 1
        if self.index > self.nop:
            self.index = self.nop
            return
        self.openTest()

    def key_up(self):
        pass

    def key_down(self):
        pass

    def keyNumberGlobal(self, number):
        number -= 1
        if len(self['menu'].list) > number:
            self['menu'].setIndex(number)
            self.okbuttonClick()

    def closeNonRecursive(self):
        self.close(False)

    def closeRecursive(self):
        self.close(True)

    def createSummary(self):
        pass

    def keyNumberGlobal(self, number):
        number -= 1
        if len(self['menu'].list) > number:
            self['menu'].setIndex(number)
            self.okbuttonClick()

    def closeNonRecursive(self):
        self.close(False)

    def closeRecursive(self):
        self.close(True)

    def createSummary(self):
        pass

    def okbuttonClick(self):
        idx = self.index - 1
        selection = self.tlist[idx]
        if selection is not None:
            selection[1]()
        return


class IconMain(Screen):

    def __init__(self, session, tlist, menuTitle):
        Screen.__init__(self, session)
        self.skinName = 'Iconmain'
        self.tlist = tlist
        ipage = 1
        list = []
        nopic = len(self.tlist)
        self.pos = []
        self.ipage = 1
        self.index = 0
        title = menuTitle
        self['title'] = Button(title)
        self.icons = []
        self.indx = []
        n1 = len(tlist)
        self.picnum = n1
        list = []
        tlist = []
        self['label1'] = StaticText()
        self['label2'] = StaticText()
        self['label3'] = StaticText()
        self['label4'] = StaticText()
        self['label5'] = StaticText()
        self['label6'] = StaticText()
        self['label1s'] = StaticText()
        self['label2s'] = StaticText()
        self['label3s'] = StaticText()
        self['label4s'] = StaticText()
        self['label5s'] = StaticText()
        self['label6s'] = StaticText()
        self['pointer'] = Pixmap()
        self['pixmap1'] = Pixmap()
        self['pixmap2'] = Pixmap()
        self['pixmap3'] = Pixmap()
        self['pixmap4'] = Pixmap()
        self['pixmap5'] = Pixmap()
        self['pixmap6'] = Pixmap()
        self['red'] = Button(_('Exit'))
        self['green'] = Button(_('Select'))
        self['yellow'] = Button(_('Config'))
        self['actions'] = NumberActionMap(['OkCancelActions', 'MenuActions', 'DirectionActions', 'NumberActions', 'ColorActions'], {'ok': self.okbuttonClick,
           'cancel': self.closeNonRecursive,
           'left': self.key_left,
           'right': self.key_right,
           'up': self.key_up,
           'down': self.key_down,
           'red': self.cancel,
           'green': self.okbuttonClick,
           'yellow': self.key_menu,
           'menu': self.closeRecursive,
           '1': self.keyNumberGlobal,
           '2': self.keyNumberGlobal,
           '3': self.keyNumberGlobal,
           '4': self.keyNumberGlobal,
           '5': self.keyNumberGlobal,
           '6': self.keyNumberGlobal,
           '7': self.keyNumberGlobal,
           '8': self.keyNumberGlobal,
           '9': self.keyNumberGlobal
           })
        self.index = 0
        i = 0
        self.maxentry = 29
        self.istart = 0
        i = 0
        self.onShown.append(self.openTest)

    def key_menu(self):
        pass

    def cancel(self):
        self.close()

    def paintFrame(self):
        pass

    def openTest(self):
        if self.ipage == 1:
            ii = 0
        else:
            if self.ipage == 2:
                ii = 6
            else:
                if self.ipage == 3:
                    ii = 12
                elif self.ipage == 4:
                    ii = 18
                elif self.ipage == 5:
                    ii = 24
                dxml = config.skin.primary_skin.value
                dskin = dxml.split('/')
                j = 0
                i = ii
                while j < 6:
                    j = j + 1
                    if i > self.picnum - 1:
                        icon = dskin[0] + '/blank.png'
                        name = ''
                    else:
                        name = self.tlist[i][0]
                    if 'AutoBouquetsMaker' in name:
                        name = 'AutoBouquets\nMakerProvider'
                    if len(name) > 14:
                        if '-' in name or '/' in name or ' ' in name:
                            name = name.replace('-', '/')
                            name = name.replace(' /', '/')
                            name = name.replace('/ ', '/')
                            name = name.replace(' ', '\n')
                        else:
                            name = name[:14] + '/' + name[12:]
                    if 'A/V' not in name:
                        name = name.replace('/', '\n')
                    if j == self.index + 1:
                        self['label' + str(j)].setText(' ')
                        self['label' + str(j) + 's'].setText(name)
                    else:
                        self['label' + str(j)].setText(name)
                        self['label' + str(j) + 's'].setText(' ')
                    i = i + 1

            j = 0
            i = ii
            while j < 6:
                j = j + 1
                itot = (self.ipage - 1) * 6 + j
                if itot > self.picnum:
                    icon = '/usr/share/enigma2/' + dskin[0] + '/blank.png'
                else:
                    icon = '/usr/share/enigma2/' + dskin[0] + '/buttons/icon1.png'
                pic = icon
                self['pixmap' + str(j)].instance.setPixmapFromFile(pic)
                i = i + 1

        if self.picnum > 6:
            try:
                dpointer = '/usr/share/enigma2/' + dskin[0] + '/pointer.png'
                self['pointer'].instance.setPixmapFromFile(dpointer)
            except:
                dpointer = '/usr/share/enigma2/skin_default/pointer.png'
                self['pointer'].instance.setPixmapFromFile(dpointer)

        else:
            try:
                dpointer = '/usr/share/enigma2/' + dskin[0] + '/blank.png'
                self['pointer'].instance.setPixmapFromFile(dpointer)
            except:
                dpointer = '/usr/share/enigma2/skin_default/blank.png'
                self['pointer'].instance.setPixmapFromFile(dpointer)

    def key_left(self):
        self.index -= 1
        inum = self.picnum - 1 - (self.ipage - 1) * 6
        if self.index < 0:
            if inum < 5:
                self.index = inum
            else:
                self.index = 5
        self.openTest()

    def key_right(self):
        self.index += 1
        inum = self.picnum - 1 - (self.ipage - 1) * 6
        if self.index > inum or self.index > 5:
            self.index = 0
        self.openTest()

    def key_up(self):
        self.ipage = self.ipage - 1
        if self.ipage < 1 and 7 > self.picnum > 0:
            self.ipage = 1
        elif self.ipage < 1 and 13 > self.picnum > 6:
            self.ipage = 2
        elif self.ipage < 1 and 19 > self.picnum > 12:
            self.ipage = 3
        elif self.ipage < 1 and 25 > self.picnum > 18:
            self.ipage = 4
        elif self.ipage < 1 and 31 > self.picnum > 24:
            self.ipage = 5
        self.index = 0
        self.openTest()

    def key_down(self):
        self.ipage = self.ipage + 1
        if self.ipage == 2 and 7 > self.picnum > 0:
            self.ipage = 1
        elif self.ipage == 3 and 13 > self.picnum > 6:
            self.ipage = 1
        elif self.ipage == 4 and 19 > self.picnum > 12:
            self.ipage = 1
        elif self.ipage == 5 and 25 > self.picnum > 18:
            self.ipage = 1
        elif self.ipage == 6 and 31 > self.picnum > 24:
            self.ipage = 1
        self.index = 0
        self.openTest()

    def keyNumberGlobal(self, number):
        number -= 1
        if len(self['menu'].list) > number:
            self['menu'].setIndex(number)
            self.okbuttonClick()

    def closeNonRecursive(self):
        self.close(False)

    def closeRecursive(self):
        self.close(True)

    def createSummary(self):
        pass

    def keyNumberGlobal(self, number):
        number -= 1
        if len(self['menu'].list) > number:
            self['menu'].setIndex(number)
            self.okbuttonClick()

    def closeNonRecursive(self):
        self.close(False)

    def closeRecursive(self):
        self.close(True)

    def createSummary(self):
        pass

    def okbuttonClick(self):
        if self.ipage == 1:
            idx = self.index
        elif self.ipage == 2:
            idx = self.index + 6
        elif self.ipage == 3:
            idx = self.index + 12
        elif self.ipage == 4:
            idx = self.index + 18
        elif self.ipage == 5:
            idx = self.index + 24
        if idx > self.picnum - 1:
            return
        else:
            if idx is None:
                return
            selection = self.tlist[idx]
            if selection is not None:
                selection[1]()
            return


class MainMenu(Menu):

    def __init__(self, *x):
        self.skinName = 'Menu'
        Menu.__init__(self, *x)