# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Tools/BoundFunction.py
# Compiled at: 2017-10-02 01:52:09


class boundFunction:

    def __init__(self, fnc, *args, **kwargs):
        self.fnc = fnc
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        newkwargs = self.kwargs
        newkwargs.update(kwargs)
        return self.fnc(*(self.args + args), **newkwargs)