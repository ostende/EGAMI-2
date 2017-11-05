# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/ResourceManager.py
# Compiled at: 2017-10-02 01:52:08


class ResourceManager:

    def __init__(self):
        self.resourceList = {}

    def addResource(self, name, resource):
        print '[ResourceManager] adding Resource', name
        self.resourceList[name] = resource
        print '[ResourceManager] resources:', self.resourceList

    def getResource(self, name):
        if not self.hasResource(name):
            return None
        else:
            return self.resourceList[name]

    def hasResource(self, name):
        return self.resourceList.has_key(name)

    def removeResource(self, name):
        if self.hasResource(name):
            del self.resourceList[name]


resourcemanager = ResourceManager()