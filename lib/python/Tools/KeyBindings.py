# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Tools/KeyBindings.py
# Compiled at: 2017-10-02 01:52:09
keyBindings = {}
from keyids import KEYIDS
from Components.config import config
from Components.RcModel import rc_model
keyDescriptions = [
 {KEYIDS['BTN_0']: ('UP', 'fp'),
    KEYIDS['BTN_1']: ('DOWN', 'fp'),
    KEYIDS['KEY_OK']: ('OK', ''),
    KEYIDS['KEY_UP']: ('UP', ),
    KEYIDS['KEY_DOWN']: ('DOWN', ),
    KEYIDS['KEY_POWER']: ('POWER', ),
    KEYIDS['KEY_RED']: ('RED', ),
    KEYIDS['KEY_BLUE']: ('BLUE', ),
    KEYIDS['KEY_GREEN']: ('GREEN', ),
    KEYIDS['KEY_YELLOW']: ('YELLOW', ),
    KEYIDS['KEY_MENU']: ('MENU', ),
    KEYIDS['KEY_LEFT']: ('LEFT', ),
    KEYIDS['KEY_RIGHT']: ('RIGHT', ),
    KEYIDS['KEY_VIDEO']: ('PVR', ),
    KEYIDS['KEY_INFO']: ('INFO', ),
    KEYIDS['KEY_AUDIO']: ('YELLOW', ),
    KEYIDS['KEY_TV']: ('TV', ),
    KEYIDS['KEY_RADIO']: ('RADIO', ),
    KEYIDS['KEY_TEXT']: ('TEXT', ),
    KEYIDS['KEY_NEXT']: ('ARROWRIGHT', ),
    KEYIDS['KEY_PREVIOUS']: ('ARROWLEFT', ),
    KEYIDS['KEY_PREVIOUSSONG']: ('REWIND', ),
    KEYIDS['KEY_PLAYPAUSE']: ('PLAYPAUSE', ),
    KEYIDS['KEY_PLAY']: ('PLAYPAUSE', ),
    KEYIDS['KEY_NEXTSONG']: ('FASTFORWARD', ),
    KEYIDS['KEY_CHANNELUP']: ('BOUQUET+', ),
    KEYIDS['KEY_CHANNELDOWN']: ('BOUQUET-', ),
    KEYIDS['KEY_0']: ('0', ),
    KEYIDS['KEY_1']: ('1', ),
    KEYIDS['KEY_2']: ('2', ),
    KEYIDS['KEY_3']: ('3', ),
    KEYIDS['KEY_4']: ('4', ),
    KEYIDS['KEY_5']: ('5', ),
    KEYIDS['KEY_6']: ('6', ),
    KEYIDS['KEY_7']: ('7', ),
    KEYIDS['KEY_8']: ('8', ),
    KEYIDS['KEY_9']: ('9', ),
    KEYIDS['KEY_EXIT']: ('EXIT', ),
    KEYIDS['KEY_STOP']: ('STOP', ),
    KEYIDS['KEY_RECORD']: ('RECORD', )
    },
 {KEYIDS['BTN_0']: ('UP', 'fp'),
    KEYIDS['BTN_1']: ('DOWN', 'fp'),
    KEYIDS['KEY_OK']: ('OK', ''),
    KEYIDS['KEY_UP']: ('UP', ),
    KEYIDS['KEY_DOWN']: ('DOWN', ),
    KEYIDS['KEY_POWER']: ('POWER', ),
    KEYIDS['KEY_RED']: ('RED', ),
    KEYIDS['KEY_BLUE']: ('BLUE', ),
    KEYIDS['KEY_GREEN']: ('GREEN', ),
    KEYIDS['KEY_YELLOW']: ('YELLOW', ),
    KEYIDS['KEY_MENU']: ('MENU', ),
    KEYIDS['KEY_LEFT']: ('LEFT', ),
    KEYIDS['KEY_RIGHT']: ('RIGHT', ),
    KEYIDS['KEY_VIDEO']: ('VIDEO', ),
    KEYIDS['KEY_INFO']: ('INFO', ),
    KEYIDS['KEY_EPG']: ('EPG', ),
    KEYIDS['KEY_AUDIO']: ('AUDIO', ),
    KEYIDS['KEY_TV']: ('TV', ),
    KEYIDS['KEY_RADIO']: ('RADIO', ),
    KEYIDS['KEY_TEXT']: ('TEXT', ),
    KEYIDS['KEY_NEXT']: ('ARROWRIGHT', ),
    KEYIDS['KEY_PREVIOUS']: ('ARROWLEFT', ),
    KEYIDS['KEY_PREVIOUSSONG']: 'PREVIOUSSKIP',
    KEYIDS['KEY_PLAYPAUSE']: 'PLAYPAUSE',
    KEYIDS['KEY_PLAY']: 'PLAY',
    KEYIDS['KEY_NEXTSONG']: 'NEXTSKIP',
    KEYIDS['KEY_CHANNELUP']: ('CH+', ),
    KEYIDS['KEY_CHANNELDOWN']: ('CH-', ),
    KEYIDS['KEY_0']: ('0', ),
    KEYIDS['KEY_1']: ('1', ),
    KEYIDS['KEY_2']: ('2', ),
    KEYIDS['KEY_3']: ('3', ),
    KEYIDS['KEY_4']: ('4', ),
    KEYIDS['KEY_5']: ('5', ),
    KEYIDS['KEY_6']: ('6', ),
    KEYIDS['KEY_7']: ('7', ),
    KEYIDS['KEY_8']: ('8', ),
    KEYIDS['KEY_9']: ('9', ),
    KEYIDS['KEY_EXIT']: ('EXIT', ),
    KEYIDS['KEY_STOP']: ('TV', 'SHIFT'),
    KEYIDS['KEY_RECORD']: ('RADIO', 'SHIFT')
    },
 {KEYIDS['BTN_0']: ('UP', 'fp'),
    KEYIDS['BTN_1']: ('DOWN', 'fp'),
    KEYIDS['KEY_OK']: ('OK', ''),
    KEYIDS['KEY_UP']: ('UP', ),
    KEYIDS['KEY_DOWN']: ('DOWN', ),
    KEYIDS['KEY_POWER']: ('POWER', ),
    KEYIDS['KEY_RED']: ('RED', ),
    KEYIDS['KEY_BLUE']: ('BLUE', ),
    KEYIDS['KEY_GREEN']: ('GREEN', ),
    KEYIDS['KEY_YELLOW']: ('YELLOW', ),
    KEYIDS['KEY_MENU']: ('MENU', ),
    KEYIDS['KEY_LEFT']: ('LEFT', ),
    KEYIDS['KEY_RIGHT']: ('RIGHT', ),
    KEYIDS['KEY_VIDEO']: ('PVR', ),
    KEYIDS['KEY_INFO']: ('INFO', ),
    KEYIDS['KEY_AUDIO']: ('AUDIO', ),
    KEYIDS['KEY_TV']: ('TV', ),
    KEYIDS['KEY_RADIO']: ('RADIO', ),
    KEYIDS['KEY_TEXT']: ('TEXT', ),
    KEYIDS['KEY_NEXT']: ('ARROWRIGHT', ),
    KEYIDS['KEY_PREVIOUS']: ('ARROWLEFT', ),
    KEYIDS['KEY_PREVIOUSSONG']: ('REWIND', ),
    KEYIDS['KEY_PLAYPAUSE']: ('PAUSE', ),
    KEYIDS['KEY_PLAY']: ('PLAY', ),
    KEYIDS['KEY_NEXTSONG']: ('FASTFORWARD', ),
    KEYIDS['KEY_CHANNELUP']: ('BOUQUET+', ),
    KEYIDS['KEY_CHANNELDOWN']: ('BOUQUET-', ),
    KEYIDS['KEY_0']: ('0', ),
    KEYIDS['KEY_1']: ('1', ),
    KEYIDS['KEY_2']: ('2', ),
    KEYIDS['KEY_3']: ('3', ),
    KEYIDS['KEY_4']: ('4', ),
    KEYIDS['KEY_5']: ('5', ),
    KEYIDS['KEY_6']: ('6', ),
    KEYIDS['KEY_7']: ('7', ),
    KEYIDS['KEY_8']: ('8', ),
    KEYIDS['KEY_9']: ('9', ),
    KEYIDS['KEY_EXIT']: ('EXIT', ),
    KEYIDS['KEY_STOP']: ('STOP', ),
    KEYIDS['KEY_RECORD']: ('RECORD', ),
    KEYIDS['KEY_FAVORITES']: ('FAVORITES', )
    },
 {KEYIDS['BTN_0']: ('UP', 'fp'),
    KEYIDS['BTN_1']: ('DOWN', 'fp'),
    KEYIDS['KEY_OK']: ('OK', ''),
    KEYIDS['KEY_UP']: ('UP', ),
    KEYIDS['KEY_DOWN']: ('DOWN', ),
    KEYIDS['KEY_POWER']: ('POWER', ),
    KEYIDS['KEY_RED']: ('RED', ),
    KEYIDS['KEY_BLUE']: ('BLUE', ),
    KEYIDS['KEY_GREEN']: ('GREEN', ),
    KEYIDS['KEY_YELLOW']: ('YELLOW', ),
    KEYIDS['KEY_MENU']: ('MENU', ),
    KEYIDS['KEY_LEFT']: ('LEFT', ),
    KEYIDS['KEY_RIGHT']: ('RIGHT', ),
    KEYIDS['KEY_VIDEO']: ('PVR', ),
    KEYIDS['KEY_INFO']: ('INFO', ),
    KEYIDS['KEY_AUDIO']: ('AUDIO', ),
    KEYIDS['KEY_SUBTITLE']: ('SUBTITLE', ),
    KEYIDS['KEY_TV']: ('TV', ),
    KEYIDS['KEY_RADIO']: ('RADIO', ),
    KEYIDS['KEY_TEXT']: ('TEXT', ),
    KEYIDS['KEY_NEXT']: ('ARROWRIGHT', ),
    KEYIDS['KEY_PREVIOUS']: ('ARROWLEFT', ),
    KEYIDS['KEY_PREVIOUSSONG']: ('SKIPBACK', ),
    KEYIDS['KEY_REWIND']: ('REWIND', ),
    KEYIDS['KEY_FASTFORWARD']: ('FASTFORWARD', ),
    KEYIDS['KEY_NEXTSONG']: ('SKIPFORWARD', ),
    KEYIDS['KEY_PLAYPAUSE']: ('PLAYPAUSE', ),
    KEYIDS['KEY_CHANNELUP']: ('BOUQUET+', ),
    KEYIDS['KEY_CHANNELDOWN']: ('BOUQUET-', ),
    KEYIDS['KEY_0']: ('0', ),
    KEYIDS['KEY_1']: ('1', ),
    KEYIDS['KEY_2']: ('2', ),
    KEYIDS['KEY_3']: ('3', ),
    KEYIDS['KEY_4']: ('4', ),
    KEYIDS['KEY_5']: ('5', ),
    KEYIDS['KEY_6']: ('6', ),
    KEYIDS['KEY_7']: ('7', ),
    KEYIDS['KEY_8']: ('8', ),
    KEYIDS['KEY_9']: ('9', ),
    KEYIDS['KEY_EXIT']: ('EXIT', ),
    KEYIDS['KEY_STOP']: ('STOP', ),
    KEYIDS['KEY_RECORD']: ('RECORD', ),
    KEYIDS['KEY_BOOKMARKS']: ('PORTAL', ),
    KEYIDS['KEY_VMODE']: ('VMODE', ),
    KEYIDS['KEY_PROGRAM']: ('TIMER', ),
    KEYIDS['KEY_SLEEP']: ('SLEEP', ),
    KEYIDS['KEY_EPG']: ('EPG', )
    },
 {KEYIDS['BTN_0']: ('UP', 'fp'),
    KEYIDS['BTN_1']: ('DOWN', 'fp'),
    KEYIDS['KEY_OK']: ('OK', ''),
    KEYIDS['KEY_UP']: ('UP', ),
    KEYIDS['KEY_DOWN']: ('DOWN', ),
    KEYIDS['KEY_POWER']: ('POWER', ),
    KEYIDS['KEY_RED']: ('RED', ),
    KEYIDS['KEY_BLUE']: ('BLUE', ),
    KEYIDS['KEY_GREEN']: ('GREEN', ),
    KEYIDS['KEY_YELLOW']: ('YELLOW', ),
    KEYIDS['KEY_MENU']: ('MENU', ),
    KEYIDS['KEY_LEFT']: ('LEFT', ),
    KEYIDS['KEY_RIGHT']: ('RIGHT', ),
    KEYIDS['KEY_VIDEO']: ('PVR', ),
    KEYIDS['KEY_INFO']: ('INFO', ),
    KEYIDS['KEY_AUDIO']: ('AUDIO', ),
    KEYIDS['KEY_TV']: ('TV', ),
    KEYIDS['KEY_RADIO']: ('RADIO', ),
    KEYIDS['KEY_TEXT']: ('TEXT', ),
    KEYIDS['KEY_NEXT']: ('ARROWRIGHT', ),
    KEYIDS['KEY_PREVIOUS']: ('ARROWLEFT', ),
    KEYIDS['KEY_REWIND']: ('REWIND', ),
    KEYIDS['KEY_PAUSE']: ('PAUSE', ),
    KEYIDS['KEY_PLAY']: ('PLAY', ),
    KEYIDS['KEY_FASTFORWARD']: ('FASTFORWARD', ),
    KEYIDS['KEY_CHANNELUP']: ('BOUQUET+', ),
    KEYIDS['KEY_CHANNELDOWN']: ('BOUQUET-', ),
    KEYIDS['KEY_0']: ('0', ),
    KEYIDS['KEY_1']: ('1', ),
    KEYIDS['KEY_2']: ('2', ),
    KEYIDS['KEY_3']: ('3', ),
    KEYIDS['KEY_4']: ('4', ),
    KEYIDS['KEY_5']: ('5', ),
    KEYIDS['KEY_6']: ('6', ),
    KEYIDS['KEY_7']: ('7', ),
    KEYIDS['KEY_8']: ('8', ),
    KEYIDS['KEY_9']: ('9', ),
    KEYIDS['KEY_EXIT']: ('EXIT', ),
    KEYIDS['KEY_STOP']: ('STOP', ),
    KEYIDS['KEY_RECORD']: ('RECORD', ),
    KEYIDS['KEY_F1']: ('F1', ),
    KEYIDS['KEY_F2']: ('F2', ),
    KEYIDS['KEY_F3']: ('F3', ),
    KEYIDS['KEY_BACK']: ('RECALL', ),
    KEYIDS['KEY_CONTEXT_MENU']: ('CONTEXT', ),
    KEYIDS['KEY_EPG']: ('EPG', ),
    KEYIDS['KEY_BOOKMARKS']: ('PLAYLIST', )
    }]

def addKeyBinding(domain, key, context, action, flags):
    keyBindings.setdefault((context, action), []).append((key, domain, flags))


def queryKeyBinding(context, action):
    if (
     context, action) in keyBindings:
        return [ (x[0], x[2]) for x in keyBindings[context, action] ]
    else:
        return []


def getKeyDescription(key):
    if rc_model.rcIsDefault():
        idx = config.misc.rcused.value
    else:
        rctype = config.plugins.remotecontroltype.rctype.value
        if rctype == 14:
            idx = 3
        elif rctype == 18:
            idx = 4
        else:
            idx = 2
    if key in keyDescriptions[idx]:
        return keyDescriptions[idx].get(key, [])


def removeKeyBindings(domain):
    for x in keyBindings:
        keyBindings[x] = filter(lambda e: e[1] != domain, keyBindings[x])