# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Tools/Alternatives.py
# Compiled at: 2017-10-02 01:52:09
from enigma import eServiceCentereServiceReference

def getAlternativeChannels(service):
    alternativeServices = eServiceCenter.getInstance().list(eServiceReference(service))
    return alternativeServices and alternativeServices.getContent('S', True)


def CompareWithAlternatives(serviceA, serviceB):
    return serviceA and serviceB and (serviceA == serviceB or serviceA.startswith('1:134:') and serviceB in getAlternativeChannels(serviceA) or serviceB.startswith('1:134:') and serviceA in getAlternativeChannels(serviceB))


def GetWithAlternative(service):
    if service.startswith('1:134:'):
        channels = getAlternativeChannels(service)
        if channels:
            return channels[0]
    return service