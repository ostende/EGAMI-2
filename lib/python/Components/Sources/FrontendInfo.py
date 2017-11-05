# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Sources/FrontendInfo.py
# Compiled at: 2017-10-02 01:52:07
from enigma import iPlayableService
from Source import Source
from Components.PerServiceDisplay import PerServiceBase
from enigma import eDVBResourceManager

class FrontendInfo(Source, PerServiceBase):

    def __init__(self, service_source=None, frontend_source=None, navcore=None):
        self.navcore = None
        Source.__init__(self)
        if navcore:
            PerServiceBase.__init__(self, navcore, {iPlayableService.evTunedIn: self.updateFrontendData,
               iPlayableService.evEnd: self.serviceEnd
               })
        res_mgr = eDVBResourceManager.getInstance()
        if res_mgr:
            res_mgr.frontendUseMaskChanged.get().append(self.updateTunerMask)
        self.service_source = service_source
        self.frontend_source = frontend_source
        self.tuner_mask = 0
        self.updateFrontendData()
        return

    def serviceEnd(self):
        self.slot_number = self.frontend_type = None
        self.changed((self.CHANGED_CLEAR,))
        return

    def updateFrontendData(self):
        data = self.getFrontendData()
        if not data:
            self.slot_number = self.frontend_type = None
        else:
            self.slot_number = data.get('tuner_number')
            self.frontend_type = data.get('tuner_type')
        self.changed((self.CHANGED_ALL,))
        return

    def updateTunerMask(self, mask):
        self.tuner_mask = mask
        self.changed((self.CHANGED_ALL,))

    def getFrontendData(self):
        if self.frontend_source:
            frontend = self.frontend_source()
            dict = {}
            if frontend:
                frontend.getFrontendData(dict)
            return dict
        else:
            if self.service_source:
                service = self.navcore and self.service_source()
                feinfo = service and service.frontendInfo()
                return feinfo and feinfo.getFrontendData()
            if self.navcore:
                service = self.navcore.getCurrentService()
                feinfo = service and service.frontendInfo()
                return feinfo and feinfo.getFrontendData()
            return None
            return None

    def destroy(self):
        if not self.frontend_source and not self.service_source:
            PerServiceBase.destroy(self)
        res_mgr = eDVBResourceManager.getInstance()
        if res_mgr:
            res_mgr.frontendUseMaskChanged.get().remove(self.updateTunerMask)
        Source.destroy(self)