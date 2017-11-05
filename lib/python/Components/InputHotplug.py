# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/InputHotplug.py
# Compiled at: 2017-10-02 01:52:08
import Netlink
import enigma
import os

class NetlinkReader:

    def __init__(self):
        from twisted.internet import reactor
        self.nls = Netlink.NetlinkSocket()
        reactor.addReader(self)

    def fileno(self):
        return self.nls.fileno()

    def doRead(self):
        for event in self.nls.parse():
            try:
                subsystem = event['SUBSYSTEM']
                if subsystem == 'input':
                    devname = event['DEVNAME']
                    action = event['ACTION']
                    if action == 'add':
                        print '[InputHotplug] New input device detected:', devname
                        enigma.addInputDevice(os.path.join('/dev', devname))
                    elif action == 'remove':
                        print '[InputHotplug] Removed input device:', devname
                        enigma.removeInputDevice(os.path.join('/dev', devname))
                elif subsystem == 'net':
                    from Network import iNetwork
                    iNetwork.hotplug(event)
            except KeyError:
                pass

    def connectionLost(self, failure):
        print '[InputHotplug] connectionLost?', failure
        self.nls.close()

    def logPrefix(self):
        return 'NetlinkReader'


reader = NetlinkReader()