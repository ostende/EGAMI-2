# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Tools/Log.py
# Compiled at: 2017-10-02 01:52:09
from sys import _getframe
from LogConfig import LogConfigLOG_TYPE_DEBUGLOG_TYPE_INFOLOG_TYPE_WARNINGLOG_TYPE_ERRORLOG_LEVEL_ERRORLOG_LEVEL_WARNINGLOG_LEVEL_INFOLOG_LEVEL_DEBUG

class Log(object):

    @staticmethod
    def e(text=''):
        LogConfig.init()
        if LogConfig.level() >= LOG_LEVEL_ERROR:
            callframe = _getframe(1)
            Log._log(LOG_TYPE_ERROR, text, callframe)

    @staticmethod
    def w(text=''):
        LogConfig.init()
        if LogConfig.level() >= LOG_LEVEL_WARNING:
            callframe = _getframe(1)
            Log._log(LOG_TYPE_WARNING, text, callframe)

    @staticmethod
    def i(text=''):
        LogConfig.init()
        if LogConfig.level() >= LOG_LEVEL_INFO:
            callframe = _getframe(1)
            Log._log(LOG_TYPE_INFO, text, callframe)

    @staticmethod
    def d(text=''):
        LogConfig.init()
        if LogConfig.level() >= LOG_LEVEL_DEBUG:
            callframe = _getframe(1)
            Log._log(LOG_TYPE_DEBUG, text, callframe)

    @staticmethod
    def _log(type, text, callframe=None):
        LogConfig.init()
        if callframe is None:
            callframe = _getframe(1)
        func = callframe.f_code.co_name
        cls = callframe.f_locals.get('self', None)
        msg = ''
        if not text:
            text = '<no detail>'
        if cls != None:
            cls = cls.__class__.__name__
            msg = '%s [%s.%s] :: %s' % (type, cls, func, text)
        else:
            msg = '%s [%s] :: %s' % (type, func, text)
        if LogConfig.verbose():
            line = callframe.f_lineno
            filename = callframe.f_code.co_filename
            msg = '%s {%s:%s}' % (msg, filename, line)
        if LogConfig.colored():
            if type == LOG_TYPE_ERROR:
                msg = '\x1b[0;31m%s\x1b[1;m' % msg
            elif type == LOG_TYPE_WARNING:
                msg = '\x1b[1;33m%s\x1b[1;m' % msg
            elif type == LOG_TYPE_DEBUG:
                msg = '\x1b[0;37m%s\x1b[1;m' % msg
        print msg
        return