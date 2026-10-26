import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Zap, Trophy, Flame, Star, Target, RotateCcw, CheckCircle } from 'lucide-react';
import ProgressBar from '../components/ProgressBar';
import { getProgress, getStreak, getAchievements, resetAllProgress } from '../utils/storage';
import { getLevelConfig } from '../data/questions';
import './Dashboard.css';

const Dashboard = () => {
  const navigate = useNavigate();
  const [progress, setProgress] = useState(null);
  const [streak, setStreak] = useState(null);
  const [achievements, setAchievements] = useState([]);
  const [levels] = useState(getLevelConfig());

  const loadData = () => {
    setProgress(getProgress());
    setStreak(getStreak());
    setAchievements(getAchievements());
  };

  useEffect(() => { loadData(); }, []);

  const handleReset = () => {
    if (window.confirm('Are you sure you want to reset all progress? This cannot be undone.')) {
      resetAllProgress();
      loadData();
    }
  };

  if (!progress) return null;

  const xpToNextLevel = 200;
  const xpInCurrentLevel = progress.totalXP % xpToNextLevel;
  const totalQuizzes = (progress.basic?.completed || 0) + (progress.intermediate?.completed || 0) + (progress.advanced?.completed || 0);
  const unlockedAchievements = achievements.filter((a) => a.unlocked);

  return (
    <main className="dashboard-page">
      <div className="db-bg">
        <div className="db-bg-circle" />
      </div>
      <div className="container db-container">
        {/* ── Header ── */}
        <div className="db-header animate-fadeInUp">
          <div>
            <div className="badge badge-orange" style={{ marginBottom: '0.5rem' }}>
              <Zap size={12} /> YOUR PROFILE
            </div>
            <h1 className="section-title">Learning Dashboard</h1>
            <p className="section-subtitle">Track your XP, streaks, and coding mastery</p>
          </div>
          <button className="btn btn-secondary db-reset-btn" onClick={handleReset}>
            <RotateCcw size={14} />
            Reset Progress
          </button>
        </div>

        {/* ── Profile Card ── */}
        <div className="db-profile-card animate-fadeInUp" style={{ animationDelay: '0.1s' }}>
          <div className="db-profile-left">
            <div className="db-avatar">🧑‍💻</div>
            <div>
              <div className="db-player-name">You</div>
              <div className="db-player-rank">
                {progress.totalXP >= 500 ? '🏆 Coding Legend' :
                  progress.totalXP >= 300 ? '⭐ Skilled Coder' :
                  progress.totalXP >= 100 ? '🔥 Rising Challenger' : '📚 Training Arc'}
              </div>
            </div>
          </div>

          <div className="db-level-section">
            <div className="db-level-num">
              <span className="db-lv-label">LV</span>
              <span className="db-lv-value">{progress.level}</span>
            </div>
            <div className="db-level-progress">
              <div className="db-level-bar">
                <ProgressBar value={xpInCurrentLevel} max={xpToNextLevel} height={10} />
              </div>
              <div className="db-xp-info">
                <span>{xpInCurrentLevel} / {xpToNextLevel} XP to Lv.{progress.level + 1}</span>
                <span className="db-total-xp"><Zap size={12} fill="currentColor" /> {progress.totalXP} Total XP</span>
              </div>
            </div>
          </div>

          <div className="db-profile-stats">
            <div className="db-mini-stat">
              <Trophy size={16} color="var(--orange-primary)" />
              <span className="db-mini-val">{totalQuizzes}</span>
              <span className="db-mini-label">Quizzes</span>
            </div>
            <div className="db-mini-stat">
              <Flame size={16} color="var(--warning)" />
              <span className="db-mini-val">{streak?.current || 0}</span>
              <span className="db-mini-label">Streak</span>
            </div>
            <div className="db-mini-stat">
              <Star size={16} color="#A855F7" />
              <span className="db-mini-val">{unlockedAchievements.length}</span>
              <span className="db-mini-label">Badges</span>
            </div>
          </div>
        </div>

        {/* ── Level Progress Cards ── */}
        <div className="db-section animate-fadeInUp" style={{ animationDelay: '0.2s' }}>
          <h2 className="db-section-title"><Target size={18} /> Level Progress</h2>
          <div className="db-levels-grid">
            {levels.map((lvl) => {
              const lvlData = progress[lvl.id] || { bestScore: 0, attempts: 0, completed: 0 };
              return (
                <div key={lvl.id} className="db-level-card card" style={{ '--lc': lvl.color }}>
                  <div className="db-lc-header">
                    <span className="db-lc-emoji">{lvl.emoji}</span>
                    <div>
                      <div className="db-lc-title" style={{ color: lvl.color }}>{lvl.title}</div>
                      <div className="db-lc-subtitle">{lvl.subtitle}</div>
                    </div>
                    <div className="db-lc-attempts">{lvlData.attempts} attempts</div>
                  </div>
                  <div className="db-lc-stats">
                    <div className="db-lc-stat">
                      <span>Best Score</span>
                      <strong style={{ color: lvl.color }}>{lvlData.bestScore}%</strong>
                    </div>
                    <div className="db-lc-stat">
                      <span>Completed</span>
                      <strong>{lvlData.completed}</strong>
                    </div>
                    <div className="db-lc-stat">
                      <span>XP/Q</span>
                      <strong>{lvl.xpPerQuestion}</strong>
                    </div>
                  </div>
                  <ProgressBar value={lvlData.bestScore} max={100} label="Best Score" showPercent color={lvl.color} height={6} />
                  <button className="btn btn-sm" style={{ background: lvl.colorLight, color: lvl.color, border: `1px solid ${lvl.color}44`, marginTop: 'var(--space-sm)' }} onClick={() => navigate(`/quiz/${lvl.id}`)}>
                    {lvlData.attempts === 0 ? 'Start Quest' : 'Practice Again'}
                  </button>
                </div>
              );
            })}
          </div>
        </div>

        {/* ── Streak Info ── */}
        <div className="db-streak-section animate-fadeInUp" style={{ animationDelay: '0.3s' }}>
          <h2 className="db-section-title"><Flame size={18} /> Daily Streak</h2>
          <div className="db-streak-card card">
            <div className="db-streak-item">
              <div className="db-streak-flame">🔥</div>
              <div>
                <div className="db-streak-value">{streak?.current || 0}</div>
                <div className="db-streak-label">Current Streak</div>
              </div>
            </div>
            <div className="db-streak-divider" />
            <div className="db-streak-item">
              <div className="db-streak-flame">⭐</div>
              <div>
                <div className="db-streak-value">{streak?.best || 0}</div>
                <div className="db-streak-label">Best Streak</div>
              </div>
            </div>
            <div className="db-streak-divider" />
            <div className="db-streak-tip">
              {(streak?.current || 0) === 0
                ? "Complete a quiz today to start your streak! 🚀"
                : `Keep going! You're on a ${streak.current}-day streak!`}
            </div>
          </div>
        </div>

        {/* ── Achievements ── */}
        <div className="db-achievements animate-fadeInUp" style={{ animationDelay: '0.4s' }}>
          <h2 className="db-section-title"><Star size={18} /> Achievements</h2>
          <div className="achievements-grid">
            {achievements.map((a) => (
              <div key={a.id} className={`achievement-card card ${a.unlocked ? 'achievement-unlocked' : 'achievement-locked'}`}>
                <div className="achievement-icon">{a.icon}</div>
                <div className="achievement-info">
                  <div className="achievement-title">{a.title}</div>
                  <div className="achievement-desc">{a.desc}</div>
                </div>
                {a.unlocked && <CheckCircle size={16} className="achievement-check" />}
              </div>
            ))}
          </div>
        </div>
      </div>
    </main>
  );
};

export default Dashboard;
