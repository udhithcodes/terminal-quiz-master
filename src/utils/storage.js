// ─────────────────────────────────────────────────
// LocalStorage Utility — Terminal Quiz Master
// ─────────────────────────────────────────────────

const KEY = {
  PROGRESS: 'tqm_progress',
  HIGH_SCORES: 'tqm_high_scores',
  STREAK: 'tqm_streak',
  ACHIEVEMENTS: 'tqm_achievements',
  THEME: 'tqm_theme',
};

// Generic helpers
const save = (key, data) => {
  try {
    localStorage.setItem(key, JSON.stringify(data));
  } catch (e) {
    console.warn('LocalStorage write failed:', e);
  }
};

const load = (key, fallback = null) => {
  try {
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : fallback;
  } catch (e) {
    console.warn('LocalStorage read failed:', e);
    return fallback;
  }
};

// ─── Progress ───
export const getProgress = () =>
  load(KEY.PROGRESS, {
    totalXP: 0,
    level: 1,
    basic: { completed: 0, bestScore: 0, attempts: 0 },
    intermediate: { completed: 0, bestScore: 0, attempts: 0 },
    advanced: { completed: 0, bestScore: 0, attempts: 0 },
  });

export const saveQuizResult = ({ level, score, total, xpEarned }) => {
  const progress = getProgress();
  const percentage = Math.round((score / total) * 100);

  progress.totalXP += xpEarned;
  progress.level = Math.floor(progress.totalXP / 200) + 1;

  const lvl = progress[level];
  lvl.attempts += 1;
  lvl.completed += 1;
  if (percentage > lvl.bestScore) lvl.bestScore = percentage;

  save(KEY.PROGRESS, progress);
  updateStreak();
  return progress;
};

// ─── High Scores ───
export const getHighScores = () =>
  load(KEY.HIGH_SCORES, { basic: 0, intermediate: 0, advanced: 0 });

export const updateHighScore = (level, score) => {
  const scores = getHighScores();
  if (score > scores[level]) {
    scores[level] = score;
    save(KEY.HIGH_SCORES, scores);
  }
};

// ─── Streak ───
export const getStreak = () =>
  load(KEY.STREAK, { current: 0, best: 0, lastDate: null });

export const updateStreak = () => {
  const streak = getStreak();
  const today = new Date().toDateString();
  const yesterday = new Date(Date.now() - 86400000).toDateString();

  if (streak.lastDate === today) return streak;
  if (streak.lastDate === yesterday) {
    streak.current += 1;
  } else if (streak.lastDate !== today) {
    streak.current = 1;
  }

  if (streak.current > streak.best) streak.best = streak.current;
  streak.lastDate = today;
  save(KEY.STREAK, streak);
  return streak;
};

// ─── Achievements ───
const ACHIEVEMENTS_DEF = [
  { id: 'first_quiz', title: 'First Steps', desc: 'Complete your first quiz', icon: '🎯', condition: (p) => Object.values(p).filter(v => v?.completed).some(v => v.completed >= 1) },
  { id: 'perfect_basic', title: 'Flawless Beginner', desc: 'Score 100% on Basic level', icon: '⭐', condition: (p) => p.basic?.bestScore === 100 },
  { id: 'advanced_attempt', title: 'Brave Soul', desc: 'Attempt the Advanced quiz', icon: '👑', condition: (p) => p.advanced?.attempts >= 1 },
  { id: 'level_5', title: 'Level 5', desc: 'Reach level 5', icon: '🔥', condition: (p) => p.level >= 5 },
  { id: 'xp_500', title: 'XP Collector', desc: 'Earn 500+ total XP', icon: '💎', condition: (p) => p.totalXP >= 500 },
];

export const getAchievements = () => {
  const progress = getProgress();
  const unlocked = load(KEY.ACHIEVEMENTS, []);
  return ACHIEVEMENTS_DEF.map((a) => ({
    ...a,
    unlocked: unlocked.includes(a.id) || a.condition(progress),
  }));
};

export const checkNewAchievements = () => {
  const progress = getProgress();
  const currentUnlocked = load(KEY.ACHIEVEMENTS, []);
  const newlyUnlocked = [];

  ACHIEVEMENTS_DEF.forEach((a) => {
    if (!currentUnlocked.includes(a.id) && a.condition(progress)) {
      currentUnlocked.push(a.id);
      newlyUnlocked.push(a);
    }
  });

  if (newlyUnlocked.length) save(KEY.ACHIEVEMENTS, currentUnlocked);
  return newlyUnlocked;
};

// ─── Theme ───
export const getTheme = () => load(KEY.THEME, 'light');
export const saveTheme = (theme) => save(KEY.THEME, theme);

// ─── Reset ───
export const resetAllProgress = () => {
  Object.values(KEY).forEach((k) => localStorage.removeItem(k));
};
