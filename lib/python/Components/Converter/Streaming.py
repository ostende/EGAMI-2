# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/Streaming.py
# Compiled at: 2017-10-02 01:52:07
from Converter import Converter
from Components.Element import cached

class Streaming(Converter):

    @cached
    def getText(self):
        service = self.source.service
        if service is None:
            return '-NO SERVICE\n'
        else:
            streaming = service.stream()
            s = streaming and streaming.getStreamingData()
            if s is None or not any(s):
                err = service.getError()
                if err:
                    return '-SERVICE ERROR:%d\n' % err
                else:
                    return '=NO STREAM\n'

            demux = s['demux']
            pids = ','.join([ '%x:%s' % (x[0], x[1]) for x in s['pids'] ])
            return '+%d:%s\n' % (demux, pids)

    text = property(getText)