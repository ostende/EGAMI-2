# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Components/Timeshift.py
# Compiled at: 2017-10-02 01:52:08
from Components.ActionMap import ActionMapHelpableActionMap
from Components.ServiceEventTracker import ServiceEventTracker
from Components.config import config
from Components.SystemInfo import SystemInfo
from Components.Task import job_manager as JobManager
from Screens.ChoiceBox import ChoiceBox
from Screens.MessageBox import MessageBox
import Screens.Standby
from ServiceReference import ServiceReference
from RecordTimer import RecordTimerEntryparseEventAFTEREVENT
from timer import TimerEntry
from Tools import ASCIItranslitNotifications
from Tools.BoundFunction import boundFunction
from Tools.Directories import pathExistsfileExistsgetRecordingFilenamecopyfileresolveFilenameSCOPE_TIMESHIFTSCOPE_AUTORECORD
from Tools.TimeShift import CopyTimeshiftJobMergeTimeshiftJobCreateAPSCFilesJob
from enigma import eBackgroundFileErasereTimereServiceCenteriServiceInformationiPlayableServiceeEPGCache
from boxbranding import getBoxTypegetBrandOEM
from time import timelocaltimestrftime
from random import randint
import os

class InfoBarTimeshift:
    ts_disabled = False

    def __init__(self):
        self['TimeshiftActions'] = HelpableActionMap(self, 'InfobarTimeshiftActions', {'timeshiftStart': (
                            self.startTimeshift, _('Start timeshift')),
           'timeshiftStop': (
                           self.stopTimeshift, _('Stop timeshift')),
           'instantRecord': self.instantRecord,
           'restartTimeshift': self.restartTimeshift
           }, prio=1)
        self['TimeshiftActivateActions'] = ActionMap(['InfobarTimeshiftActivateActions'], {'timeshiftActivateEnd': self.activateTimeshiftEnd,
           'timeshiftActivateEndAndPause': self.activateTimeshiftEndAndPause
           }, prio=-1)
        self['TimeshiftSeekPointerActions'] = ActionMap(['InfobarTimeshiftSeekPointerActions'], {'SeekPointerOK': self.ptsSeekPointerOK,
           'SeekPointerLeft': self.ptsSeekPointerLeft,
           'SeekPointerRight': self.ptsSeekPointerRight
           }, prio=-1)
        self['TimeshiftFileActions'] = ActionMap(['InfobarTimeshiftActions'], {'jumpPreviousFile': self.__evSOFjump,
           'jumpNextFile': self.__evEOF
           }, prio=-1)
        self['TimeshiftActions'].setEnabled(False)
        self['TimeshiftActivateActions'].setEnabled(False)
        self['TimeshiftSeekPointerActions'].setEnabled(False)
        self['TimeshiftFileActions'].setEnabled(False)
        self.switchToLive = True
        self.ptsStop = False
        self.ts_rewind_timer = eTimer()
        self.ts_rewind_timer.callback.append(self.rewindService)
        self.save_timeshift_file = False
        self.saveTimeshiftEventPopupActive = False
        self.__event_tracker = ServiceEventTracker(screen=self, eventmap={iPlayableService.evStart: self.__serviceStarted,
           iPlayableService.evSeekableStatusChanged: self.__seekableStatusChanged,
           iPlayableService.evEnd: self.__serviceEnd,
           iPlayableService.evSOF: self.__evSOF,
           iPlayableService.evUpdatedInfo: self.__evInfoChanged,
           iPlayableService.evUpdatedEventInfo: self.__evEventInfoChanged,
           iPlayableService.evUser + 1: self.ptsTimeshiftFileChanged
           })
        self.pts_begintime = 0
        self.pts_switchtolive = False
        self.pts_firstplayable = 1
        self.pts_lastposition = 0
        self.pts_lastplaying = 1
        self.pts_currplaying = 1
        self.pts_nextplaying = 0
        self.pts_lastseekspeed = 0
        self.pts_service_changed = False
        self.pts_file_changed = False
        self.pts_record_running = self.session.nav.RecordTimer.isRecording()
        self.save_current_timeshift = False
        self.save_timeshift_postaction = None
        self.service_changed = 0
        self.event_changed = False
        self.checkEvents_value = int(config.timeshift.timeshiftCheckEvents.value)
        self.pts_starttime = time()
        self.ptsAskUser_wait = False
        self.posDiff = 0
        self.session.ptsmainloopvalue = 0
        config.timeshift.isRecording.value = False
        self.BgFileEraser = eBackgroundFileEraser.getInstance()
        self.pts_delay_timer = eTimer()
        self.pts_delay_timer.callback.append(self.autostartAutorecordTimeshift)
        self.pts_mergeRecords_timer = eTimer()
        self.pts_mergeRecords_timer.callback.append(self.ptsMergeRecords)
        self.pts_mergeCleanUp_timer = eTimer()
        self.pts_mergeCleanUp_timer.callback.append(self.ptsMergePostCleanUp)
        self.pts_QuitMainloop_timer = eTimer()
        self.pts_QuitMainloop_timer.callback.append(self.ptsTryQuitMainloop)
        self.pts_cleanUp_timer = eTimer()
        self.pts_cleanUp_timer.callback.append(self.ptsCleanTimeshiftFolder)
        self.pts_cleanEvent_timer = eTimer()
        self.pts_cleanEvent_timer.callback.append(self.ptsEventCleanTimeshiftFolder)
        self.pts_SeekBack_timer = eTimer()
        self.pts_SeekBack_timer.callback.append(self.ptsSeekBackTimer)
        self.pts_StartSeekBackTimer = eTimer()
        self.pts_StartSeekBackTimer.callback.append(self.ptsStartSeekBackTimer)
        self.pts_SeekToPos_timer = eTimer()
        self.pts_SeekToPos_timer.callback.append(self.ptsSeekToPos)
        self.pts_CheckFileChanged_counter = 1
        self.pts_CheckFileChanged_timer = eTimer()
        self.pts_CheckFileChanged_timer.callback.append(self.ptsCheckFileChanged)
        self.pts_blockZap_timer = eTimer()
        self.pts_FileJump_timer = eTimer()
        self.session.nav.RecordTimer.on_state_change.append(self.ptsTimerEntryStateChange)
        self.pts_eventcount = 0
        self.pts_curevent_begin = int(time())
        self.pts_curevent_end = 0
        self.pts_curevent_name = _('Timeshift')
        self.pts_curevent_description = ''
        self.pts_curevent_servicerefname = ''
        self.pts_curevent_station = ''
        self.pts_curevent_eventid = None
        return

    def __seekableStatusChanged(self):
        self['TimeshiftActivateActions'].setEnabled(not self.isSeekable() and self.timeshiftEnabled())
        state = self.getSeek() is not None and self.timeshiftEnabled()
        self['SeekActionsPTS'].setEnabled(state)
        self['TimeshiftFileActions'].setEnabled(state)
        if not state and self.pts_currplaying == self.pts_eventcount and self.timeshiftEnabled() and not self.event_changed:
            self.setSeekState(self.SEEK_STATE_PLAY)
            if hasattr(self, 'pvrStateDialog'):
                self.pvrStateDialog.hide()
        self.restartSubtitle()
        if self.timeshiftEnabled() and not self.isSeekable():
            self.ptsSeekPointerReset()
            if int(config.timeshift.startdelay.value):
                if self.pts_starttime <= time() - 5:
                    self.pts_blockZap_timer.start(3000, True)
            self.pts_lastplaying = self.pts_currplaying = self.pts_eventcount
            self.pts_nextplaying = 0
            self.pts_file_changed = True
            self.ptsSetNextPlaybackFile('pts_livebuffer_%s' % self.pts_eventcount)
        return

    def __serviceStarted(self):
        self.service_changed = 1
        self.pts_service_changed = True
        if self.pts_delay_timer.isActive():
            self.pts_delay_timer.stop()
        if int(config.timeshift.startdelay.value):
            self.pts_delay_timer.start(int(config.timeshift.startdelay.value) * 1000, True)
        self['TimeshiftActions'].setEnabled(True)

    def __serviceEnd(self):
        if self.save_current_timeshift:
            if self.pts_curevent_end > time():
                self.SaveTimeshift('pts_livebuffer_%s' % self.pts_eventcount, mergelater=True)
                self.ptsRecordCurrentEvent()
            else:
                self.SaveTimeshift('pts_livebuffer_%s' % self.pts_eventcount)
        self.service_changed = 0
        self.__seekableStatusChanged()
        self['TimeshiftActions'].setEnabled(False)

    def __evSOFjump(self):
        if not self.timeshiftEnabled() or self.pts_CheckFileChanged_timer.isActive() or self.pts_SeekBack_timer.isActive() or self.pts_StartSeekBackTimer.isActive() or self.pts_SeekToPos_timer.isActive():
            return
        if self.pts_FileJump_timer.isActive():
            self.__evSOF()
        else:
            self.pts_FileJump_timer.start(5000, True)
            self.setSeekState(self.SEEK_STATE_PLAY)
            self.doSeek(0)
            self.posDiff = 0

    def evSOF(self, posDiff=0):
        self.posDiff = posDiff
        self.__evSOF()

    def __evSOF(self):
        if not self.timeshiftEnabled() or self.pts_CheckFileChanged_timer.isActive() or self.pts_SeekBack_timer.isActive() or self.pts_StartSeekBackTimer.isActive() or self.pts_SeekToPos_timer.isActive():
            return
        self.pts_switchtolive = False
        self.pts_lastplaying = self.pts_currplaying
        self.pts_nextplaying = 0
        if self.pts_currplaying > self.pts_firstplayable:
            self.pts_currplaying -= 1
        else:
            self.setSeekState(self.SEEK_STATE_PLAY)
            self.doSeek(0)
            self.posDiff = 0
            if self.pts_FileJump_timer.isActive():
                self.pts_FileJump_timer.stop()
                Notifications.AddNotification(MessageBox, _('First playable timeshift file!'), MessageBox.TYPE_INFO, timeout=3)
            if not self.pts_FileJump_timer.isActive():
                self.pts_FileJump_timer.start(5000, True)
            return
        if fileExists('%spts_livebuffer_%s' % (config.usage.timeshift_path.value, self.pts_currplaying), 'r'):
            self.ptsSetNextPlaybackFile('pts_livebuffer_%s' % self.pts_currplaying)
            self.setSeekState(self.SEEK_STATE_PLAY)
            self.doSeek(7776000000)
            self.pts_CheckFileChanged_counter = 1
            self.pts_CheckFileChanged_timer.start(1000, False)
            self.pts_file_changed = False
        else:
            print '[TIMESHIFT] - "pts_livebuffer_%s" file was not found -> put pointer to the first (current) "pts_livebuffer_%s" file' % (self.pts_currplaying, self.pts_currplaying + 1)
            self.pts_currplaying += 1
            self.pts_firstplayable += 1
            self.setSeekState(self.SEEK_STATE_PLAY)
            self.doSeek(0)
            self.posDiff = 0

    def evEOF(self, posDiff=0):
        self.posDiff = posDiff
        self.__evEOF()

    def __evEOF(self):
        if not self.timeshiftEnabled() or self.pts_CheckFileChanged_timer.isActive() or self.pts_SeekBack_timer.isActive() or self.pts_StartSeekBackTimer.isActive() or self.pts_SeekToPos_timer.isActive():
            return
        self.pts_switchtolive = False
        self.pts_lastposition = self.ptsGetPosition()
        self.pts_lastplaying = self.pts_currplaying
        self.pts_nextplaying = 0
        self.pts_currplaying += 1
        if fileExists('%spts_livebuffer_%s' % (config.usage.timeshift_path.value, self.pts_currplaying), 'r'):
            self.ptsSetNextPlaybackFile('pts_livebuffer_%s' % self.pts_currplaying)
            self.setSeekState(self.SEEK_STATE_PLAY)
            self.doSeek(7776000000)
            self.pts_CheckFileChanged_counter = 1
            self.pts_CheckFileChanged_timer.start(1000, False)
            self.pts_file_changed = False
        else:
            if not int(config.timeshift.startdelay.value) and config.timeshift.showlivetvmsg.value:
                Notifications.AddNotification(MessageBox, _('Switching to live TV - timeshift is still active!'), MessageBox.TYPE_INFO, timeout=3)
            self.posDiff = 0
            self.pts_lastposition = 0
            self.pts_currplaying -= 1
            self.pts_switchtolive = True
            self.ptsSetNextPlaybackFile('')
            self.setSeekState(self.SEEK_STATE_PLAY)
            self.doSeek(7776000000)
            self.pts_CheckFileChanged_counter = 1
            self.pts_CheckFileChanged_timer.start(1000, False)
            self.pts_file_changed = False

    def __evInfoChanged(self):
        if self.service_changed:
            self.service_changed = 0
            if self.save_current_timeshift:
                self.SaveTimeshift('pts_livebuffer_%s' % self.pts_eventcount)
            if config.timeshift.deleteAfterZap.value:
                self.ptsEventCleanTimerSTOP()
            self.pts_firstplayable = self.pts_eventcount + 1
            if self.pts_eventcount == 0 and not int(config.timeshift.startdelay.value):
                self.pts_cleanUp_timer.start(1000, True)

    def __evEventInfoChanged(self):
        service = self.session.nav.getCurrentService()
        old_begin_time = self.pts_begintime
        info = service and service.info()
        ptr = info and info.getEvent(0)
        self.pts_begintime = ptr and ptr.getBeginTime() or 0
        if info.getInfo(iServiceInformation.sVideoPID) != -1:
            if self.save_current_timeshift and self.timeshiftEnabled():
                if config.recording.margin_after.value > 0 and len(self.recording) == 0:
                    self.SaveTimeshift(mergelater=True)
                    recording = RecordTimerEntry(ServiceReference(self.session.nav.getCurrentlyPlayingServiceOrGroup()), time(), time() + config.recording.margin_after.value * 60, self.pts_curevent_name, self.pts_curevent_description, self.pts_curevent_eventid, afterEvent=AFTEREVENT.AUTO, justplay=False, always_zap=False, dirname=config.usage.autorecord_path.value)
                    recording.dontSave = True
                    self.session.nav.RecordTimer.record(recording)
                    self.recording.append(recording)
                else:
                    self.SaveTimeshift()
                if not config.timeshift.filesplitting.value:
                    self.stopTimeshiftcheckTimeshiftRunningCallback(True)
            if not self.pts_delay_timer.isActive():
                if old_begin_time != self.pts_begintime or old_begin_time == 0:
                    if int(config.timeshift.startdelay.value) or self.timeshiftEnabled():
                        self.event_changed = True
                    self.pts_delay_timer.start(1000, True)

    def getTimeshift(self):
        if self.ts_disabled or self.pts_delay_timer.isActive():
            return None
        else:
            service = self.session.nav.getCurrentService()
            return service and service.timeshift()

    def timeshiftEnabled(self):
        ts = self.getTimeshift()
        return ts and ts.isTimeshiftEnabled()

    def startTimeshift(self):
        ts = self.getTimeshift()
        if ts is None:
            return 0
        else:
            if ts.isTimeshiftEnabled():
                print '[TIMESHIFT] - hu, timeshift already enabled?'
                self.activateTimeshiftEndAndPause()
            else:
                self.activateAutorecordTimeshift()
                self.activateTimeshiftEndAndPause()
            return

    def stopTimeshift(self):
        ts = self.getTimeshift()
        if ts and ts.isTimeshiftEnabled():
            if int(config.timeshift.startdelay.value) and self.isSeekable():
                self.switchToLive = True
                self.ptsStop = True
                self.checkTimeshiftRunning(self.stopTimeshiftcheckTimeshiftRunningCallback)
            elif not int(config.timeshift.startdelay.value):
                self.checkTimeshiftRunning(self.stopTimeshiftcheckTimeshiftRunningCallback)
            else:
                return 0
        else:
            return 0

    def stopTimeshiftcheckTimeshiftRunningCallback(self, answer):
        if answer and int(config.timeshift.startdelay.value) and self.switchToLive and self.isSeekable():
            self.posDiff = 0
            self.pts_lastposition = 0
            if self.pts_currplaying != self.pts_eventcount:
                self.pts_lastposition = self.ptsGetPosition()
            self.pts_lastplaying = self.pts_currplaying
            self.ptsStop = False
            self.pts_nextplaying = 0
            self.pts_switchtolive = True
            self.setSeekState(self.SEEK_STATE_PLAY)
            self.ptsSetNextPlaybackFile('')
            self.doSeek(7776000000)
            self.pts_CheckFileChanged_counter = 1
            self.pts_CheckFileChanged_timer.start(1000, False)
            self.pts_file_changed = False
            return 0
        ts = self.getTimeshift()
        if answer and ts:
            if int(config.timeshift.startdelay.value):
                ts.stopTimeshift(self.switchToLive)
            else:
                ts.stopTimeshift(not self.event_changed)
            self.__seekableStatusChanged()

    def activateTimeshiftEnd(self, back=True):
        ts = self.getTimeshift()
        if ts is None:
            return
        else:
            if ts.isTimeshiftActive():
                self.pauseService()
            else:
                ts.activateTimeshift()
                self.setSeekState(self.SEEK_STATE_PAUSE)
                seekable = self.getSeek()
                if seekable is not None:
                    seekable.seekTo(-90000)
            if back:
                if getBrandOEM() == 'xtrend':
                    self.ts_rewind_timer.start(1000, 1)
                else:
                    self.ts_rewind_timer.start(500, 1)
            return

    def rewindService(self):
        if getBrandOEM() in ('gigablue', 'xp'):
            self.setSeekState(self.SEEK_STATE_PLAY)
        self.setSeekState(self.makeStateBackward(int(config.seek.enter_backward.value)))

    def callServiceStarted(self):
        from Screens.InfoBarGenerics import isStandardInfoBar
        if isStandardInfoBar(self):
            ServiceEventTracker.setActiveInfoBar(self, None, None)
            self.__serviceStarted()
        return

    def activateTimeshiftEndAndPause(self):
        self.activateTimeshiftEnd(False)

    def checkTimeshiftRunning(self, returnFunction):
        url = None
        ext = ['.3g2', '.3gp', '.asf', '.asx', '.avi', '.flv', '.m2ts', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg', '.rm', '.swf', '.vob', '.wmv', '.m3u8']
        if self.session.nav.getCurrentlyPlayingServiceReference():
            url = ServiceReference(self.session.nav.getCurrentlyPlayingServiceReference()).getPath()
        if self.ptsStop:
            returnFunction(True)
        elif (self.isSeekable() or self.timeshiftEnabled() and not int(config.timeshift.startdelay.value) or self.save_current_timeshift) and config.usage.check_timeshift.value and not str(url).endswith(tuple(ext)):
            if config.timeshift.favoriteSaveAction.value == 'askuser':
                if self.save_current_timeshift:
                    message = _('You have chosen to save the current timeshift event, but the event has not yet finished\nWhat do you want to do ?')
                    choice = [(_('Save timeshift as movie and continue recording'), 'savetimeshiftandrecord'),
                     (
                      _('Save timeshift as movie and stop recording'), 'savetimeshift'),
                     (
                      _('Cancel save timeshift as movie'), 'noSave'),
                     (
                      _('Nothing, just leave this menu'), 'no')]
                    self.session.openWithCallback(boundFunction(self.checkTimeshiftRunningCallback, returnFunction), MessageBox, message, simple=True, list=choice, timeout=30)
                else:
                    message = _('You seem to be in timeshift, Do you want to leave timeshift ?')
                    choice = [(_("Yes, but don't save timeshift as movie"), 'noSave'),
                     (
                      _('Yes, but save timeshift as movie and continue recording'), 'savetimeshiftandrecord'),
                     (
                      _('Yes, but save timeshift as movie and stop recording'), 'savetimeshift'),
                     (
                      _('No'), 'no')]
                    self.session.openWithCallback(boundFunction(self.checkTimeshiftRunningCallback, returnFunction), MessageBox, message, simple=True, list=choice, timeout=30)
            elif self.save_current_timeshift:
                message = _('You have chosen to save the current timeshift')
                choice = [(_('Now save timeshift as movie and continues recording'), 'savetimeshiftandrecord')]
                self.session.openWithCallback(boundFunction(self.checkTimeshiftRunningCallback, returnFunction), MessageBox, message, simple=True, list=choice, timeout=1)
            else:
                message = _('You seem to be in timeshift, Do you want to leave timeshift ?')
                choice = [(_('Yes'), config.timeshift.favoriteSaveAction.value), (_('No'), 'no')]
                self.session.openWithCallback(boundFunction(self.checkTimeshiftRunningCallback, returnFunction), MessageBox, message, simple=True, list=choice, timeout=30)
        elif self.save_current_timeshift:
            message = _('You have chosen to save the current timeshift')
            choice = [(_('Now save timeshift as movie and continues recording'), 'savetimeshiftandrecord')]
            self.session.openWithCallback(boundFunction(self.checkTimeshiftRunningCallback, returnFunction), MessageBox, message, simple=True, list=choice, timeout=1)
        else:
            returnFunction(True)
        return

    def checkTimeshiftRunningCallback(self, returnFunction, answer):
        if answer:
            if answer == 'savetimeshift' or answer == 'savetimeshiftandrecord':
                self.save_current_timeshift = True
            elif answer == 'noSave':
                self.save_current_timeshift = False
            elif answer == 'no':
                pass
            InfoBarTimeshift.saveTimeshiftActions(self, answer, returnFunction)

    def eraseTimeshiftFile(self):
        for filename in os.listdir(config.usage.timeshift_path.value):
            if filename.startswith('timeshift.') and not filename.endswith('.del') and not filename.endswith('.copy'):
                self.BgFileEraser.erase('%s%s' % (config.usage.timeshift_path.value, filename))

    def autostartAutorecordTimeshift(self):
        ts = self.getTimeshift()
        if ts is None:
            print '[TIMESHIFT] - tune lock failed, so could not start.'
            return 0
        else:
            if self.pts_delay_timer.isActive():
                self.pts_delay_timer.stop()
            if int(config.timeshift.startdelay.value) and not self.timeshiftEnabled() or self.event_changed:
                self.activateAutorecordTimeshift()
            return

    def activateAutorecordTimeshift(self):
        self.createTimeshiftFolder()
        if self.pts_eventcount == 0:
            self.ptsCleanTimeshiftFolder(justZapped=True)
        else:
            self.ptsCleanTimeshiftFolder(justZapped=False)
        if self.ptsCheckTimeshiftPath() is False or self.session.screen['Standby'].boolean is True or self.ptsLiveTVStatus() is False or config.timeshift.stopwhilerecording.value and self.pts_record_running:
            return
        else:
            if config.timeshift.filesplitting.value:
                if self.isSeekable():
                    self.pts_nextplaying = self.pts_currplaying + 1
                    self.ptsSetNextPlaybackFile('pts_livebuffer_%s' % self.pts_nextplaying)
                    self.switchToLive = False
                else:
                    self.switchToLive = True
                self.stopTimeshiftcheckTimeshiftRunningCallback(True)
            elif self.pts_currplaying < self.pts_eventcount:
                self.pts_nextplaying = self.pts_currplaying + 1
                self.ptsSetNextPlaybackFile('pts_livebuffer_%s' % self.pts_nextplaying)
            else:
                self.pts_nextplaying = 0
                self.ptsSetNextPlaybackFile('')
            self.event_changed = False
            ts = self.getTimeshift()
            if ts and (not ts.startTimeshift() or self.pts_eventcount == 0):
                self.pts_eventcount += 1
                if (getBoxType() == 'vuuno' or getBoxType() == 'vuduo') and os.path.exists('/proc/stb/lcd/symbol_timeshift'):
                    if self.session.nav.RecordTimer.isRecording():
                        f = open('/proc/stb/lcd/symbol_timeshift', 'w')
                        f.write('0')
                        f.close()
                self.pts_starttime = time()
                self.save_timeshift_postaction = None
                self.ptsGetEventInfo()
                self.ptsCreateHardlink()
                self.__seekableStatusChanged()
                self.ptsEventCleanTimerSTART()
            elif ts and ts.startTimeshift():
                self.ptsGetEventInfo()
                try:
                    metafile = open('%spts_livebuffer_%s.meta' % (config.usage.timeshift_path.value, self.pts_eventcount), 'w')
                    metafile.write('%s\n%s\n%s\n%i\n' % (self.pts_curevent_servicerefname, self.pts_curevent_name.replace('\n', ''), self.pts_curevent_description.replace('\n', ''), int(self.pts_starttime)))
                    metafile.close()
                    self.ptsCreateEITFile('%spts_livebuffer_%s' % (config.usage.timeshift_path.value, self.pts_eventcount))
                except:
                    print '[TIMESHIFT] - failure rewrite meta and eit files.'

                self.ptsEventCleanTimerSTART()
            else:
                self.ptsEventCleanTimerSTOP()
                try:
                    self.session.open(MessageBox, _('Timeshift not possible!'), MessageBox.TYPE_ERROR, timeout=2)
                except:
                    print '[TIMESHIFT] - Failed to open MessageBox, Timeshift not possible, probably another MessageBox was active.'

            if self.pts_eventcount < self.pts_firstplayable:
                self.pts_firstplayable = self.pts_eventcount
            return

    def createTimeshiftFolder(self):
        timeshiftdir = resolveFilename(SCOPE_TIMESHIFT)
        if not pathExists(timeshiftdir):
            try:
                os.makedirs(timeshiftdir)
            except:
                print '[TIMESHIFT] - Failed to create %s !!' % timeshiftdir

    def restartTimeshift(self):
        self.activateAutorecordTimeshift()
        Notifications.AddNotification(MessageBox, _('[TimeShift] Restarting Timeshift!'), MessageBox.TYPE_INFO, timeout=5)

    def saveTimeshiftEventPopup(self):
        self.saveTimeshiftEventPopupActive = True
        filecount = 0
        entrylist = [(_('Current Event:') + ' %s' % self.pts_curevent_name, 'savetimeshift')]
        filelist = os.listdir(config.usage.timeshift_path.value)
        if filelist is not None:
            try:
                filelist = sorted(filelist, key=lambda x: int(x.split('pts_livebuffer_')[1]) if x.startswith('pts_livebuffer') and not os.path.splitext(x)[1] else x)
            except:
                print '[TIMESHIFT] - file sorting error, use standard sorting method'
                filelist.sort()

            for filename in filelist:
                if filename.startswith('pts_livebuffer') and not os.path.splitext(filename)[1]:
                    statinfo = os.stat('%s%s' % (config.usage.timeshift_path.value, filename))
                    if statinfo.st_mtime < time() - 5.0:
                        readmetafile = open('%s%s.meta' % (config.usage.timeshift_path.value, filename), 'r')
                        servicerefname = readmetafile.readline()[0:-1]
                        eventname = readmetafile.readline()[0:-1]
                        description = readmetafile.readline()[0:-1]
                        begintime = readmetafile.readline()[0:-1]
                        readmetafile.close()
                        filecount += 1
                        if config.timeshift.deleteAfterZap.value and servicerefname == self.pts_curevent_servicerefname:
                            entrylist.append((_('Record') + ' #%s (%s): %s' % (filecount, strftime('%H:%M', localtime(int(begintime))), eventname), '%s' % filename))
                        else:
                            servicename = ServiceReference(servicerefname).getServiceName()
                            entrylist.append(('[%s] %s : %s' % (strftime('%H:%M', localtime(int(begintime))), servicename, eventname), '%s' % filename))

            self.session.openWithCallback(self.recordQuestionCallback, ChoiceBox, title=_('Which event do you want to save permanently?'), list=entrylist)
        return

    def saveTimeshiftActions(self, action=None, returnFunction=None):
        timeshiftfile = None
        if self.pts_currplaying != self.pts_eventcount:
            timeshiftfile = 'pts_livebuffer_%s' % self.pts_currplaying
        if action == 'savetimeshift':
            self.SaveTimeshift(timeshiftfile)
        elif action == 'savetimeshiftandrecord':
            if self.pts_curevent_end > time() and timeshiftfile is None:
                self.SaveTimeshift(mergelater=True)
                self.ptsRecordCurrentEvent()
            else:
                self.SaveTimeshift(timeshiftfile)
        elif action == 'noSave':
            config.timeshift.isRecording.value = False
            self.save_current_timeshift = False
        elif action == 'no':
            pass
        if returnFunction is not None and action != 'no':
            self.eraseTimeshiftFile()
        returnFunction(action and action != 'no')
        return

    def SaveTimeshift(self, timeshiftfile=None, mergelater=False):
        self.save_current_timeshift = False
        savefilename = None
        if timeshiftfile is not None:
            savefilename = timeshiftfile
        if savefilename is None:
            for filename in os.listdir(config.usage.timeshift_path.value):
                if filename.startswith('timeshift.') and not filename.endswith(('.del',
                                                                                '.copy',
                                                                                '.sc')):
                    statinfo = os.stat('%s%s' % (config.usage.timeshift_path.value, filename))
                    if statinfo.st_mtime > time() - 5.0:
                        savefilename = filename

        if savefilename is None:
            Notifications.AddNotification(MessageBox, _('No Timeshift found to save as recording!'), MessageBox.TYPE_ERROR, timeout=30)
        else:
            timeshift_saved = True
            timeshift_saveerror1 = ''
            timeshift_saveerror2 = ''
            metamergestring = ''
            config.timeshift.isRecording.value = True
            if mergelater:
                self.pts_mergeRecords_timer.start(120000, True)
                metamergestring = 'pts_merge\n'
            try:
                if timeshiftfile is None:
                    if self.pts_starttime >= time() - 60:
                        self.pts_starttime -= 60
                    ptsfilename = '%s - %s - %s' % (strftime('%Y%m%d %H%M', localtime(self.pts_starttime)), self.pts_curevent_station, self.pts_curevent_name.replace('\n', ''))
                    try:
                        if config.usage.setup_level.index >= 2:
                            if config.recording.filename_composition.value == 'long' and self.pts_curevent_name.replace('\n', '') != self.pts_curevent_description.replace('\n', ''):
                                ptsfilename = '%s - %s - %s - %s' % (strftime('%Y%m%d %H%M', localtime(self.pts_starttime)), self.pts_curevent_station, self.pts_curevent_name.replace('\n', ''), self.pts_curevent_description.replace('\n', ''))
                            elif config.recording.filename_composition.value == 'short':
                                ptsfilename = '%s - %s' % (strftime('%Y%m%d', localtime(self.pts_starttime)), self.pts_curevent_name.replace('\n', ''))
                            elif config.recording.filename_composition.value == 'veryshort':
                                ptsfilename = '%s - %s' % (self.pts_curevent_name.replace('\n', ''), strftime('%Y%m%d %H%M', localtime(self.pts_starttime)))
                            elif config.recording.filename_composition.value == 'veryveryshort':
                                ptsfilename = '%s - %s' % (self.pts_curevent_name.replace('\n', ''), strftime('%Y%m%d %H%M', localtime(self.pts_starttime)))
                    except Exception as errormsg:
                        print '[TIMESHIFT] - Using default filename'

                    if config.recording.ascii_filenames.value:
                        ptsfilename = ASCIItranslit.legacyEncode(ptsfilename)
                    fullname = getRecordingFilename(ptsfilename, config.usage.autorecord_path.value)
                    os.link('%s%s' % (config.usage.timeshift_path.value, savefilename), '%s.ts' % fullname)
                    metafile = open('%s.ts.meta' % fullname, 'w')
                    metafile.write('%s\n%s\n%s\n%i\n%s' % (self.pts_curevent_servicerefname, self.pts_curevent_name.replace('\n', ''), self.pts_curevent_description.replace('\n', ''), int(self.pts_starttime), metamergestring))
                    metafile.close()
                    self.ptsCreateEITFile(fullname)
                elif timeshiftfile.startswith('pts_livebuffer'):
                    readmetafile = open('%s%s.meta' % (config.usage.timeshift_path.value, timeshiftfile), 'r')
                    servicerefname = readmetafile.readline()[0:-1]
                    eventname = readmetafile.readline()[0:-1]
                    description = readmetafile.readline()[0:-1]
                    begintime = readmetafile.readline()[0:-1]
                    readmetafile.close()
                    if config.timeshift.deleteAfterZap.value and servicerefname == self.pts_curevent_servicerefname:
                        servicename = self.pts_curevent_station
                    else:
                        servicename = ServiceReference(servicerefname).getServiceName()
                    ptsfilename = '%s - %s - %s' % (strftime('%Y%m%d %H%M', localtime(int(begintime))), servicename, eventname)
                    try:
                        if config.usage.setup_level.index >= 2:
                            if config.recording.filename_composition.value == 'long' and eventname != description:
                                ptsfilename = '%s - %s - %s - %s' % (strftime('%Y%m%d %H%M', localtime(int(begintime))), servicename, eventname, description)
                            elif config.recording.filename_composition.value == 'short':
                                ptsfilename = '%s - %s' % (strftime('%Y%m%d', localtime(int(begintime))), eventname)
                            elif config.recording.filename_composition.value == 'veryshort':
                                ptsfilename = '%s - %s' % (eventname, strftime('%Y%m%d %H%M', localtime(int(begintime))))
                            elif config.recording.filename_composition.value == 'veryveryshort':
                                ptsfilename = '%s - %s' % (eventname, strftime('%Y%m%d %H%M', localtime(int(begintime))))
                    except Exception as errormsg:
                        print '[TIMESHIFT] - Using default filename'

                    if config.recording.ascii_filenames.value:
                        ptsfilename = ASCIItranslit.legacyEncode(ptsfilename)
                    fullname = getRecordingFilename(ptsfilename, config.usage.autorecord_path.value)
                    os.link('%s%s' % (config.usage.timeshift_path.value, timeshiftfile), '%s.ts' % fullname)
                    os.link('%s%s.meta' % (config.usage.timeshift_path.value, timeshiftfile), '%s.ts.meta' % fullname)
                    if os.path.exists('%s%s.eit' % (config.usage.timeshift_path.value, timeshiftfile)):
                        os.link('%s%s.eit' % (config.usage.timeshift_path.value, timeshiftfile), '%s.eit' % fullname)
                    if mergelater:
                        metafile = open('%s.ts.meta' % fullname, 'a')
                        metafile.write('%s\n' % metamergestring)
                        metafile.close()
                if not mergelater:
                    self.ptsCreateAPSCFiles(fullname + '.ts')
            except Exception as errormsg:
                timeshift_saved = False
                timeshift_saveerror1 = errormsg

            if not timeshift_saved:
                try:
                    stat = os.statvfs(config.usage.autorecord_path.value)
                    freespace = stat.f_bfree / 1000 * stat.f_bsize / 1000
                    randomint = randint(1, 999)
                    if timeshiftfile is None:
                        filesize = int(os.path.getsize('%s%s' % (config.usage.timeshift_path.value, savefilename)) / 1048576)
                        if filesize <= freespace:
                            os.link('%s%s' % (config.usage.timeshift_path.value, savefilename), '%s%s.%s.copy' % (config.usage.timeshift_path.value, savefilename, randomint))
                            copy_file = savefilename
                            metafile = open('%s.ts.meta' % fullname, 'w')
                            metafile.write('%s\n%s\n%s\n%i\n%s' % (self.pts_curevent_servicerefname, self.pts_curevent_name.replace('\n', ''), self.pts_curevent_description.replace('\n', ''), int(self.pts_starttime), metamergestring))
                            metafile.close()
                            self.ptsCreateEITFile(fullname)
                    elif timeshiftfile.startswith('pts_livebuffer'):
                        filesize = int(os.path.getsize('%s%s' % (config.usage.timeshift_path.value, timeshiftfile)) / 1048576)
                        if filesize <= freespace:
                            os.link('%s%s' % (config.usage.timeshift_path.value, timeshiftfile), '%s%s.%s.copy' % (config.usage.timeshift_path.value, timeshiftfile, randomint))
                            copyfile('%s%s.meta' % (config.usage.timeshift_path.value, timeshiftfile), '%s.ts.meta' % fullname)
                            if os.path.exists('%s%s.eit' % (config.usage.timeshift_path.value, timeshiftfile)):
                                copyfile('%s%s.eit' % (config.usage.timeshift_path.value, timeshiftfile), '%s.eit' % fullname)
                            copy_file = timeshiftfile
                        if mergelater:
                            metafile = open('%s.ts.meta' % fullname, 'a')
                            metafile.write('%s\n' % metamergestring)
                            metafile.close()
                    if filesize <= freespace:
                        timeshift_saved = True
                        copy_file = copy_file + '.' + str(randomint)
                        if os.path.exists('%s.ts.meta' % fullname):
                            readmetafile = open('%s.ts.meta' % fullname, 'r')
                            servicerefname = readmetafile.readline()[0:-1]
                            eventname = readmetafile.readline()[0:-1]
                            readmetafile.close()
                        else:
                            eventname = ''
                        JobManager.AddJob(CopyTimeshiftJob(self, 'mv "%s%s.copy" "%s.ts"' % (config.usage.timeshift_path.value, copy_file, fullname), copy_file, fullname, eventname))
                        if not Screens.Standby.inTryQuitMainloop and not Screens.Standby.inStandby and not mergelater and self.save_timeshift_postaction != 'standby':
                            Notifications.AddNotification(MessageBox, _('Saving timeshift as movie now. This might take a while!'), MessageBox.TYPE_INFO, timeout=30)
                    else:
                        timeshift_saved = False
                        timeshift_saveerror1 = ''
                        timeshift_saveerror2 = _('Not enough free Diskspace!\n\nFilesize: %sMB\nFree Space: %sMB\nPath: %s' % (filesize, freespace, config.usage.autorecord_path.value))
                except Exception as errormsg:
                    timeshift_saved = False
                    timeshift_saveerror2 = errormsg

            if not timeshift_saved:
                config.timeshift.isRecording.value = False
                self.save_timeshift_postaction = None
                errormessage = str(timeshift_saveerror1) + '\n' + str(timeshift_saveerror2)
                Notifications.AddNotification(MessageBox, _('Timeshift save failed!') + '\n\n%s' % errormessage, MessageBox.TYPE_ERROR, timeout=30)
        return

    def ptsAskUser(self, what):
        if self.ptsAskUser_wait:
            return
        message_time = _('The buffer time for timeshift exceeds the specified limit in the settings.\nWhat do you want to do ?')
        message_space = _('The available disk space for timeshift is less than specified in the settings.\nWhat do you want to do ?')
        message_livetv = _("Can't going to live TV!\nSwitch to live TV and restart Timeshift ?")
        message_nextfile = _("Can't play the next Timeshift file!\nSwitch to live TV and restart Timeshift ?")
        choice_restart = [(_('Delete the current timeshift buffer and restart timeshift'), 'restarttimeshift'),
         (
          _('Nothing, just leave this menu'), 'no')]
        choice_save = [(_('Stop timeshift and save timeshift buffer as movie and start recording of current event'), 'savetimeshiftandrecord'),
         (
          _('Stop timeshift and save timeshift buffer as movie'), 'savetimeshift'),
         (
          _('Stop timeshift'), 'noSave'),
         (
          _('Nothing, just leave this menu'), 'no')]
        choice_livetv = [(_('No'), 'nolivetv'),
         (
          _('Yes'), 'golivetv')]
        if what == 'time':
            message = message_time
            choice = choice_restart
        elif what == 'space':
            message = message_space
            choice = choice_restart
        elif what == 'time_and_save':
            message = message_time
            choice = choice_save
        elif what == 'space_and_save':
            message = message_space
            choice = choice_save
        elif what == 'livetv':
            message = message_livetv
            choice = choice_livetv
        elif what == 'nextfile':
            message = message_nextfile
            choice = choice_livetv
        else:
            return
        self.ptsAskUser_wait = True
        self.session.openWithCallback(self.ptsAskUserCallback, MessageBox, message, simple=True, list=choice, timeout=30)

    def ptsAskUserCallback(self, answer):
        self.ptsAskUser_wait = False
        if answer:
            if answer == 'restarttimeshift':
                self.ptsEventCleanTimerSTOP()
                self.save_current_timeshift = False
                self.stopTimeshiftAskUserCallback(True)
                self.restartTimeshift()
            elif answer == 'noSave':
                self.ptsEventCleanTimerSTOP()
                self.save_current_timeshift = False
                self.stopTimeshiftAskUserCallback(True)
            elif answer == 'savetimeshift' or answer == 'savetimeshiftandrecord':
                self.ptsEventCleanTimerSTOP()
                self.save_current_timeshift = True
                InfoBarTimeshift.saveTimeshiftActions(self, answer, self.stopTimeshiftAskUserCallback)
            elif answer == 'golivetv':
                self.ptsEventCleanTimerSTOP(True)
                self.stopTimeshiftAskUserCallback(True)
                self.restartTimeshift()
            elif answer == 'nolivetv':
                if self.pts_lastposition:
                    self.setSeekState(self.SEEK_STATE_PLAY)
                    self.doSeek(self.pts_lastposition)

    def stopTimeshiftAskUserCallback(self, answer):
        ts = self.getTimeshift()
        if answer and ts:
            ts.stopTimeshift(True)
            self.__seekableStatusChanged()

    def ptsEventCleanTimerSTOP(self, justStop=False):
        if justStop is False:
            self.pts_eventcount = 0
        if self.pts_cleanEvent_timer.isActive():
            self.pts_cleanEvent_timer.stop()
            print "[TIMESHIFT] - 'cleanEvent_timer' is stopped"

    def ptsEventCleanTimerSTART(self):
        if not self.pts_cleanEvent_timer.isActive() and int(config.timeshift.timeshiftCheckEvents.value):
            self.pts_cleanEvent_timer.start(60000 * int(config.timeshift.timeshiftCheckEvents.value), False)
            print "[TIMESHIFT] - 'cleanEvent_timer' is starting"

    def ptsEventCleanTimeshiftFolder(self):
        print "[TIMESHIFT] - 'cleanEvent_timer' is running"
        self.ptsCleanTimeshiftFolder(justZapped=False)

    def ptsCleanTimeshiftFolder(self, justZapped=True):
        if self.ptsCheckTimeshiftPath() is False or self.session.screen['Standby'].boolean is True:
            self.ptsEventCleanTimerSTOP()
            return
        freespace = int(config.timeshift.timeshiftCheckFreeSpace.value)
        timeshiftEnabled = self.timeshiftEnabled()
        isSeekable = self.isSeekable()
        filecounter = 0
        filesize = 0
        lockedFiles = []
        removeFiles = []
        if timeshiftEnabled:
            if isSeekable:
                for i in range(self.pts_currplaying, self.pts_eventcount + 1):
                    lockedFiles.append('pts_livebuffer_%s' % i)

            elif not self.event_changed:
                lockedFiles.append('pts_livebuffer_%s' % self.pts_currplaying)
        if freespace:
            try:
                stat = os.statvfs(config.usage.timeshift_path.value)
                freespace = stat.f_bavail * stat.f_bsize / 1024 / 1024
            except:
                print "[TIMESHIFT] - error reading disk space - function 'checking for free space' can't used"

        if freespace < int(config.timeshift.timeshiftCheckFreeSpace.value):
            for i in range(1, self.pts_eventcount + 1):
                removeFiles.append('pts_livebuffer_%s' % i)

            print '[TIMESHIFT] - less than %s MByte disk space available - try to the deleting all unused timeshift files' % config.timeshift.timeshiftCheckFreeSpace.value
        elif self.pts_eventcount - config.timeshift.timeshiftMaxEvents.value >= 0:
            if self.event_changed or len(lockedFiles) == 0:
                for i in range(1, self.pts_eventcount - config.timeshift.timeshiftMaxEvents.value + 2):
                    removeFiles.append('pts_livebuffer_%s' % i)

            else:
                for i in range(1, self.pts_eventcount - config.timeshift.timeshiftMaxEvents.value + 1):
                    removeFiles.append('pts_livebuffer_%s' % i)

        for filename in os.listdir(config.usage.timeshift_path.value):
            if os.path.exists('%s%s' % (config.usage.timeshift_path.value, filename)) and (filename.startswith('timeshift.') or filename.startswith('pts_livebuffer_')):
                statinfo = os.stat('%s%s' % (config.usage.timeshift_path.value, filename))
                if justZapped is True and filename.endswith('.del') is False and filename.endswith('.copy') is False:
                    filesize += os.path.getsize('%s%s' % (config.usage.timeshift_path.value, filename))
                    self.BgFileEraser.erase('%s%s' % (config.usage.timeshift_path.value, filename))
                elif filename.endswith('.eit') is False and filename.endswith('.meta') is False and filename.endswith('.sc') is False and filename.endswith('.del') is False and filename.endswith('.copy') is False:
                    if not filename.startswith('timeshift.'):
                        filecounter += 1
                    if (statinfo.st_mtime < time() - 3600 * config.timeshift.timeshiftMaxHours.value or any((filename in s for s in removeFiles))) and self.saveTimeshiftEventPopupActive is False and not any((filename in s for s in lockedFiles)):
                        filesize += os.path.getsize('%s%s' % (config.usage.timeshift_path.value, filename))
                        self.BgFileEraser.erase('%s%s' % (config.usage.timeshift_path.value, filename))
                        if os.path.exists('%s%s.eit' % (config.usage.timeshift_path.value, filename)):
                            filesize += os.path.getsize('%s%s.eit' % (config.usage.timeshift_path.value, filename))
                            self.BgFileEraser.erase('%s%s.eit' % (config.usage.timeshift_path.value, filename))
                        if os.path.exists('%s%s.meta' % (config.usage.timeshift_path.value, filename)):
                            filesize += os.path.getsize('%s%s.meta' % (config.usage.timeshift_path.value, filename))
                            self.BgFileEraser.erase('%s%s.meta' % (config.usage.timeshift_path.value, filename))
                        if os.path.exists('%s%s.sc' % (config.usage.timeshift_path.value, filename)):
                            filesize += os.path.getsize('%s%s.sc' % (config.usage.timeshift_path.value, filename))
                            self.BgFileEraser.erase('%s%s.sc' % (config.usage.timeshift_path.value, filename))
                        if not filename.startswith('timeshift.'):
                            filecounter -= 1
                elif statinfo.st_mtime < time() - 3600 * (24 + config.timeshift.timeshiftMaxHours.value):
                    if filename.endswith('.del') is True:
                        filesize += os.path.getsize('%s%s' % (config.usage.timeshift_path.value, filename))
                        try:
                            os.rename('%s%s' % (config.usage.timeshift_path.value, filename), '%s%s.del_again' % (config.usage.timeshift_path.value, filename))
                            self.BgFileEraser.erase('%s%s.del_again' % (config.usage.timeshift_path.value, filename))
                        except:
                            print "[TIMESHIFT] - can't rename %s%s." % (config.usage.timeshift_path.value, filename)
                            self.BgFileEraser.erase('%s%s' % (config.usage.timeshift_path.value, filename))

                    else:
                        filesize += os.path.getsize('%s%s' % (config.usage.timeshift_path.value, filename))
                        self.BgFileEraser.erase('%s%s' % (config.usage.timeshift_path.value, filename))

        if filecounter == 0:
            self.ptsEventCleanTimerSTOP()
        else:
            if timeshiftEnabled and not isSeekable:
                if freespace + filesize / 1024 / 1024 < int(config.timeshift.timeshiftCheckFreeSpace.value):
                    self.ptsAskUser('space')
                elif time() - self.pts_starttime > 3600 * config.timeshift.timeshiftMaxHours.value:
                    self.ptsAskUser('time')
            elif isSeekable:
                if freespace + filesize / 1024 / 1024 < int(config.timeshift.timeshiftCheckFreeSpace.value):
                    self.ptsAskUser('space_and_save')
                elif time() - self.pts_starttime > 3600 * config.timeshift.timeshiftMaxHours.value:
                    self.ptsAskUser('time_and_save')
            if self.checkEvents_value != int(config.timeshift.timeshiftCheckEvents.value):
                if self.pts_cleanEvent_timer.isActive():
                    self.pts_cleanEvent_timer.stop()
                    if int(config.timeshift.timeshiftCheckEvents.value):
                        self.ptsEventCleanTimerSTART()
                    else:
                        print "[TIMESHIFT] - 'cleanEvent_timer' is deactivated"
        self.checkEvents_value = int(config.timeshift.timeshiftCheckEvents.value)

    def ptsGetEventInfo(self):
        event = None
        try:
            serviceref = self.session.nav.getCurrentlyPlayingServiceOrGroup()
            serviceHandler = eServiceCenter.getInstance()
            info = serviceHandler.info(serviceref)
            self.pts_curevent_servicerefname = serviceref.toString()
            self.pts_curevent_station = info.getName(serviceref)
            service = self.session.nav.getCurrentService()
            info = service and service.info()
            event = info and info.getEvent(0)
        except Exception as errormsg:
            Notifications.AddNotification(MessageBox, _('Getting Event Info failed!') + '\n\n%s' % errormsg, MessageBox.TYPE_ERROR, timeout=10)

        if event is not None:
            curEvent = parseEvent(event)
            self.pts_curevent_begin = int(curEvent[0])
            self.pts_curevent_end = int(curEvent[1])
            self.pts_curevent_name = curEvent[2]
            self.pts_curevent_description = curEvent[3]
            self.pts_curevent_eventid = curEvent[4]
        return

    def ptsFrontpanelActions(self, action=None):
        if self.session.nav.RecordTimer.isRecording() or SystemInfo.get('NumFrontpanelLEDs', 0) == 0:
            return
        if action == 'start':
            if os.path.exists('/proc/stb/fp/led_set_pattern'):
                f = open('/proc/stb/fp/led_set_pattern', 'w')
                f.write('0xa7fccf7a')
                f.close()
            elif os.path.exists('/proc/stb/fp/led0_pattern'):
                f = open('/proc/stb/fp/led0_pattern', 'w')
                f.write('0x55555555')
                f.close()
            if os.path.exists('/proc/stb/fp/led_pattern_speed'):
                f = open('/proc/stb/fp/led_pattern_speed', 'w')
                f.write('20')
                f.close()
            elif os.path.exists('/proc/stb/fp/led_set_speed'):
                f = open('/proc/stb/fp/led_set_speed', 'w')
                f.write('20')
                f.close()
        elif action == 'stop':
            if os.path.exists('/proc/stb/fp/led_set_pattern'):
                f = open('/proc/stb/fp/led_set_pattern', 'w')
                f.write('0')
                f.close()
            elif os.path.exists('/proc/stb/fp/led0_pattern'):
                f = open('/proc/stb/fp/led0_pattern', 'w')
                f.write('0')
                f.close()

    def ptsCreateHardlink(self):
        for filename in os.listdir(config.usage.timeshift_path.value):
            if filename.startswith('timeshift.') and not filename.endswith('.sc') and not filename.endswith('.del') and not filename.endswith('.copy') and not filename.endswith('.ap'):
                if os.path.exists('%spts_livebuffer_%s.eit' % (config.usage.timeshift_path.value, self.pts_eventcount)):
                    self.BgFileEraser.erase('%spts_livebuffer_%s.eit' % (config.usage.timeshift_path.value, self.pts_eventcount))
                if os.path.exists('%spts_livebuffer_%s.meta' % (config.usage.timeshift_path.value, self.pts_eventcount)):
                    self.BgFileEraser.erase('%spts_livebuffer_%s.meta' % (config.usage.timeshift_path.value, self.pts_eventcount))
                if os.path.exists('%spts_livebuffer_%s' % (config.usage.timeshift_path.value, self.pts_eventcount)):
                    self.BgFileEraser.erase('%spts_livebuffer_%s' % (config.usage.timeshift_path.value, self.pts_eventcount))
                if os.path.exists('%spts_livebuffer_%s.sc' % (config.usage.timeshift_path.value, self.pts_eventcount)):
                    self.BgFileEraser.erase('%spts_livebuffer_%s.sc' % (config.usage.timeshift_path.value, self.pts_eventcount))
                try:
                    os.link('%s%s' % (config.usage.timeshift_path.value, filename), '%spts_livebuffer_%s' % (config.usage.timeshift_path.value, self.pts_eventcount))
                    os.link('%s%s.sc' % (config.usage.timeshift_path.value, filename), '%spts_livebuffer_%s.sc' % (config.usage.timeshift_path.value, self.pts_eventcount))
                    metafile = open('%spts_livebuffer_%s.meta' % (config.usage.timeshift_path.value, self.pts_eventcount), 'w')
                    metafile.write('%s\n%s\n%s\n%i\n' % (self.pts_curevent_servicerefname, self.pts_curevent_name.replace('\n', ''), self.pts_curevent_description.replace('\n', ''), int(self.pts_starttime)))
                    metafile.close()
                except Exception as errormsg:
                    pass

                self.ptsCreateEITFile('%spts_livebuffer_%s' % (config.usage.timeshift_path.value, self.pts_eventcount))
                if config.timeshift.autorecord.value:
                    try:
                        fullname = getRecordingFilename('%s - %s - %s' % (strftime('%Y%m%d %H%M', localtime(self.pts_starttime)), self.pts_curevent_station, self.pts_curevent_name), config.usage.autorecord_path.value)
                        os.link('%s%s' % (config.usage.timeshift_path.value, filename), '%s.ts' % fullname)
                        metafile = open('%s.ts.meta' % fullname, 'w')
                        metafile.write('%s\n%s\n%s\n%i\nautosaved\n' % (self.pts_curevent_servicerefname, self.pts_curevent_name.replace('\n', ''), self.pts_curevent_description.replace('\n', ''), int(self.pts_starttime)))
                        metafile.close()
                    except Exception as errormsg:
                        print '[TIMESHIFT] - %s' % errormsg

    def ptsRecordCurrentEvent(self):
        recording = RecordTimerEntry(ServiceReference(self.session.nav.getCurrentlyPlayingServiceOrGroup()), time(), self.pts_curevent_end, self.pts_curevent_name, self.pts_curevent_description, self.pts_curevent_eventid, afterEvent=AFTEREVENT.AUTO, justplay=False, always_zap=False, dirname=config.usage.autorecord_path.value)
        recording.dontSave = True
        self.session.nav.RecordTimer.record(recording)
        self.recording.append(recording)

    def ptsMergeRecords(self):
        if self.session.nav.RecordTimer.isRecording():
            self.pts_mergeRecords_timer.start(120000, True)
            return
        else:
            ptsmergeSRC = ''
            ptsmergeDEST = ''
            ptsmergeeventname = ''
            ptsgetnextfile = False
            ptsfilemerged = False
            filelist = os.listdir(config.usage.autorecord_path.value)
            if filelist is not None:
                filelist.sort()
            for filename in filelist:
                if filename.endswith('.meta'):
                    readmetafile = open('%s%s' % (config.usage.autorecord_path.value, filename), 'r')
                    servicerefname = readmetafile.readline()[0:-1]
                    eventname = readmetafile.readline()[0:-1]
                    eventtitle = readmetafile.readline()[0:-1]
                    eventtime = readmetafile.readline()[0:-1]
                    eventtag = readmetafile.readline()[0:-1]
                    readmetafile.close()
                    if ptsgetnextfile:
                        ptsgetnextfile = False
                        ptsmergeSRC = filename[0:-5]
                        if ASCIItranslit.legacyEncode(eventname) == ASCIItranslit.legacyEncode(ptsmergeeventname):
                            if fileExists('%s%s.eit' % (config.usage.autorecord_path.value, ptsmergeSRC[0:-3])):
                                copyfile('%s%s.eit' % (config.usage.autorecord_path.value, ptsmergeSRC[0:-3]), '%s%s.eit' % (config.usage.autorecord_path.value, ptsmergeDEST[0:-3]))
                            if os.path.exists('%s%s.ap' % (config.usage.autorecord_path.value, ptsmergeDEST)):
                                self.BgFileEraser.erase('%s%s.ap' % (config.usage.autorecord_path.value, ptsmergeDEST))
                            if os.path.exists('%s%s.sc' % (config.usage.autorecord_path.value, ptsmergeDEST)):
                                self.BgFileEraser.erase('%s%s.sc' % (config.usage.autorecord_path.value, ptsmergeDEST))
                            JobManager.AddJob(MergeTimeshiftJob(self, 'cat "%s%s" >> "%s%s"' % (config.usage.autorecord_path.value, ptsmergeSRC, config.usage.autorecord_path.value, ptsmergeDEST), ptsmergeSRC, ptsmergeDEST, eventname))
                            config.timeshift.isRecording.value = True
                            ptsfilemerged = True
                        else:
                            ptsgetnextfile = True
                    if eventtag == 'pts_merge' and not ptsgetnextfile:
                        ptsgetnextfile = True
                        ptsmergeDEST = filename[0:-5]
                        ptsmergeeventname = eventname
                        ptsfilemerged = False
                        if fileExists('%s%s' % (config.usage.autorecord_path.value, ptsmergeDEST)):
                            statinfo = os.stat('%s%s' % (config.usage.autorecord_path.value, ptsmergeDEST))
                            if statinfo.st_mtime > time() - 10.0:
                                self.pts_mergeRecords_timer.start(120000, True)
                                return
                        metafile = open('%s%s.meta' % (config.usage.autorecord_path.value, ptsmergeDEST), 'w')
                        metafile.write('%s\n%s\n%s\n%i\n' % (servicerefname, eventname.replace('\n', ''), eventtitle.replace('\n', ''), int(eventtime)))
                        metafile.close()

            if not ptsfilemerged and ptsgetnextfile:
                Notifications.AddNotification(MessageBox, _('[Timeshift] Merging records failed!'), MessageBox.TYPE_ERROR, timeout=30)
            return

    def ptsCreateAPSCFiles(self, filename):
        if fileExists(filename, 'r'):
            if fileExists(filename + '.meta', 'r'):
                readmetafile = open(filename + '.meta', 'r')
                servicerefname = readmetafile.readline()[0:-1]
                eventname = readmetafile.readline()[0:-1]
                readmetafile.close()
            else:
                eventname = ''
            JobManager.AddJob(CreateAPSCFilesJob(self, '/usr/lib/enigma2/python/Components/createapscfiles "%s" > /dev/null' % filename, eventname))
        else:
            self.ptsSaveTimeshiftFinished()

    def ptsCreateEITFile(self, filename):
        if self.pts_curevent_eventid is not None:
            try:
                serviceref = ServiceReference(self.session.nav.getCurrentlyPlayingServiceOrGroup()).ref
                eEPGCache.getInstance().saveEventToFile(filename + '.eit', serviceref, self.pts_curevent_eventid, -1, -1)
            except Exception as errormsg:
                print '[TIMESHIFT] - %s' % errormsg

        return

    def ptsCopyFilefinished(self, srcfile, destfile):
        if fileExists(srcfile):
            self.BgFileEraser.erase(srcfile)
        if self.pts_mergeRecords_timer.isActive():
            self.pts_mergeRecords_timer.stop()
            self.pts_mergeRecords_timer.start(15000, True)
        else:
            self.ptsCreateAPSCFiles(destfile)

    def ptsMergeFilefinished(self, srcfile, destfile):
        if self.session.nav.RecordTimer.isRecording() or len(JobManager.getPendingJobs()) >= 1:
            self.pts_mergeCleanUp_timer.start(120000, True)
            os.system('echo "" > "%s.pts.del"' % srcfile[0:-3])
        else:
            self.BgFileEraser.erase('%s' % srcfile)
            self.BgFileEraser.erase('%s.ap' % srcfile)
            self.BgFileEraser.erase('%s.sc' % srcfile)
            self.BgFileEraser.erase('%s.meta' % srcfile)
            self.BgFileEraser.erase('%s.cuts' % srcfile)
            self.BgFileEraser.erase('%s.eit' % srcfile[0:-3])
        self.ptsCreateAPSCFiles(destfile)
        self.pts_mergeRecords_timer.start(10000, True)

    def ptsSaveTimeshiftFinished(self):
        if not self.pts_mergeCleanUp_timer.isActive():
            self.ptsFrontpanelActions('stop')
            config.timeshift.isRecording.value = False
        if Screens.Standby.inTryQuitMainloop:
            self.pts_QuitMainloop_timer.start(30000, True)
        else:
            Notifications.AddNotification(MessageBox, _('Timeshift saved to your harddisk!'), MessageBox.TYPE_INFO, timeout=30)

    def ptsMergePostCleanUp(self):
        if self.session.nav.RecordTimer.isRecording() or len(JobManager.getPendingJobs()) >= 1:
            config.timeshift.isRecording.value = True
            self.pts_mergeCleanUp_timer.start(120000, True)
            return
        self.ptsFrontpanelActions('stop')
        config.timeshift.isRecording.value = False
        filelist = os.listdir(config.usage.autorecord_path.value)
        for filename in filelist:
            if filename.endswith('.pts.del'):
                srcfile = config.usage.autorecord_path.value + '/' + filename[0:-8] + '.ts'
                self.BgFileEraser.erase('%s' % srcfile)
                self.BgFileEraser.erase('%s.ap' % srcfile)
                self.BgFileEraser.erase('%s.sc' % srcfile)
                self.BgFileEraser.erase('%s.meta' % srcfile)
                self.BgFileEraser.erase('%s.cuts' % srcfile)
                self.BgFileEraser.erase('%s.eit' % srcfile[0:-3])
                self.BgFileEraser.erase('%s.pts.del' % srcfile[0:-3])
                if Screens.Standby.inTryQuitMainloop and self.pts_QuitMainloop_timer.isActive():
                    self.pts_QuitMainloop_timer.start(60000, True)

    def ptsTryQuitMainloop(self):
        if Screens.Standby.inTryQuitMainloop and (len(JobManager.getPendingJobs()) >= 1 or self.pts_mergeCleanUp_timer.isActive()):
            self.pts_QuitMainloop_timer.start(60000, True)
            return
        else:
            if Screens.Standby.inTryQuitMainloop and self.session.ptsmainloopvalue:
                self.session.dialog_stack = []
                self.session.summary_stack = [
                 None]
                self.session.open(Screens.Standby.TryQuitMainloop, self.session.ptsmainloopvalue)
            return

    def ptsGetSeekInfo(self):
        s = self.session.nav.getCurrentService()
        return s and s.seek()

    def ptsGetPosition(self):
        seek = self.ptsGetSeekInfo()
        if seek is None:
            return
        else:
            pos = seek.getPlayPosition()
            if pos[0]:
                return 0
            return pos[1]

    def ptsGetLength(self):
        seek = self.ptsGetSeekInfo()
        if seek is None:
            return
        else:
            length = seek.getLength()
            if length[0]:
                return 0
            return length[1]

    def ptsGetTimeshiftStatus(self):
        if (self.isSeekable() and self.timeshiftEnabled() or self.save_current_timeshift) and config.usage.check_timeshift.value:
            return True
        else:
            return False

    def ptsSeekPointerOK(self):
        if self.pvrStateDialog.has_key('PTSSeekPointer') and self.timeshiftEnabled() and self.isSeekable():
            if not self.pvrStateDialog.shown:
                if self.seekstate != self.SEEK_STATE_PLAY or self.seekstate == self.SEEK_STATE_PAUSE:
                    self.setSeekState(self.SEEK_STATE_PLAY)
                self.doShow()
                return
            length = self.ptsGetLength()
            position = self.ptsGetPosition()
            if length is None or position is None:
                return
            cur_pos = self.pvrStateDialog['PTSSeekPointer'].position
            jumptox = int(cur_pos[0]) - (int(self.pvrStateDialog['PTSSeekBack'].instance.position().x()) + 8)
            jumptoperc = round(jumptox / float(self.pvrStateDialog['PTSSeekBack'].instance.size().width()) * 100, 0)
            jumptotime = int(length / 100 * jumptoperc)
            jumptodiff = position - jumptotime
            self.doSeekRelative(-jumptodiff)
        else:
            return
        return

    def ptsSeekPointerLeft(self):
        if self.pvrStateDialog.has_key('PTSSeekPointer') and self.pvrStateDialog.shown and self.timeshiftEnabled() and self.isSeekable():
            self.ptsMoveSeekPointer(direction='left')
        else:
            return

    def ptsSeekPointerRight(self):
        if self.pvrStateDialog.has_key('PTSSeekPointer') and self.pvrStateDialog.shown and self.timeshiftEnabled() and self.isSeekable():
            self.ptsMoveSeekPointer(direction='right')
        else:
            return

    def ptsSeekPointerReset(self):
        if self.pvrStateDialog.has_key('PTSSeekPointer') and self.timeshiftEnabled():
            self.pvrStateDialog['PTSSeekPointer'].setPosition(int(self.pvrStateDialog['PTSSeekBack'].instance.position().x()) + 8, self.pvrStateDialog['PTSSeekPointer'].position[1])

    def ptsSeekPointerSetCurrentPos(self):
        if not self.pvrStateDialog.has_key('PTSSeekPointer') or not self.timeshiftEnabled() or not self.isSeekable():
            return
        position = self.ptsGetPosition()
        length = self.ptsGetLength()
        if length >= 1:
            tpixels = int(float(int(position * 100 / length)) / 100 * self.pvrStateDialog['PTSSeekBack'].instance.size().width())
            self.pvrStateDialog['PTSSeekPointer'].setPosition(int(self.pvrStateDialog['PTSSeekBack'].instance.position().x()) + 8 + tpixels, self.pvrStateDialog['PTSSeekPointer'].position[1])

    def ptsMoveSeekPointer(self, direction=None):
        if direction is None or not self.pvrStateDialog.has_key('PTSSeekPointer'):
            return
        else:
            isvalidjump = False
            cur_pos = self.pvrStateDialog['PTSSeekPointer'].position
            self.doShow()
            if direction == 'left':
                minmaxval = int(self.pvrStateDialog['PTSSeekBack'].instance.position().x()) + 8
                movepixels = -15
                if cur_pos[0] + movepixels > minmaxval:
                    isvalidjump = True
            elif direction == 'right':
                minmaxval = int(self.pvrStateDialog['PTSSeekBack'].instance.size().width() * 0.96)
                movepixels = 15
                if cur_pos[0] + movepixels < minmaxval:
                    isvalidjump = True
            else:
                return 0
            if isvalidjump:
                self.pvrStateDialog['PTSSeekPointer'].setPosition(cur_pos[0] + movepixels, cur_pos[1])
            else:
                self.pvrStateDialog['PTSSeekPointer'].setPosition(minmaxval, cur_pos[1])
            return

    def ptsCheckFileChanged(self):
        if not self.timeshiftEnabled():
            self.pts_CheckFileChanged_timer.stop()
            return
        if self.pts_CheckFileChanged_counter >= 5 and not self.pts_file_changed:
            if self.pts_switchtolive:
                if config.timeshift.showlivetvmsg.value:
                    self.ptsAskUser('livetv')
            elif self.pts_lastplaying <= self.pts_currplaying:
                self.ptsAskUser('nextfile')
            else:
                Notifications.AddNotification(MessageBox, _("Can't play the previous timeshift file! You can try again."), MessageBox.TYPE_INFO, timeout=3)
                self.doSeek(0)
                self.setSeekState(self.SEEK_STATE_PLAY)
            self.pts_currplaying = self.pts_lastplaying
            self.pts_CheckFileChanged_timer.stop()
            return
        self.pts_CheckFileChanged_counter += 1
        if self.pts_file_changed:
            self.pts_CheckFileChanged_timer.stop()
            if self.posDiff:
                self.pts_SeekToPos_timer.start(1000, True)
            elif self.pts_FileJump_timer.isActive():
                self.pts_FileJump_timer.stop()
            elif self.pts_lastplaying > self.pts_currplaying:
                self.pts_SeekBack_timer.start(1000, True)
        else:
            self.doSeek(7776000000)

    def ptsTimeshiftFileChanged(self):
        self.pts_file_changed = True
        self.ptsSeekPointerReset()
        if self.pts_switchtolive:
            self.pts_switchtolive = False
            self.pts_nextplaying = 0
            self.pts_currplaying = self.pts_eventcount
            return
        if self.pts_nextplaying:
            self.pts_currplaying = self.pts_nextplaying
        self.pts_nextplaying = self.pts_currplaying + 1
        if fileExists('%spts_livebuffer_%s' % (config.usage.timeshift_path.value, self.pts_nextplaying), 'r'):
            self.ptsSetNextPlaybackFile('pts_livebuffer_%s' % self.pts_nextplaying)
            self.pts_switchtolive = False
        else:
            self.ptsSetNextPlaybackFile('')
            self.pts_switchtolive = True

    def ptsSetNextPlaybackFile(self, nexttsfile):
        ts = self.getTimeshift()
        if ts is None:
            return
        else:
            if nexttsfile:
                ts.setNextPlaybackFile('%s%s' % (config.usage.timeshift_path.value, nexttsfile))
            else:
                ts.setNextPlaybackFile('')
            return

    def ptsSeekToPos(self):
        length = self.ptsGetLength()
        if length is None:
            return
        else:
            if self.posDiff < 0:
                if length <= abs(self.posDiff):
                    self.posDiff = 0
            elif length <= abs(self.posDiff):
                tmp = length - 900000
                if tmp < 0:
                    tmp = 0
                self.posDiff = tmp
            self.setSeekState(self.SEEK_STATE_PLAY)
            self.doSeek(self.posDiff)
            self.posDiff = 0
            return

    def ptsSeekBackTimer(self):
        self.doSeek(-900000)
        self.setSeekState(self.SEEK_STATE_PAUSE)
        self.pts_StartSeekBackTimer.start(1000, True)

    def ptsStartSeekBackTimer(self):
        if self.pts_lastseekspeed == 0:
            self.setSeekState(self.makeStateBackward(int(config.seek.enter_backward.value)))
        else:
            self.setSeekState(self.makeStateBackward(int(-self.pts_lastseekspeed)))

    def ptsCheckTimeshiftPath(self):
        if fileExists(config.usage.timeshift_path.value, 'w'):
            return True
        else:
            if self.pts_delay_timer.isActive():
                self.pts_delay_timer.stop()
            if self.pts_cleanUp_timer.isActive():
                self.pts_cleanUp_timer.stop()
            return False

    def ptsTimerEntryStateChange(self, timer):
        if not config.timeshift.stopwhilerecording.value:
            return
        self.pts_record_running = self.session.nav.RecordTimer.isRecording()
        if self.session.screen['Standby'].boolean is True:
            return
        if timer.state == TimerEntry.StateRunning and self.timeshiftEnabled() and self.pts_record_running:
            if self.seekstate != self.SEEK_STATE_PLAY:
                self.setSeekState(self.SEEK_STATE_PLAY)
            if self.isSeekable():
                Notifications.AddNotification(MessageBox, _('Record started! Stopping timeshift now ...'), MessageBox.TYPE_INFO, timeout=30)
            self.switchToLive = False
            self.stopTimeshiftcheckTimeshiftRunningCallback(True)
        if timer.state == TimerEntry.StateEnded:
            if not self.timeshiftEnabled() and not self.pts_record_running:
                self.autostartAutorecordTimeshift()
            if self.pts_mergeRecords_timer.isActive():
                self.pts_mergeRecords_timer.stop()
                self.pts_mergeRecords_timer.start(15000, True)
                self.ptsFrontpanelActions('start')
                config.timeshift.isRecording.value = True
            else:
                jobs = JobManager.getPendingJobs()
                if len(jobs) >= 1:
                    for job in jobs:
                        jobname = str(job.name)
                        if jobname == _('Saving Timeshift files') or jobname == _('Creating AP and SC Files') or jobname == _('Merging Timeshift files'):
                            self.ptsFrontpanelActions('start')
                            config.timeshift.isRecording.value = True
                            break

    def ptsLiveTVStatus(self):
        service = self.session.nav.getCurrentService()
        info = service and service.info()
        sTSID = info and info.getInfo(iServiceInformation.sTSID) or -1
        if sTSID is None or sTSID == -1:
            return False
        else:
            return True
            return