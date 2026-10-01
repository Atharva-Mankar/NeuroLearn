/**
 * NeuroLearn demo data
 * --------------------
 * Every piece of fake data used by the UI lives in this one file.
 *
 * In a later phase this file is replaced by real data from the FastAPI
 * backend. Nothing else in the app should contain hard-coded example values,
 * so that swapping `demoData` for `apiData` is a small, contained change.
 */

/** The signed-in student. Replaced by the real user profile in a later phase. */
export const demoUser = {
  name: 'Atharva',
  email: 'atharva@example.com',
}

/** Subjects a student can pick from when starting a session. */
export const subjects = [
  'Machine Learning',
  'Data Science',
  'Mathematics',
  'Computer Vision',
  'Statistics',
  'Deep Learning',
  'Natural Language Processing',
  'Reinforcement Learning',
  'Other',
]

/** The three fatigue levels the product uses everywhere. */
export const fatigueLevels = ['Low', 'Medium', 'High']

/** Shared note shown wherever an estimated fatigue value appears. */
export const fatigueDisclaimer =
  'An approximate study-productivity signal, not a medical diagnosis.'

/** Everything the Dashboard page needs. */
export const dashboard = {
  studyProgress: {
    percent: 68,
    label: 'Weekly Study Progress',
    detail: '8.5 of 12.5 hours this week',
  },
  fatigue: {
    level: 'Medium',
    // 0-100, used only to size the bar in the indicator.
    score: 52,
  },
  timeline: [
    { time: '7:00 PM', subject: 'Machine Learning', duration: '45 min', kind: 'study' },
    { time: '8:00 PM', subject: 'Data Science', duration: '30 min', kind: 'study' },
    { time: '9:00 PM', subject: 'Break', duration: '15 min', kind: 'break' },
    { time: '9:30 PM', subject: 'Review notes', duration: '20 min', kind: 'study' },
  ],
  recentSessions: [
    {
      id: 1,
      subject: 'Machine Learning',
      topic: 'Neural networks',
      duration: '45 min',
      fatigue: 'Low',
      date: 'Sep 28',
    },
    {
      id: 2,
      subject: 'Data Science',
      topic: 'Pandas and NumPy',
      duration: '30 min',
      fatigue: 'Medium',
      date: 'Sep 27',
    },
    {
      id: 3,
      subject: 'Mathematics',
      topic: 'Linear algebra',
      duration: '60 min',
      fatigue: 'High',
      date: 'Sep 26',
    },
    {
      id: 4,
      subject: 'Computer Vision',
      topic: 'OpenCV basics',
      duration: '40 min',
      fatigue: 'Low',
      date: 'Sep 25',
    },
  ],
  recommendations: [
    {
      id: 1,
      title: 'Take a short break first',
      reason:
        'Your estimated fatigue is medium, and your last two sessions were back to back.',
      action: 'A 10-15 minute break before your next focused block.',
    },
    {
      id: 2,
      title: 'Best focus window is 7-9 PM',
      reason:
        'Across your recent history, sessions in this window ended with the lowest fatigue estimate.',
      action: 'Schedule your hardest subject in this window.',
    },
    {
      id: 3,
      title: 'One session from your weekly goal',
      reason:
        'You are at 68% of this week’s study target with four days remaining.',
      action: 'A 45-minute session would complete the goal.',
    },
  ],
}

/** The full session list used by the History page and the calendar. */
export const sessions = [
  {
    id: 1,
    subject: 'Machine Learning',
    topic: 'Neural networks',
    minutes: 45,
    fatigue: 'Low',
    date: '2024-09-28',
    status: 'Completed',
  },
  {
    id: 2,
    subject: 'Data Science',
    topic: 'Pandas and NumPy',
    minutes: 30,
    fatigue: 'Medium',
    date: '2024-09-27',
    status: 'Completed',
  },
  {
    id: 3,
    subject: 'Mathematics',
    topic: 'Linear algebra',
    minutes: 60,
    fatigue: 'High',
    date: '2024-09-26',
    status: 'Completed',
  },
  {
    id: 4,
    subject: 'Computer Vision',
    topic: 'OpenCV basics',
    minutes: 40,
    fatigue: 'Low',
    date: '2024-09-25',
    status: 'Completed',
  },
  {
    id: 5,
    subject: 'Statistics',
    topic: 'Probability distributions',
    minutes: 50,
    fatigue: 'Medium',
    date: '2024-09-24',
    status: 'Completed',
  },
  {
    id: 6,
    subject: 'Deep Learning',
    topic: 'Convolutional networks',
    minutes: 55,
    fatigue: 'High',
    date: '2024-09-23',
    status: 'Completed',
  },
  {
    id: 7,
    subject: 'Natural Language Processing',
    topic: 'Transformers',
    minutes: 35,
    fatigue: 'Low',
    date: '2024-09-22',
    status: 'Completed',
  },
  {
    id: 8,
    subject: 'Reinforcement Learning',
    topic: 'Q-learning',
    minutes: 45,
    fatigue: 'Medium',
    date: '2024-09-21',
    status: 'Completed',
  },
  {
    id: 9,
    subject: 'Machine Learning',
    topic: 'Model evaluation',
    minutes: 50,
    fatigue: 'Medium',
    date: '2024-09-20',
    status: 'Completed',
  },
  {
    id: 10,
    subject: 'Data Science',
    topic: 'Data cleaning',
    minutes: 25,
    fatigue: 'Low',
    date: '2024-09-19',
    status: 'Completed',
  },
  {
    id: 11,
    subject: 'Mathematics',
    topic: 'Probability basics',
    minutes: 40,
    fatigue: 'Low',
    date: '2024-09-18',
    status: 'Completed',
  },
  {
    id: 12,
    subject: 'Computer Vision',
    topic: 'Image filters',
    minutes: 35,
    fatigue: 'Medium',
    date: '2024-09-17',
    status: 'Completed',
  },
]

