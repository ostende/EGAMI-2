# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Tools/LoadPixmap.py
# Compiled at: 2017-10-02 01:52:09
from enigma import loadPNGloadJPG
from Tools.LRUCache import lru_cache

def LoadPixmap(path, desktop=None, cached=False):
    if cached is None or cached:
        ret = _cached_load(path, desktop)
        return ret
    else:
        return _load(path, desktop)
        return


@lru_cache(maxsize=256)
def _cached_load(path, desktop):
    return _load(path, desktop)


def _load(path, desktop):
    if path[-4:] == '.png':
        ptr = loadPNG(path)
    elif path[-4:] == '.jpg':
        ptr = loadJPG(path)
    elif path[-1:] == '.':
        alpha = loadPNG(path + 'a.png')
        ptr = loadJPG(path + 'rgb.jpg', alpha)
    else:
        raise Exception('neither .png nor .jpg, please fix file extension')
    if ptr and desktop:
        desktop.makeCompatiblePixmap(ptr)
    return ptr