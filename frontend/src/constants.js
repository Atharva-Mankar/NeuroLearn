/**
 * NeuroLearn UI constants - values that are part of the product configuration,
 * not fake user data or demo content.
 *
 * These values can safely be shared with the backend or stored in the app
 * without being mistaken for personalized or fabricated metrics.
 */

/**
 * Subjects a student can pick from when starting a session.
 * This is a fixed list of UI options, not personalized recommendations.
 */
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
];

/**
 * The three fatigue levels the product uses everywhere.
 */
export const fatigueLevels = ['Low', 'Medium', 'High'];

/**
 * Shared note shown wherever an estimated fatigue value appears.
 * Kept here so every surface shares one definition. Fatigue values themselves
 * do not exist yet (no webcam monitoring), so nothing currently renders this.
 */
export const fatigueDisclaimer =
  'An approximate study-productivity signal, not a medical diagnosis.';