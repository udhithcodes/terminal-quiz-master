import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowRight, ChevronDown, Sparkles, BookOpen, Trophy, Zap, Target, Star } from 'lucide-react';
import AnimeMascot from '../components/AnimeMascot';
import DifficultyCard from '../components/DifficultyCard';
import { getLevelConfig } from '../data/questions';
import { getProgress, getStreak } from '../utils/storage';
import './Home.css';

/* ─── Floating decorative element ─── */
const FloatBadge = ({ style, children, delay = 0 }) => (
  <div className="float-badge" style={{ ...style, animationDelay: `${delay}s` }}>
    {children}
  </div>
);

/* ─── Stat counter ─── */
const StatItem = ({ icon, value, label }) => (
  <div className="hero-stat">
    <span className="hero-stat-icon">{icon}</span>
    <span className="hero-stat-value">{value}</span>
    <span className="hero-stat-label">{label}</span>
  </div>
);

const Home = () => {
  const navigate = useNavigate();
  const levels = getLevelConfig();
  const [progress, setProgress] = useState(null);
  const [streak, setStreak] = useState(null);

  useEffect(() => {
    setProgress(getProgress());
    setStreak(getStreak());
  }, []);

  const scrollToDifficulty = () => {
    document.getElementById('difficulties')?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <main className="home">
      {/* ═══════════════════════════════════
          HERO SECTION
      ═══════════════════════════════════ */}
      <section className="hero-section" id="hero">
        {/* Background decorations */}
        <div className="hero-bg">
          <div className="hero-circle hero-circle-1" />
          <div className="hero-circle hero-circle-2" />
          <div className="hero-grid" />
          {/* Manga speed lines */}
          <svg className="manga-lines" viewBox="0 0 800 600" preserveAspectRatio="xMidYMid slice">
            {[...Array(18)].map((_, i) => (
              <line
                key={i}
                x1="400" y1="300"
                x2={400 + Math.cos((i / 18) * Math.PI * 2) * 900}
                y2={300 + Math.sin((i / 18) * Math.PI * 2) * 900}
                stroke="rgba(255,121,0,0.04)"
                strokeWidth="2"
              />
            ))}
          </svg>
        </div>

        <div className="container hero-container">
          {/* ── Left: Content ── */}
          <div className="hero-content animate-slideLeft">
            <div className="badge badge-orange hero-badge">
              <Sparkles size={12} />
              YOUR CODING JOURNEY STARTS HERE
            </div>

            <h1 className="hero-heading">
              Think Smart.<br />
              <span className="hero-heading-accent">Code Better.</span><br />
              Level Up!
            </h1>

            <p className="hero-subtext">
              Master Python programming through interactive quizzes, earn XP, unlock achievements,
              and rise through anime-inspired ranks — from Training Arc to Coding Legend.
            </p>

            <div className="hero-actions">
              <button id="hero-start-quest" className="btn btn-primary btn-lg" onClick={() => navigate('/quiz/basic')}>
                <Zap size={18} />
                Start Your Quest
              </button>
              <button id="hero-explore-levels" className="btn btn-secondary btn-lg" onClick={scrollToDifficulty}>
                Explore Levels
                <ChevronDown size={18} />
              </button>
            </div>

            {/* Mini stats */}
            <div className="hero-stats">
              <StatItem icon={<BookOpen size={16} />} value="30+" label="Questions" />
              <div className="hero-stat-divider" />
              <StatItem icon={<Target size={16} />} value="3" label="Difficulty Levels" />
              <div className="hero-stat-divider" />
              <StatItem icon={<Trophy size={16} />} value="4" label="Anime Ranks" />
              {streak?.current > 0 && (
                <>
                  <div className="hero-stat-divider" />
                  <StatItem icon={<Star size={16} />} value={`${streak.current}🔥`} label="Day Streak" />
                </>
              )}
            </div>
          </div>

          {/* ── Right: Mascot + UI Elements ── */}
          <div className="hero-visual animate-slideRight">
            {/* Floating XP badge */}
            <FloatBadge style={{ top: '8%', right: '5%' }} delay={0}>
              <div className="xp-badge">
                <Zap size={14} fill="currentColor" />
                <span>+30 XP</span>
              </div>
            </FloatBadge>

            {/* Floating Level badge */}
            <FloatBadge style={{ bottom: '22%', left: '0%' }} delay={1.2}>
              <div className="level-badge">
                <span className="level-badge-number">Lv.{progress?.level || 1}</span>
                <span className="level-badge-label">Your Level</span>
              </div>
            </FloatBadge>

            {/* Floating Code snippet */}
            <FloatBadge style={{ top: '28%', left: '-5%' }} delay={0.6}>
              <div className="code-snippet-badge">
                <span style={{ color: '#FF79C6' }}>def</span>{' '}
                <span style={{ color: '#50FA7B' }}>level_up</span>
                <span style={{ color: '#F8F8F2' }}>():</span>
              </div>
            </FloatBadge>

            {/* Streak badge */}
            {streak?.current > 0 && (
              <FloatBadge style={{ top: '15%', left: '5%' }} delay={1.8}>
                <div className="streak-badge">🔥 {streak.current}-day streak!</div>
              </FloatBadge>
            )}

            {/* Glow ring */}
            <div className="mascot-glow-ring" />

            <AnimeMascot mode="hero" size={320} animate />
          </div>
        </div>

        {/* Scroll indicator */}
        <button className="scroll-indicator" onClick={scrollToDifficulty} aria-label="Scroll to difficulty selection">
          <ChevronDown size={22} />
        </button>
      </section>

      {/* ═══════════════════════════════════
          DIFFICULTY SELECTION
      ═══════════════════════════════════ */}
      <section className="difficulties-section section" id="difficulties">
        <div className="container">
          <div className="section-header text-center">
            <div className="badge badge-orange" style={{ marginBottom: '1rem' }}>
              <Target size={12} />
              CHOOSE YOUR PATH
            </div>
            <h2 className="section-title">Select Your Difficulty</h2>
            <p className="section-subtitle">
              Start at your level and work your way to becoming a Coding Legend
            </p>
          </div>

          <div className="difficulty-grid">
            {levels.map((level, i) => (
              <DifficultyCard key={level.id} config={level} progress={progress} index={i} />
            ))}
          </div>
        </div>
      </section>

      {/* ═══════════════════════════════════
          FEATURES / HOW IT WORKS
      ═══════════════════════════════════ */}
      <section className="features-section section" id="how-it-works">
        <div className="container">
          <div className="text-center" style={{ marginBottom: 'var(--space-2xl)' }}>
            <div className="badge badge-orange" style={{ marginBottom: '1rem' }}>
              <Sparkles size={12} />
              HOW IT WORKS
            </div>
            <h2 className="section-title">Your Quest Awaits</h2>
          </div>
          <div className="features-grid">
            {[
              { step: '01', icon: '🎯', title: 'Choose Your Level', desc: 'Pick from Basic, Intermediate, or Advanced difficulty based on your Python experience.' },
              { step: '02', icon: '🧠', title: 'Answer Questions', desc: 'Tackle 10 carefully crafted Python questions with instant feedback and explanations.' },
              { step: '03', icon: '⭐', title: 'Earn XP & Rank Up', desc: 'Every correct answer earns you XP. Level up and climb the anime-inspired rank ladder.' },
              { step: '04', icon: '📊', title: 'Track Progress', desc: 'Your scores, streaks, and achievements are saved locally so you can improve over time.' },
            ].map((f) => (
              <div key={f.step} className="feature-card card">
                <div className="feature-step">{f.step}</div>
                <div className="feature-icon">{f.icon}</div>
                <h3 className="feature-title">{f.title}</h3>
                <p className="feature-desc">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ═══════════════════════════════════
          CTA BANNER
      ═══════════════════════════════════ */}
      <section className="cta-section section">
        <div className="container">
          <div className="cta-banner">
            <div className="cta-bg-glow" />
            <div className="cta-content">
              <h2 className="cta-title">Ready to Become a Coding Legend?</h2>
              <p className="cta-subtitle">Your first quest is just one click away. No signup required.</p>
              <div className="hero-actions">
                <button id="cta-start-now" className="btn btn-primary btn-lg" onClick={() => navigate('/quiz/basic')}>
                  <Zap size={18} />
                  Start Now — It's Free
                </button>
                <button className="btn" style={{ color: 'rgba(255,255,255,0.8)', border: '2px solid rgba(255,255,255,0.3)' }} onClick={() => navigate('/leaderboard')}>
                  <Trophy size={16} />
                  View Leaderboard
                </button>
              </div>
            </div>
            <div className="cta-mascot">
              <AnimeMascot mode="celebrate" size={180} animate={false} />
            </div>
          </div>
        </div>
      </section>
    </main>
  );
};

export default Home;
