# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Netlink.py
# Compiled at: 2017-10-02 01:52:08
import os
import socket

class NetlinkSocket(socket.socket):

    def __init__(self):
        NETLINK_KOBJECT_UEVENT = 15
        socket.socket.__init__(self, socket.AF_NETLINK, socket.SOCK_DGRAM, NETLINK_KOBJECT_UEVENT)
        self.bind((os.getpid(), -1))

    def parse(self):
        data = self.recv(512)
        event = {}
        for item in data.split('\x00'):
            if not item:
                yield event
                event = {}
            else:
                try:
                    k, v = item.split('=', 1)
                    event[k] = v
                except:
                    event[None] = item

        return


if __name__ == '__main__':
    nls = NetlinkSocket()
    print 'socket no:', nls.fileno()
    while 1:
        for item in nls.parse():
            print repr(item)