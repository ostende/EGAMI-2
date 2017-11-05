# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Screens/InstallWizard.py
# Compiled at: 2017-10-02 01:52:09
from Screens.Screen import Screen
from Components.ConfigList import ConfigListScreen
from Components.Sources.StaticText import StaticText
from Components.config import configConfigSubsectionConfigBooleangetConfigListEntryConfigSelectionConfigYesNoConfigIP
from Components.Network import iNetwork
from Components.Ipkg import IpkgComponent
from enigma import eDVBDB
import os
from boxbranding import getBoxType
from EGAMI.EGAMI_tools import getStbArch
config.misc.installwizard = ConfigSubsection()
config.misc.installwizard.hasnetwork = ConfigBoolean(default=False)
config.misc.installwizard.ipkgloaded = ConfigBoolean(default=False)
config.misc.installwizard.channellistdownloaded = ConfigBoolean(default=False)

class InstallWizard(Screen, ConfigListScreen):
    STATE_UPDATE = 0
    STATE_CHOISE_CHANNELLIST = 1
    STATE_CHOISE_SOFTCAM = 2

    def __init__(self, session, args=None):
        Screen.__init__(self, session)
        self.index = args
        self.list = []
        ConfigListScreen.__init__(self, self.list)
        self.ipConfigEntry = ConfigIP(default=[0, 0, 0, 0])
        self.interface = 'eth0'
        if self.index == self.STATE_UPDATE:
            config.misc.installwizard.hasnetwork.value = False
            config.misc.installwizard.ipkgloaded.value = False
            modes = {0: ' '}
            self.enabled = ConfigSelection(choices=modes, default=0)
            self.adapters = [ (iNetwork.getFriendlyAdapterName(x), x) for x in iNetwork.getAdapterList() ]
            is_found = False
            for x in self.adapters:
                if x[1] == 'eth0':
                    if iNetwork.getAdapterAttribute(x[1], 'up'):
                        self.ipConfigEntry = ConfigIP(default=iNetwork.getAdapterAttribute(x[1], 'ip'))
                        iNetwork.checkNetworkState(self.checkNetworkCB)
                        if_found = True
                        self.interface = x[1]
                    else:
                        iNetwork.restartNetwork(self.checkNetworkLinkCB)
                    break

            if is_found is False:
                self.createMenu()
        elif self.index == self.STATE_CHOISE_CHANNELLIST:
            self.enabled = ConfigYesNo(default=True)
            modes = {'henksat-19e': 'Astra 1','henksat-23e': 'Astra 3','henksat-19e-23e': 'Astra 1 Astra 3','henksat-19e-23e-28e': 'Astra 1 Astra 2 Astra 3','henksat-13e-19e-23e-28e': 'Astra 1 Astra 2 Astra 3 Hotbird'}
            self.channellist_type = ConfigSelection(choices=modes, default='henksat-13e-19e-23e-28e')
            self.createMenu()
        elif self.index == self.STATE_CHOISE_SOFTCAM:
            self.enabled = ConfigYesNo(default=True)
            if getStbArch() in 'armv7ahf':
                modes = {'oscam': _('default') + ' OSCam','oscam2': 'OScam MOD','wicardd': 'Wicardd','gbox': 'GBox'}
            elif getStbArch() in 'meson-6':
                modes = {'oscam': _('default') + ' OSCam'}
            else:
                modes = {'oscam': _('default') + ' OSCam','cccam': 'CCcam','gbox': 'GBox','oscam2': 'OScam MOD','wicardd': 'Wicardd','mgcamd': 'MGCamd'}
            self.softcam_type = ConfigSelection(choices=modes, default='oscam')
            self.createMenu()

    def checkNetworkCB(self, data):
        if data < 3:
            config.misc.installwizard.hasnetwork.value = True
        self.createMenu()

    def checkNetworkLinkCB(self, retval):
        if retval:
            iNetwork.checkNetworkState(self.checkNetworkCB)
        else:
            self.createMenu()

    def createMenu(self):
        self.list = []
        try:
            test = self.index
        except:
            return

        if self.index == self.STATE_UPDATE:
            if config.misc.installwizard.hasnetwork.value:
                self.ipConfigEntry = ConfigIP(default=iNetwork.getAdapterAttribute(self.interface, 'ip'))
                self.list.append(getConfigListEntry(_('Your internet connection is working (ip: %s)') % self.ipConfigEntry.getText(), self.enabled))
            else:
                self.list.append(getConfigListEntry(_('Your receiver does not have an internet connection'), self.enabled))
        elif self.index == self.STATE_CHOISE_CHANNELLIST:
            self.list.append(getConfigListEntry(_('Install channel list'), self.enabled))
            if self.enabled.value:
                self.list.append(getConfigListEntry(_('Channel list type'), self.channellist_type))
        elif self.index == self.STATE_CHOISE_SOFTCAM:
            self.list.append(getConfigListEntry(_('Install softcam'), self.enabled))
            if self.enabled.value:
                self.list.append(getConfigListEntry(_('Softcam type'), self.softcam_type))
        self['config'].list = self.list
        self['config'].l.setList(self.list)

    def keyLeft(self):
        if self.index == 0:
            return
        ConfigListScreen.keyLeft(self)
        self.createMenu()

    def keyRight(self):
        if self.index == 0:
            return
        ConfigListScreen.keyRight(self)
        self.createMenu()

    def run(self):
        if self.index == self.STATE_UPDATE:
            if config.misc.installwizard.hasnetwork.value:
                self.session.open(InstallWizardIpkgUpdater, self.index, _('Please wait (updating packages)'), IpkgComponent.CMD_UPDATE)
        elif self.index == self.STATE_CHOISE_CHANNELLIST and self.enabled.value:
            self.session.open(InstallWizardIpkgUpdater, self.index, _('Please wait (downloading channel list)'), IpkgComponent.CMD_REMOVE, {'package': 'enigma2-plugin-settings-' + self.channellist_type.value})
        elif self.index == self.STATE_CHOISE_SOFTCAM and self.enabled.value:
            softcam_name = self.softcam_type.value
            if softcam_name == 'cccam':
                cmd = ';rm /tmp/Addon.tgz;wget -q http://egami-feed.com/plugins/mipsel/softcams_full_mipsel/cccam_230_egami_E2_sh.tar.gz -O /tmp/Addon.tgz'
            elif softcam_name == 'wicardd':
                if getStbArch() in 'armv7ahf':
                    cmd = ';rm /tmp/Addon.tgz;wget -q http://egami-feed.com/plugins/armv7ahf/softcams_full_armv7ahf/wicardd_119_egami_E2_armv7ahf_sh.tar.gz -O /tmp/Addon.tgz'
                else:
                    cmd = ';rm /tmp/Addon.tgz;wget -q http://egami-feed.com/plugins/mipsel/softcams_full_mipsel/wicardd_118_egami_E2_sh.tar.gz -O /tmp/Addon.tgz'
            elif softcam_name == 'gbox':
                if getStbArch() in 'armv7ahf':
                    cmd = ';rm /tmp/Addon.tgz;wget -q http://egami-feed.com/plugins/armv7ahf/softcams_full_armv7ahf/gbox_811k_egami_E2_armv7ahf_sh.tar.gz -O /tmp/Addon.tgz'
                else:
                    cmd = ';rm /tmp/Addon.tgz;wget -q http://egami-feed.com/plugins/mipsel/softcams_full_mipsel/gbox_811K_egami_E2_sh.tar.gz -O /tmp/Addon.tgz'
            elif softcam_name == 'mgcamd':
                cmd = ';rm /tmp/Addon.tgz;wget -q http://egami-feed.com/plugins/mipsel/softcams_full_mipsel/mgcamd_138c_egami_E2_sh.tar.gz -O /tmp/Addon.tgz'
            elif softcam_name == 'oscam':
                if getStbArch() in 'armv7ahf':
                    cmd = ';rm /tmp/Addon.tgz;wget -q http://egami-feed.com/plugins/armv7ahf/softcams_full_armv7ahf/oscam_11225_egami_E2_armv7ahf_sh.tar.gz -O /tmp/Addon.tgz'
                elif getStbArch() in 'meson-6':
                    cmd = ';rm /tmp/Addon.tgz;wget -q http://egami-feed.com/plugins/cortexa9hf/softcams_cfg_cortexa9hf/oscam_10943_egami_E2_cortexa9hf_sh.tar.gz -O /tmp/Addon.tgz'
                else:
                    cmd = ';rm /tmp/Addon.tgz;wget -q http://egami-feed.com/plugins/mipsel/softcams_full_mipsel/oscam_11214_egami_E2_sh.tar.gz -O /tmp/Addon.tgz'
            elif softcam_name == 'oscam2':
                if getStbArch() in 'armv7ahf':
                    cmd = ';rm /tmp/Addon.tgz;wget -q http://egami-feed.com/plugins/armv7ahf/softcams_full_armv7ahf/Oscam-RuBeN-4K.tar.gz -O /tmp/Addon.tgz'
                elif getStbArch() in 'meson-6':
                    cmd = ';rm /tmp/Addon.tgz;wget -q http://egami-feed.com/plugins/cortexa9hf/softcams_cfg_cortexa9hf/oscam_10943_egami_E2_cortexa9hf_sh.tar.gz -O /tmp/Addon.tgz'
                else:
                    cmd = ';rm /tmp/Addon.tgz;wget -q http://egami-feed.com/plugins/mipsel/softcams_full_mipsel/oscam-rubeni_egami.tar.gz -O /tmp/Addon.tgz'
            cmd += ';cd /; tar -xz -f /tmp/Addon.tgz ; rm /tmp/Addon.tgz'
            self.session.open(InstallWizardIpkgUpdater, self.index, _('Please wait (downloading softcam)'), IpkgComponent.CMD_INSTALL, {'package': cmd})


class InstallWizardIpkgUpdater(Screen):

    def __init__(self, session, index, info, cmd, pkg=None):
        Screen.__init__(self, session)
        self['statusbar'] = StaticText(info)
        self.pkg = pkg
        self.index = index
        self.state = 0
        self.ipkg = IpkgComponent()
        self.ipkg.addCallback(self.ipkgCallback)
        if self.index == InstallWizard.STATE_CHOISE_CHANNELLIST:
            self.ipkg.startCmd(cmd, {'package': 'enigma2-plugin-settings-*'})
        else:
            self.ipkg.startCmd(cmd, pkg)

    def ipkgCallback(self, event, param):
        if event == IpkgComponent.EVENT_DONE:
            if self.index == InstallWizard.STATE_UPDATE:
                config.misc.installwizard.ipkgloaded.value = True
            elif self.index == InstallWizard.STATE_CHOISE_CHANNELLIST:
                if self.state == 0:
                    self.ipkg.startCmd(IpkgComponent.CMD_INSTALL, self.pkg)
                    self.state = 1
                    return
                config.misc.installwizard.channellistdownloaded.value = True
                eDVBDB.getInstance().reloadBouquets()
                eDVBDB.getInstance().reloadServicelist()
            self.close()