/** Planned study blocks shown on the Calendar page. */
export const calendarEvents = [
  {
    id: 1,
    title: 'Machine Learning',
    date: '2024-09-28',
    startTime: '19:00',
    endTime: '19:45',
    type: 'study',
  },
  {
    id: 2,
    title: 'Data Science',
    date: '2024-09-28',
    startTime: '20:00',
    endTime: '20:30',
    type: 'study',
  },
  {
    id: 3,
    title: 'Break',
    date: '2024-09-28',
    startTime: '21:00',
    endTime: '21:15',
    type: 'break',
  },
  {
    id: 4,
    title: 'Mathematics',
    date: '2024-09-27',
    startTime: '18:30',
    endTime: '19:30',
    type: 'study',
  },
  {
    id: 5,
    title: 'Computer Vision',
    date: '2024-09-26',
    startTime: '19:00',
    endTime: '19:40',
    type: 'study',
  },
  {
    id: 6,
    title: 'Statistics',
    date: '2024-09-24',
    startTime: '20:00',
    endTime: '20:50',
    type: 'study',
  },
  {
    id: 7,
    title: 'Deep Learning',
    date: '2024-09-23',
    startTime: '19:00',
    endTime: '19:55',
    type: 'study',
  },
  {
    id: 8,
    title: 'Natural Language Processing',
    date: '2024-09-22',
    startTime: '18:00',
    endTime: '18:35',
    type: 'study',
  },
  {
    id: 9,
    title: 'Reinforcement Learning',
    date: '2024-09-21',
    startTime: '20:00',
    endTime: '20:45',
    type: 'study',
  },
  {
    id: 10,
    title: 'Machine Learning',
    date: '2024-09-20',
    startTime: '19:30',
    endTime: '20:20',
    type: 'study',
  },
  {
    id: 11,
    title: 'Data Science',
    date: '2024-09-19',
    startTime: '17:00',
    endTime: '17:25',
    type: 'study',
  },
]

/** Numbers and simple series used by the Insights page. */
export const insights = {
  studyTime: {
    label: 'Study Time',
    value: '8.5',
    unit: 'hours this week',
    change: '+12% vs last week',
  },
  sessionsCompleted: {
    label: 'Sessions Completed',
    value: '28',
    unit: 'this month',
    change: '12 day streak',
  },
  averageDuration: {
    label: 'Average Session',
    value: '42',
    unit: 'minutes',
    change: '45 min this week',
  },
  // One number per bar in the fatigue trend chart. 0-100.
  fatigueTrend: {
    label: 'Fatigue Trend',
    // Each entry is one day, most recent last.
    days: [
      { day: 'Mon', score: 35 },
      { day: 'Tue', score: 42 },
      { day: 'Wed', score: 55 },
      { day: 'Thu', score: 48 },
      { day: 'Fri', score: 52 },
      { day: 'Sat', score: 40 },
      { day: 'Sun', score: 30 },
    ],
    disclaimer: fatigueDisclaimer,
  },
  // Hours per subject. Together these add up to the monthly total.
  subjectDistribution: {
    label: 'Subject Distribution',
    totalHours: 42.5,
    items: [
      { subject: 'Machine Learning', hours: 12.5 },
      { subject: 'Data Science', hours: 8.0 },
      { subject: 'Mathematics', hours: 6.5 },
      { subject: 'Computer Vision', hours: 5.0 },
      { subject: 'Statistics', hours: 4.5 },
      { subject: 'Other', hours: 6.0 },
    ],
  },
}

/** Default values shown on the Settings page. */
export const settingsDefaults = {
  profile: {
    name: 'Atharva',
    email: 'atharva@example.com',
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
}

export const dashboardData = {
  user: demoUser,
  studyProgress: {
    percentage: dashboard.studyProgress.percent,
    description: dashboard.studyProgress.detail,
  },
  fatigueLevel: {
    label: 'Estimated fatigue',
    value: dashboard.fatigue.level,
    level: dashboard.fatigue.score,
    disclaimer: fatigueDisclaimer,
  },
  timeline: dashboard.timeline,
  recentSessions: dashboard.recentSessions,
  suggestions: dashboard.recommendations.map(({ title, reason }) => ({
    title,
    description: reason,
  })),
  calendarPreview: calendarEvents.map(({ date }) => ({ date, sessions: 1 })),
}

export const sessionsData = sessions.map(session => ({
  ...session,
  duration: `${session.minutes} min`,
  status: session.status.toLowerCase(),
}))

const subjectColors = ['blue-500', 'green-500', 'yellow-500', 'purple-500', 'red-500', 'slate-500']

export const insightsData = {
  studyTime: {
    totalHours: Number(insights.studyTime.value),
    changePercent: 12,
  },
  sessionsCompleted: {
    total: Number(insights.sessionsCompleted.value),
    thisWeek: 7,
    streak: 12,
  },
  avgDuration: {
    overall: Number(insights.averageDuration.value),
    thisWeek: 45,
  },
  fatigueTrend: insights.fatigueTrend.days.map(({ day, score }) => ({
    day,
    level: score,
  })),
  subjectDistribution: insights.subjectDistribution.items.map((item, index) => ({
    ...item,
    color: subjectColors[index],
  })),
}

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
}
