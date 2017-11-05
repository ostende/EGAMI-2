# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/TransponderInfo.py
# Compiled at: 2017-10-02 01:52:07
from Components.Converter.Converter import Converter
from enigma import iServiceInformationiPlayableServiceiPlayableServicePtreServiceCenter
from Components.Element import cached
from ServiceReference import resolveAlternateServiceReference
from Tools.Transponder import ConvertToHumanReadablegetChannelNumber
from Components.NimManager import nimmanager
import Screens.InfoBar

class TransponderInfo(Converter, object):

    def __init__(self, type):
        Converter.__init__(self, type)
        self.type = type.split(';')

    @cached
    def getText(self):
        service = self.source.service
        if isinstance(service, iPlayableServicePtr):
            info = service and service.info()
            ref = None
        else:
            info = service and self.source.info
            ref = service
        if not info:
            return ''
        else:
            if ref:
                nref = resolveAlternate(ref)
                if nref:
                    ref = nref
                    info = eServiceCenter.getInstance().info(ref)
                transponderraw = info.getInfoObject(ref, iServiceInformation.sTransponderData)
            else:
                transponderraw = info.getInfoObject(iServiceInformation.sTransponderData)
            if 'InRootOnly' in self.type and not self.rootBouquet():
                return ''
            if 'NoRoot' in self.type and self.rootBouquet():
                return ''
            if transponderraw:
                transponderdata = ConvertToHumanReadable(transponderraw)
                if not transponderdata['system']:
                    transponderdata['system'] = transponderraw.get('tuner_type', 'None')
                if not transponderdata['system']:
                    return ''
                if 'DVB-T' in transponderdata['system']:
                    return '%s %s %s %s' % (transponderdata['system'], transponderdata['channel'], transponderdata['frequency'], transponderdata['bandwidth'])
                if 'DVB-C' in transponderdata['system']:
                    return '%s %s %s %s %s' % (transponderdata['system'], transponderdata['frequency'], transponderdata['symbol_rate'], transponderdata['fec_inner'],
                     transponderdata['modulation'])
                return '%s %s %s %s %s %s %s' % (transponderdata['system'], transponderdata['frequency'], transponderdata['polarization_abbreviation'], transponderdata['symbol_rate'],
                 transponderdata['fec_inner'], transponderdata['modulation'], transponderdata['detailed_satpos' in self.type and 'orbital_position' or 'orb_pos'])
            if ref:
                result = ref.toString().replace('%3a', ':')
            else:
                result = info.getInfoString(iServiceInformation.sServiceref)
            if '://' in result:
                return _('Stream') + ' ' + result.rsplit('://', 1)[1].split('/')[0]
            return ''

    text = property(getText)

    def rootBouquet(self):
        servicelist = Screens.InfoBar.InfoBar.instance.servicelist
        epg_bouquet = servicelist and servicelist.getRoot()
        if ServiceReference(epg_bouquet).getServiceName():
            return False
        return True

    def changed(self, what):
        if what[0] != self.CHANGED_SPECIFIC or what[1] in (iPlayableService.evStart,):
            Converter.changed(self, what)