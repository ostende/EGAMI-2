# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/MovieReference.py
# Compiled at: 2017-10-02 01:52:07
from Components.Converter.Converter import Converter
from Components.Element import cached
from enigma import iServiceInformationeServiceReferenceiPlayableServicePtr

class MovieReference(Converter, object):

    def __init__(self, type):
        Converter.__init__(self, type)

    @cached
    def getText(self):
        service = self.source.service
        if isinstance(service, eServiceReference):
            info = self.source.info
        elif isinstance(service, iPlayableServicePtr):
            info = service.info()
            service = None
        else:
            info = None
        if info is None:
            return ''
        else:
            if service is None:
                refstr = info.getInfoString(iServiceInformation.sServiceref)
                path = refstr and eServiceReference(refstr).getPath()
                if path:
                    try:
                        fd = open('%s.meta' % path, 'r')
                        refstr = fd.readline().strip()
                        fd.close()
                    except:
                        pass

                return refstr
            return info.getInfoString(service, iServiceInformation.sServiceref)
            return

    text = property(getText)