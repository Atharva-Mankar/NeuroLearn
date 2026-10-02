/**
 * NeuroLearn settings defaults.
 *
 * These are product defaults for the Settings page form -- timezone, preferred
 * study hours, break intervals, webcam sampling rate. They are configuration,
 * not fabricated user data, and the Settings page has no backend yet so it
 * cannot read anything real.
 *
 * When Settings is wired to a real backend in a later phase, these become the
 * initial values for an empty profile.
 */

/** Default values shown on the Settings page. */
export const settingsDefaults = {
  profile: {
    name: '',
    email: '',
    timezone: 'Asia/Kolkata (UTC+5:30)',
  },
  study: {
    dailyGoalMinutes: 90,
    weeklyGoalHours: 12.5,
    preferredStart: '19:00',
    breakEveryMinutes: 50,
  },
  session: {
    defaultDurationMinutes: 45,
    autoPauseOnInactive: true,
    pauseAfterMinutes: 10,
    showFatigueLive: true,
  },
  webcam: {
    defaultEnabled: false,
    samplingRate: 'medium',
    showPreviewDuringSession: true,
    // Stated plainly so the privacy promise is visible in the UI itself.
    privacyNote:
      'Video is analysed on this device and discarded. NeuroLearn never records or uploads camera footage.',
  },
};

/** Shape of the Settings form state, derived from the defaults. */
export const settingsData = {
  profile: {
    name: settingsDefaults.profile.name,
    email: settingsDefaults.profile.email,
    timezone: 'UTC+5:30',
    language: 'English',
  },
  studyPreferences: {
    weeklyGoalHours: settingsDefaults.study.weeklyGoalHours,
    dailyGoalMinutes: settingsDefaults.study.dailyGoalMinutes,
    preferredStartTime: settingsDefaults.study.preferredStart,
    preferredEndTime: '21:00',
    breakReminderInterval: settingsDefaults.study.breakEveryMinutes,
  },
  sessionPreferences: {
    defaultDuration: settingsDefaults.session.defaultDurationMinutes,
    autoPauseOnInactivity: settingsDefaults.session.autoPauseOnInactive,
    inactivityThreshold: settingsDefaults.session.pauseAfterMinutes,
    showFatigueDuringSession: settingsDefaults.session.showFatigueLive,
    playCompletionSound: true,
  },
  webcamPreferences: {
    enableMonitoring: settingsDefaults.webcam.defaultEnabled,
    monitoringFrequency: settingsDefaults.webcam.samplingRate,
    saveFrames: false,
    privacyMode: true,
  },
};