# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/MovieInfo.py
# Compiled at: 2017-10-02 01:52:07
from Components.Converter.Converter import Converter
from Components.Element import cachedElementError
from enigma import iServiceInformationeServiceReference
from ServiceReference import ServiceReference

class MovieInfo(Converter, object):
    MOVIE_SHORT_DESCRIPTION = 0
    MOVIE_META_DESCRIPTION = 1
    MOVIE_REC_SERVICE_NAME = 2
    MOVIE_REC_SERVICE_REF = 3
    MOVIE_REC_FILESIZE = 4

    def __init__(self, type):
        if type == 'ShortDescription':
            self.type = self.MOVIE_SHORT_DESCRIPTION
        elif type == 'MetaDescription':
            self.type = self.MOVIE_META_DESCRIPTION
        elif type == 'RecordServiceName':
            self.type = self.MOVIE_REC_SERVICE_NAME
        elif type == 'FileSize':
            self.type = self.MOVIE_REC_FILESIZE
        elif type in ('RecordServiceRef', 'Reference'):
            self.type = self.MOVIE_REC_SERVICE_REF
        else:
            raise ElementError("'%s' is not <ShortDescription|MetaDescription|RecordServiceName|FileSize> for MovieInfo converter" % type)
        Converter.__init__(self, type)

    @cached
    def getText(self):
        service = self.source.service
        info = self.source.info
        event = self.source.event
        if info and service:
            if self.type == self.MOVIE_SHORT_DESCRIPTION:
                if service.flags & eServiceReference.flagDirectory == eServiceReference.flagDirectory:
                    return service.getPath()
                return info.getInfoString(service, iServiceInformation.sDescription) or event and event.getShortDescription() or service.getPath()
            if self.type == self.MOVIE_META_DESCRIPTION:
                return event and (event.getExtendedDescription() or event.getShortDescription()) or info.getInfoString(service, iServiceInformation.sDescription) or service.getPath()
            if self.type == self.MOVIE_REC_SERVICE_NAME:
                rec_ref_str = info.getInfoString(service, iServiceInformation.sServiceref)
                return ServiceReference(rec_ref_str).getServiceName()
            if self.type == self.MOVIE_REC_SERVICE_REF:
                rec_ref_str = info.getInfoString(service, iServiceInformation.sServiceref)
                return str(ServiceReference(rec_ref_str))
            if self.type == self.MOVIE_REC_FILESIZE:
                if service.flags & eServiceReference.flagDirectory == eServiceReference.flagDirectory:
                    return _('Directory')
                filesize = info.getInfoObject(service, iServiceInformation.sFileSize)
                if filesize is not None:
                    if filesize >= 104857600000:
                        return _('%.0f GB') % (filesize / 1073741824.0)
                    else:
                        if filesize >= 102400000:
                            return _('%.2f GB') % (filesize / 1073741824.0)
                        return _('%.0f MB') % (filesize / 1048576.0)

        return ''

    text = property(getText)