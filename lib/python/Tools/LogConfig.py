# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Tools/LogConfig.py
# Compiled at: 2017-10-02 01:52:09
LOG_TYPE_DEBUG = 'D/ '
LOG_TYPE_INFO = 'I/ '
LOG_TYPE_WARNING = 'W/ '
LOG_TYPE_ERROR = 'E/ '
LOG_LEVEL_ERROR = 0
LOG_LEVEL_WARNING = 1
LOG_LEVEL_INFO = 2
LOG_LEVEL_DEBUG = 3

class LogConfig(object):
    _initialized = False

    @staticmethod
    def init():
        if LogConfig._initialized:
            return
        from Components.config import configConfigSubsectionConfigOnOffConfigSelection
        config.log = ConfigSubsection()
        config.log.level = ConfigSelection(choices={str(LOG_LEVEL_DEBUG): 'DEBUG',str(LOG_LEVEL_INFO): 'INFO',str(LOG_LEVEL_WARNING): 'WARNING',str(LOG_LEVEL_ERROR): 'ERROR'}, default=str(LOG_LEVEL_INFO))
        config.log.verbose = ConfigOnOff(default=False)
        config.log.colored = ConfigOnOff(default=True)
        LogConfig._initialized = True

    @staticmethod
    def level():
        from Components.config import config
        return int(config.log.level.value)

    @staticmethod
    def verbose():
        from Components.config import config
        return config.log.verbose.value

    @staticmethod
    def colored():
        from Components.config import config
        return config.log.colored.value