# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Tools/MovieInfoParser.py
# Compiled at: 2017-10-02 01:52:09
from os import path

def getExtendedMovieDescription(ref):
    f = None
    extended_desc = ''
    name = ''
    extensions = ('.txt', '.info')
    info_file = path.realpath(ref.getPath())
    name = path.basename(info_file)
    ext_pos = name.rfind('.')
    if ext_pos > 0:
        name = name[:ext_pos].replace('_', ' ')
    else:
        name = name.replace('_', ' ')
    for ext in extensions:
        if path.exists(info_file + ext):
            f = info_file + ext
            break

    if not f:
        ext_pos = info_file.rfind('.')
        name_len = len(info_file)
        ext_len = name_len - ext_pos
        if ext_len <= 5:
            info_file = info_file[:ext_pos]
            for ext in extensions:
                if path.exists(info_file + ext):
                    f = info_file + ext
                    break

    if f:
        with open(f, 'r') as txtfile:
            extended_desc = txtfile.read()
    return (name, extended_desc)