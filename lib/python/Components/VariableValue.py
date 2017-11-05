# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/VariableValue.py
# Compiled at: 2017-10-02 01:52:08


class VariableValue(object):

    def __init__(self):
        self.__value = 0

    def setValue(self, value):
        self.__value = value
        if self.instance:
            try:
                self.instance.setValue(self.__value)
            except (TypeError, OverflowError) as e:
                print '[VariableValue::setValue] exception', type(e), 'handled'
                self.instance.setValue(0)

    def getValue(self):
        return self.__value

    def postWidgetCreate(self, instance):
        print self
        print self.GUI_WIDGET
        self.instance.setValue(self.__value)

    value = property(getValue, setValue)