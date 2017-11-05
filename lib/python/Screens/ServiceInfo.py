# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Screens/ServiceInfo.py
# Compiled at: 2017-10-02 01:52:09
from Components.HTMLComponent import HTMLComponent
from Components.GUIComponent import GUIComponent
from Screen import Screen
from Components.ActionMap import ActionMap
from Components.Label import Label
from ServiceReference import ServiceReference
from enigma import eListboxPythonMultiContenteListboxgFontiServiceInformationeServiceCenter
from Tools.Transponder import ConvertToHumanReadablegetChannelNumber
import skin
RT_HALIGN_LEFT = 0
TYPE_TEXT = 0
TYPE_VALUE_HEX = 1
TYPE_VALUE_DEC = 2
TYPE_VALUE_HEX_DEC = 3
TYPE_SLIDER = 4
TYPE_VALUE_ORBIT_DEC = 5
TYPE_VALUE_FREQ = 6
TYPE_VALUE_FREQ_FLOAT = 7
TYPE_VALUE_BITRATE = 8

def to_unsigned(x):
    return x & 4294967295


def ServiceInfoListEntry(a, b='', valueType=TYPE_TEXT, param=4):
    print 'b:', b
    if not isinstance(b, str):
        if valueType == TYPE_VALUE_HEX:
            b = ('%0' + str(param) + 'X') % to_unsigned(b)
        elif valueType == TYPE_VALUE_FREQ:
            b = '%s MHz' % (b / 1000)
        elif valueType == TYPE_VALUE_FREQ_FLOAT:
            b = '%.3f MHz' % (b / 1000.0)
        elif valueType == TYPE_VALUE_BITRATE:
            b = '%s KSymbols/s' % (b / 1000)
        elif valueType == TYPE_VALUE_HEX_DEC:
            b = ('%0' + str(param) + 'X (%d)') % (to_unsigned(b), b)
        elif valueType == TYPE_VALUE_ORBIT_DEC:
            direction = 'E'
            if b > 1800:
                b = 3600 - b
                direction = 'W'
            b = '%d.%d%s' % (b // 10, b % 10, direction)
        else:
            b = str(b)
    x, y, w, h = skin.parameters.get('ServiceInfo', (0, 0, 300, 30))
    xa, ya, wa, ha = skin.parameters.get('ServiceInfoLeft', (0, 0, 300, 25))
    xb, yb, wb, hb = skin.parameters.get('ServiceInfoRight', (300, 0, 600, 25))
    if b:
        return [
         (
          eListboxPythonMultiContent.TYPE_TEXT, x, y, w, h, 0, RT_HALIGN_LEFT, ''),
         (
          eListboxPythonMultiContent.TYPE_TEXT, xa, ya, wa, ha, 0, RT_HALIGN_LEFT, a),
         (
          eListboxPythonMultiContent.TYPE_TEXT, xb, yb, wb, hb, 0, RT_HALIGN_LEFT, b)]
    else:
        return [
         (
          eListboxPythonMultiContent.TYPE_TEXT, x, y, w, h, 0, RT_HALIGN_LEFT, ''),
         (
          eListboxPythonMultiContent.TYPE_TEXT, xa, ya, wa + wb, ha + hb, 0, RT_HALIGN_LEFT, a)]


class ServiceInfoList(HTMLComponent, GUIComponent):

    def __init__(self, source):
        GUIComponent.__init__(self)
        self.l = eListboxPythonMultiContent()
        self.list = source
        self.l.setList(self.list)
        font = skin.fonts.get('ServiceInfo', ('Regular', 21, 25))
        self.l.setFont(0, gFont(font[0], font[1]))
        self.l.setItemHeight(font[2])

    GUI_WIDGET = eListbox

    def postWidgetCreate(self, instance):
        self.instance.setContent(self.l)


TYPE_SERVICE_INFO = 1
TYPE_TRANSPONDER_INFO = 2

class ServiceInfo(Screen):

    def __init__(self, session, serviceref=None):
        Screen.__init__(self, session)
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'], {'ok': self.close,
           'cancel': self.close,
           'red': self.close,
           'green': self.ShowECMInformation,
           'yellow': self.ShowServiceInformation,
           'blue': self.ShowTransponderInformation
           }, -1)
        self['infolist'] = ServiceInfoList([])
        self.setTitle(_('Service info'))
        self['key_red'] = self['red'] = Label(_('Exit'))
        self['key_green'] = self['green'] = Label(_('ECM Info'))
        self.transponder_info = self.info = self.feinfo = None
        play_service = session.nav.getCurrentlyPlayingServiceReference()
        if serviceref and not (play_service and play_service == serviceref):
            self.type = TYPE_TRANSPONDER_INFO
            self.skinName = 'ServiceInfoSimple'
            self.transponder_info = eServiceCenter.getInstance().info(serviceref).getInfoObject(serviceref, iServiceInformation.sTransponderData)
        else:
            self.type = TYPE_SERVICE_INFO
            service = session.nav.getCurrentService()
            if service:
                self.transponder_info = None
                self.info = service.info()
                self.feinfo = service.frontendInfo()
                if self.feinfo and not self.feinfo.getAll(True):
                    self.feinfo = None
                    serviceref = play_service
                    self.transponder_info = serviceref and eServiceCenter.getInstance().info(serviceref).getInfoObject(serviceref, iServiceInformation.sTransponderData)
            if self.feinfo or self.transponder_info:
                self['key_yellow'] = self['yellow'] = Label(_('Service & PIDs'))
                self['key_blue'] = self['blue'] = Label(_('Tuner setting values'))
            else:
                self.skinName = 'ServiceInfoSimple'
        self.onShown.append(self.ShowServiceInformation)
        return

    def ShowServiceInformation(self):
        if self.type == TYPE_SERVICE_INFO:
            self['Title'].text = _('Service info - service & PIDs')
            if self.feinfo or self.transponder_info:
                self['key_blue'].text = self['blue'].text = _('Tuner setting values')
            if self.session.nav.getCurrentlyPlayingServiceOrGroup():
                name = ServiceReference(self.session.nav.getCurrentlyPlayingServiceReference()).getServiceName()
                refstr = self.session.nav.getCurrentlyPlayingServiceReference().toString()
                reftype = self.session.nav.getCurrentlyPlayingServiceReference().type
            else:
                name = _('N/A')
                refstr = _('N/A')
                reftype = 0
            aspect = '-'
            videocodec = '-'
            resolution = '-'
            if self.info:
                videocodec = ('MPEG2', 'AVC', 'MPEG1', 'MPEG4-VC', 'VC1', 'VC1-SM',
                              'HEVC', 'N/A')[self.info.getInfo(iServiceInformation.sVideoType)]
                width = self.info.getInfo(iServiceInformation.sVideoWidth)
                height = self.info.getInfo(iServiceInformation.sVideoHeight)
                if width > 0 and height > 0:
                    resolution = videocodec + ' - '
                    resolution += '%dx%d - ' % (width, height)
                    resolution += str((self.info.getInfo(iServiceInformation.sFrameRate) + 500) / 1000)
                    resolution += (' i', ' p', '')[self.info.getInfo(iServiceInformation.sProgressive)]
                    aspect = self.getServiceInfoValue(iServiceInformation.sAspect)
                    aspect = aspect in (1, 2, 5, 6, 9, 10, 13, 14) and '4:3' or '16:9'
                    resolution += ' - [' + aspect + ']'
            if '%3a//' in refstr and reftype not in (1, 257, 4098, 4114):
                fillList = [
                 (
                  _('Service name'), name, TYPE_TEXT),
                 (
                  _('Videocodec, size & format'), resolution, TYPE_TEXT),
                 (
                  _('Service reference'), ':'.join(refstr.split(':')[:9]), TYPE_TEXT),
                 (
                  _('URL'), refstr.split(':')[10].replace('%3a', ':'), TYPE_TEXT)]
            else:
                if ':/' in refstr:
                    fillList = [
                     (
                      _('Service name'), name, TYPE_TEXT),
                     (
                      _('Videocodec, size & format'), resolution, TYPE_TEXT),
                     (
                      _('Service reference'), ':'.join(refstr.split(':')[:9]), TYPE_TEXT),
                     (
                      _('Filename'), refstr.split(':')[10], TYPE_TEXT)]
                else:
                    fillList = [
                     (
                      _('Service name'), name, TYPE_TEXT),
                     (
                      _('Provider'), self.getServiceInfoValue(iServiceInformation.sProvider), TYPE_TEXT),
                     (
                      _('Videocodec, size & format'), resolution, TYPE_TEXT)]
                    if '%3a//' in refstr:
                        fillList = fillList + [(_('Service reference'), ':'.join(refstr.split(':')[:9]), TYPE_TEXT),
                         (
                          _('URL'), refstr.split(':')[10].replace('%3a', ':'), TYPE_TEXT)]
                    else:
                        fillList = fillList + [(_('Service reference'), refstr, TYPE_TEXT)]
                fillList = fillList + [(_('Namespace'), self.getServiceInfoValue(iServiceInformation.sNamespace), TYPE_VALUE_HEX, 8),
                 (
                  _('Service ID'), self.getServiceInfoValue(iServiceInformation.sSID), TYPE_VALUE_HEX_DEC, 4),
                 (
                  _('Video PID'), self.getServiceInfoValue(iServiceInformation.sVideoPID), TYPE_VALUE_HEX_DEC, 4),
                 (
                  _('Audio PID'), self.getServiceInfoValue(iServiceInformation.sAudioPID), TYPE_VALUE_HEX_DEC, 4),
                 (
                  _('PCR PID'), self.getServiceInfoValue(iServiceInformation.sPCRPID), TYPE_VALUE_HEX_DEC, 4),
                 (
                  _('PMT PID'), self.getServiceInfoValue(iServiceInformation.sPMTPID), TYPE_VALUE_HEX_DEC, 4),
                 (
                  _('TXT PID'), self.getServiceInfoValue(iServiceInformation.sTXTPID), TYPE_VALUE_HEX_DEC, 4),
                 (
                  _('TSID'), self.getServiceInfoValue(iServiceInformation.sTSID), TYPE_VALUE_HEX_DEC, 4),
                 (
                  _('ONID'), self.getServiceInfoValue(iServiceInformation.sONID), TYPE_VALUE_HEX_DEC, 4)]
            self.fillList(fillList)
        elif self.transponder_info:
            self.fillList(self.getFEData(self.transponder_info))

    def ShowTransponderInformation(self):
        if self.type == TYPE_SERVICE_INFO:
            frontendData = self.feinfo and self.feinfo.getAll(True)
            if frontendData:
                if self['key_blue'].text == _('Tuner setting values'):
                    self['Title'].text = _('Service info - tuner setting values')
                    self['key_blue'].text = self['blue'].text = _('Tuner live values')
                else:
                    self['Title'].text = _('Service info - tuner live values')
                    self['key_blue'].text = self['blue'].text = _('Tuner setting values')
                    frontendData = self.feinfo.getAll(False)
                self.fillList(self.getFEData(frontendData))
            elif self.transponder_info:
                self['Title'].text = _('Service info - tuner setting values')
                self['key_blue'].text = self['blue'].text = _('Tuner setting values')
                self.fillList(self.getFEData(self.transponder_info))

    def getFEData(self, frontendDataOrg):
        if frontendDataOrg and len(frontendDataOrg):
            frontendData = ConvertToHumanReadable(frontendDataOrg)
            if self.transponder_info:
                tuner = (
                 _('Type'), frontendData['tuner_type'], TYPE_TEXT)
            else:
                tuner = (
                 _('NIM & Type'), chr(ord('A') + frontendData['tuner_number']) + ' - ' + frontendData['tuner_type'], TYPE_TEXT)
            if frontendDataOrg['tuner_type'] == 'DVB-S':
                if frontendData.get('is_id', -1) > -1:
                    return (tuner,
                     (
                      _('System & Modulation'), '%s %s' % (frontendData['system'], frontendData['modulation']), TYPE_TEXT),
                     (
                      _('Orbital position'), '%s' % frontendData['orbital_position'], TYPE_TEXT),
                     (
                      _('Frequency & Polarization'), '%s - %s' % (frontendData.get('frequency', 0), frontendData['polarization']), TYPE_TEXT),
                     (
                      _('Symbol rate & FEC'), '%s - %s' % (frontendData.get('symbol_rate', 0), frontendData['fec_inner']), TYPE_TEXT),
                     (
                      _('Input Stream ID'), '%s' % frontendData.get('is_id', -1), TYPE_TEXT),
                     (
                      _('PLS Mode & PLS Code'), '%s - %s' % (frontendData['pls_mode'], frontendData['pls_code']), TYPE_TEXT),
                     (
                      _('Inversion, Pilot & Roll-off'), '%s - %s - %s' % (frontendData['inversion'], frontendData.get('pilot', None), str(frontendData.get('rolloff', None))), TYPE_TEXT))
                else:
                    return (
                     tuner,
                     (
                      _('System & Modulation'), '%s %s' % (frontendData['system'], frontendData['modulation']), TYPE_TEXT),
                     (
                      _('Orbital position'), '%s' % frontendData['orbital_position'], TYPE_TEXT),
                     (
                      _('Frequency & Polarization'), '%s - %s' % (frontendData.get('frequency', 0), frontendData['polarization']), TYPE_TEXT),
                     (
                      _('Symbol rate & FEC'), '%s - %s' % (frontendData.get('symbol_rate', 0), frontendData['fec_inner']), TYPE_TEXT),
                     (
                      _('Inversion, Pilot & Roll-off'), '%s - %s - %s' % (frontendData['inversion'], frontendData.get('pilot', None), str(frontendData.get('rolloff', None))), TYPE_TEXT))

            else:
                if frontendDataOrg['tuner_type'] == 'DVB-C':
                    return (tuner,
                     (
                      _('Modulation'), '%s' % frontendData['modulation'], TYPE_TEXT),
                     (
                      _('Frequency'), '%s' % frontendData.get('frequency', 0), TYPE_TEXT),
                     (
                      _('Symbol rate & FEC'), '%s - %s' % (frontendData.get('symbol_rate', 0), frontendData['fec_inner']), TYPE_TEXT),
                     (
                      _('Inversion'), '%s' % frontendData['inversion'], TYPE_TEXT))
                if frontendDataOrg['tuner_type'] == 'DVB-T':
                    return (tuner,
                     (
                      _('Frequency & Channel'), '%s - Ch. %s' % (frontendData.get('frequency', 0), getChannelNumber(frontendData['frequency'], frontendData['tuner_number'])), TYPE_TEXT),
                     (
                      _('Inversion & Bandwidth'), '%s - %s' % (frontendData['inversion'], frontendData['bandwidth']), TYPE_TEXT),
                     (
                      _('Code R. LP-HP & Guard Int'), '%s - %s - %s' % (frontendData['code_rate_lp'], frontendData['code_rate_hp'], frontendData['guard_interval']), TYPE_TEXT),
                     (
                      _('Constellation & FFT mode'), '%s - %s' % (frontendData['constellation'], frontendData['transmission_mode']), TYPE_TEXT),
                     (
                      _('Hierarchy info'), '%s' % frontendData['hierarchy_information'], TYPE_TEXT))
                if frontendDataOrg['tuner_type'] == 'ATSC':
                    return (tuner,
                     (
                      _('System & Modulation'), '%s - %s' % (frontendData['system'], frontendData['modulation']), TYPE_TEXT),
                     (
                      _('Frequency'), '%s' % frontendData.get('frequency', 0), TYPE_TEXT),
                     (
                      _('Inversion'), '%s' % frontendData['inversion'], TYPE_TEXT))
        return []

    def fillList(self, Labels):
        tlist = []
        for item in Labels:
            if item[1]:
                value = item[1]
                if len(item) < 4:
                    tlist.append(ServiceInfoListEntry(item[0] + ':', value, item[2]))
                else:
                    tlist.append(ServiceInfoListEntry(item[0] + ':', value, item[2], item[3]))

        self['infolist'].l.setList(tlist)

    def getServiceInfoValue(self, what):
        if self.info:
            v = self.info.getInfo(what)
            if v == -2:
                v = self.info.getInfoString(what)
            elif v == -1:
                v = _('N/A')
            return v
        return ''

    def ShowECMInformation(self):
        if self.info:
            from Components.Converter.PliExtraInfo import caid_data
            self['Title'].text = _('Service info - ECM Info')
            tlist = []
            for caid in sorted(set(self.info.getInfoObject(iServiceInformation.sCAIDPIDs)), key=lambda x: (x[0], x[1])):
                CaIdDescription = _('Undefined')
                extra_info = ''
                provid = ''
                for caid_entry in caid_data:
                    if int(caid_entry[0], 16) <= caid[0] <= int(caid_entry[1], 16):
                        CaIdDescription = caid_entry[2]
                        break

                if caid[2]:
                    if CaIdDescription == 'Seca':
                        provid = ','.join([ caid[2][i:i + 4] for i in range(0, len(caid[2]), 30) ])
                    if CaIdDescription == 'Nagra':
                        provid = caid[2][-4:]
                    if CaIdDescription == 'Via':
                        provid = caid[2][-6:]
                    if provid:
                        extra_info = 'provid=%s' % provid
                    else:
                        extra_info = 'extra data=%s' % caid[2]
                from Tools.GetEcmInfo import GetEcmInfo
                ecmdata = GetEcmInfo().getEcmData()
                if caid[0] == int(ecmdata[1], 16) and (caid[1] == int(ecmdata[3], 16) or str(int(ecmdata[2], 16)) in provid):
                    color = '\\c00??;?00' if 1 else ''
                    tlist.append(ServiceInfoListEntry('%sECMPid %04X (%d) %04X-%s %s' % (color, caid[1], caid[1], caid[0], CaIdDescription, extra_info)))

            if not tlist:
                tlist.append(ServiceInfoListEntry(_('No ECMPids available (FTA Service)')))
            self['infolist'].l.setList(tlist)