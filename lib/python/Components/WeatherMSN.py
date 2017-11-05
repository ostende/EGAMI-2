# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/WeatherMSN.py
# Compiled at: 2017-10-02 01:56:05
from enigma import eEnveTimer
from Plugins.Extensions.WeatherPlugin.MSNWeather import MSNWeather

class WeatherMSN:
    TIMER_INTERVAL = 1800

    def __init__(self):
        self.weatherData = MSNWeather()
        self.callbacks = []
        self.callbacksAllIconsDownloaded = []
        self.timer = eTimer()
        self.timer.callback.append(self.getData)

    def getData(self):
        self.timer.stop()
        self.weatherData.getDefaultWeatherData(self.callback, self.callbackAllIconsDownloaded)
        self.timer.startLongTimer(self.TIMER_INTERVAL)

    def updateWeather(self, weather, result, errortext):
        if result == MSNWeather.OK:
            self.timer.stop()
            self.weatherData = weather
            self.weatherData.callback = None
            self.weatherData.callbackShowIcon = None
            self.weatherData.callbackAllIconsDownloaded = None
            self.callback(result, errortext)
            self.callbackAllIconsDownloaded()
            self.timer.startLongTimer(self.TIMER_INTERVAL)
        return

    def callbackAllIconsDownloaded(self):
        for x in self.callbacksAllIconsDownloaded:
            x()

    def callback(self, result, errortext):
        for x in self.callbacks:
            x(result, errortext)


weathermsn = WeatherMSN()