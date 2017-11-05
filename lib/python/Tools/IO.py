# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Tools/IO.py
# Compiled at: 2017-10-02 01:52:09
from os import fchmodfsyncpathrenameunlink
from tempfile import NamedTemporaryFile

def saveFile(filename, data, mode=420):
    tmpFilename = None
    try:
        f = NamedTemporaryFile(prefix='.%s.' % path.basename(filename), dir=path.dirname(filename), delete=False)
        tmpFilename = f.name
        if isinstance(data, list):
            for x in data:
                f.write(x)

        else:
            f.write(data)
        f.flush()
        fsync(f.fileno())
        fchmod(f.fileno(), mode)
        f.close()
        rename(tmpFilename, filename)
    except Exception as e:
        print 'saveFile: failed to write to %s: %s' % (filename, e)
        if tmpFilename and path.exists(tmpFilename):
            unlink(tmpFilename)
        return False

    return True