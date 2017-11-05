# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Tools/Notifications.py
# Compiled at: 2017-10-02 01:52:09
notifications = []
notificationAdded = []
current_notifications = []

def __AddNotification(fnc, screen, id, *args, **kwargs):
    if ".MessageBox'>" in `screen`:
        kwargs['simple'] = True
    notifications.append((fnc, screen, args, kwargs, id))
    for x in notificationAdded:
        x()


def AddNotification(screen, *args, **kwargs):
    AddNotificationWithCallback(None, screen, *args, **kwargs)
    return


def AddNotificationWithCallback(fnc, screen, *args, **kwargs):
    __AddNotification(fnc, screen, None, *args, **kwargs)
    return


def AddNotificationParentalControl(fnc, screen, *args, **kwargs):
    RemovePopup('Parental control')
    __AddNotification(fnc, screen, 'Parental control', *args, **kwargs)


def AddNotificationWithID(id, screen, *args, **kwargs):
    __AddNotification(None, screen, id, *args, **kwargs)
    return


def AddNotificationWithIDCallback(fnc, id, screen, *args, **kwargs):
    __AddNotification(fnc, screen, id, *args, **kwargs)


def RemovePopup(id):
    print '[Notifications] RemovePopup, id =', id
    for x in notifications:
        if x[4] and x[4] == id:
            print '(found in notifications)'
            notifications.remove(x)

    for x in current_notifications:
        if x[0] == id:
            print '(found in current notifications)'
            x[1].close()


from Screens.MessageBox import MessageBox

def AddPopup(text, type, timeout, id=None):
    if id is not None:
        RemovePopup(id)
    print '[Notifications] AddPopup, id =', id
    AddNotificationWithID(id, MessageBox, text=text, type=type, timeout=timeout, close_on_any_key=True)
    return


def AddPopupWithCallback(fnc, text, type, timeout, id=None):
    if id is not None:
        RemovePopup(id)
    print '[Notifications] AddPopup, id =', id
    AddNotificationWithIDCallback(fnc, id, MessageBox, text=text, type=type, timeout=timeout, close_on_any_key=False)
    return