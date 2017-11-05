# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/RecordingConfig.py
# Compiled at: 2017-10-02 01:52:08
from config import ConfigSelectionNumberConfigYesNoConfigSubsectionConfigSelectionconfig
from enigma import pNavigation
from Components.SystemInfo import SystemInfo

def InitRecordingConfig():
    config.recording = ConfigSubsection()
    config.recording.asktozap = ConfigYesNo(default=True)
    config.recording.margin_before = ConfigSelectionNumber(min=0, max=120, stepwidth=1, default=3, wraparound=True)
    config.recording.margin_after = ConfigSelectionNumber(min=0, max=120, stepwidth=1, default=5, wraparound=True)
    config.recording.ascii_filenames = ConfigYesNo(default=False)
    config.recording.keep_timers = ConfigSelectionNumber(min=1, max=120, stepwidth=1, default=7, wraparound=True)
    config.recording.filename_composition = ConfigSelection(default='standard', choices=[
     (
      'standard', _('standard')),
     (
      'veryveryshort', _('Very very short filenames - Warning')),
     (
      'veryshort', _('Very short filenames')),
     (
      'event', _('Event name first')),
     (
      'short', _('Short filenames')),
     (
      'long', _('Long filenames'))])
    config.recording.offline_decode_delay = ConfigSelectionNumber(min=1, max=10000, stepwidth=10, default=1000, wraparound=True)
    config.recording.ecm_data = ConfigSelection(choices=[('normal', _('normal')), ('descrambled+ecm', _('descramble and record ecm')), ('scrambled+ecm', _("don't descramble, record ecm"))], default='normal')
    config.recording.default_timertype = ConfigSelection(choices=[('zap', _('zap')), ('record', _('record')), ('zap+record', _('zap and record'))], default='record')
    if SystemInfo['DeepstandbySupport']:
        shutdownString = _('go to deep standby')
    else:
        shutdownString = _('shut down')
    config.recording.default_afterevent = ConfigSelection(choices=[('0', _('do nothing')), ('1', _('go to standby')), ('2', shutdownString), ('3', _('auto'))], default='3')
    config.recording.include_ait = ConfigYesNo(default=False)
    config.recording.show_rec_symbol_for_rec_types = ConfigSelection(choices=[('any', _('any recordings')), ('real', _('real recordings')), ('real_streaming', _('real recordings or streaming')), ('real_pseudo', _('real or pseudo recordings'))], default='real_streaming')
    config.recording.warn_box_restart_rec_types = ConfigSelection(choices=[('any', _('any recordings')), ('real', _('real recordings')), ('real_streaming', _('real recordings or streaming')), ('real_pseudo', _('real or pseudo recordings'))], default='real_streaming')
    config.recording.ask_to_abort_pseudo_rec = ConfigSelection(choices=[('ask', _('ask user')), ('abort_no_msg', _('just abort, no message')), ('abort_msg', _('just abort, show message')), ('never_abort', _('never abort'))], default='abort_msg')
    config.recording.ask_to_abort_streaming = ConfigSelection(choices=[('ask', _('ask user')), ('abort_no_msg', _('just abort, no message')), ('abort_msg', _('just abort, show message')), ('never_abort', _('never abort'))], default='abort_msg')
    config.recording.ask_to_abort_pip = ConfigSelection(choices=[('ask', _('ask user')), ('abort_no_msg', _('just abort, no message')), ('abort_msg', _('just abort, show message')), ('never_abort', _('never abort'))], default='abort_msg')


def recType(configString):
    if configString == 'any':
        return pNavigation.isAnyRecording
    if configString == 'real':
        return pNavigation.isRealRecording
    if configString == 'real_streaming':
        return pNavigation.isRealRecording | pNavigation.isStreaming
    if configString == 'real_pseudo':
        return pNavigation.isRealRecording | pNavigation.isPseudoRecording