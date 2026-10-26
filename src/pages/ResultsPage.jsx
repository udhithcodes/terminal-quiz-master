import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Trophy, RotateCcw, Home, BookOpen, ChevronDown, ChevronUp, CheckCircle, XCircle, Zap, Clock, Target } from 'lucide-react';
import AnimeMascot from '../components/AnimeMascot';
import ProgressBar from '../components/ProgressBar';
import { getRank } from '../data/questions';
import './ResultsPage.css';

/* ─── Answer Review Card ─── */
const AnswerReviewCard = ({ answer, index }) => {
  const [expanded, setExpanded] = useState(false);
  const { correct, selected, question } = answer;
  const LABELS = ['A', 'B', 'C', 'D'];

  return (
    <div className={`review-card ${correct ? 'review-correct' : 'review-wrong'}`}>
      <div className="review-card-header" onClick={() => setExpanded((v) => !v)}>
        <div className="review-status-badge">
          {correct ? <CheckCircle size={16} /> : <XCircle size={16} />}
          <span>Q{index + 1}</span>
        </div>
        <div className="review-question-preview">{question.question.slice(0, 80)}{question.question.length > 80 ? '…' : ''}</div>
        <button className="review-toggle" aria-label={expanded ? 'Collapse' : 'Expand'}>
          {expanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
        </button>
      </div>

      {expanded && (
        <div className="review-card-body animate-fadeInUp">
          <p className="review-full-question">{question.question}</p>
          {question.code && (
            <div className="code-block review-code">{question.code}</div>
          )}
          <div className="review-options">
            {question.options.map((opt, i) => {
              const isCorrect = opt === question.answer;
              const isSelected = opt === selected;
              const cls = isCorrect ? 'review-opt-correct' : (isSelected && !isCorrect) ? 'review-opt-wrong' : '';
              return (
                <div key={opt} className={`review-option ${cls}`}>
                  <span className="review-opt-label">{LABELS[i]}</span>
                  <span>{opt}</span>
                  {isCorrect && <CheckCircle size={14} />}
                  {isSelected && !isCorrect && <XCircle size={14} />}
                </div>
              );
            })}
          </div>
          {!selected && <p className="review-no-answer">⏱️ Time ran out — no answer submitted</p>}
          <div className="review-explanation">
            <strong>💡 Explanation:</strong> {question.explanation}
          </div>
        </div>
      )}
    </div>
  );
};

/* ─── Confetti particle ─── */
const ConfettiParticle = ({ style }) => <div className="confetti-particle" style={style} />;

const ResultsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [showReview, setShowReview] = useState(false);
  const [animateDone, setAnimateDone] = useState(false);

  const state = location.state;

  useEffect(() => {
    if (!state) { navigate('/'); return; }
    const t = setTimeout(() => setAnimateDone(true), 400);
    return () => clearTimeout(t);
  }, [state, navigate]);

  if (!state) return null;

  const { level, levelConfig, score, total, timeTaken, xpEarned, answers, questions, progress } = state;
  const percentage = Math.round((score / total) * 100);
  const { rank, icon, color, bgColor } = getRank(percentage);

  const minutes = Math.floor(timeTaken / 60);
  const seconds = timeTaken % 60;
  const timeStr = minutes > 0 ? `${minutes}m ${seconds}s` : `${seconds}s`;

  const getPerformanceMessage = () => {
    if (percentage === 100) return "🏆 Absolute perfection! You are a true Coding Legend!";
    if (percentage >= 90) return "🌟 Outstanding! You've earned the title of Coding Legend!";
    if (percentage >= 70) return "⭐ Great work! You're a Skilled Coder on the rise!";
    if (percentage >= 40) return "🔥 Keep going! You're becoming a Rising Challenger!";
    return "📚 Every master was once a beginner. Keep practicing!";
  };

  const confettiColors = ['#FF7900', '#FF9F1C', '#22C55E', '#3B82F6', '#A855F7', '#F59E0B'];
  const showConfetti = percentage >= 70;

  return (
    <div className="results-page">
      {/* Confetti */}
      {showConfetti && (
        <div className="confetti-container" aria-hidden="true">
          {[...Array(40)].map((_, i) => (
            <ConfettiParticle
              key={i}
              style={{
                left: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 2}s`,
                animationDuration: `${2 + Math.random() * 2}s`,
                background: confettiColors[i % confettiColors.length],
                width: `${6 + Math.random() * 8}px`,
                height: `${6 + Math.random() * 8}px`,
                borderRadius: Math.random() > 0.5 ? '50%' : '2px',
              }}
            />
          ))}
        </div>
      )}

      <div className="container results-container">
        {/* ── Top: Rank & Score ── */}
        <div className="results-hero animate-fadeInUp">
          <div className="results-mascot-wrap">
            <AnimeMascot mode={percentage >= 70 ? 'celebrate' : 'hero'} size={200} animate />
          </div>

          <div className="results-score-section">
            {/* Rank badge */}
            <div className="rank-badge animate-bounceIn" style={{ background: bgColor, color }}>
              <span className="rank-icon">{icon}</span>
              <span className="rank-name">{rank}</span>
            </div>

            <h1 className="results-title">Quest Complete!</h1>
            <p className="results-message">{getPerformanceMessage()}</p>

            {/* Score display */}
            <div className="score-display animate-scaleIn">
              <div className="score-big">
                <span className="score-number">{percentage}</span>
                <span className="score-percent">%</span>
              </div>
              <p className="score-label">{score} / {total} correct</p>
            </div>

            {/* Progress bar for score */}
            <div style={{ width: '100%', maxWidth: '360px' }}>
              <ProgressBar value={animateDone ? percentage : 0} max={100} height={12} />
            </div>
          </div>
        </div>

        {/* ── Stats Grid ── */}
        <div className="results-stats-grid animate-fadeInUp" style={{ animationDelay: '0.2s' }}>
          {[
            { icon: <Trophy size={20} />, label: 'Score', value: `${score}/${total}`, color: 'var(--orange-primary)' },
            { icon: <Target size={20} />, label: 'Accuracy', value: `${percentage}%`, color: percentage >= 70 ? 'var(--success)' : 'var(--orange-primary)' },
            { icon: <Zap size={20} />, label: 'XP Earned', value: `+${xpEarned}`, color: 'var(--orange-bright)' },
            { icon: <Clock size={20} />, label: 'Time Taken', value: timeStr, color: 'var(--text-secondary)' },
          ].map((s) => (
            <div key={s.label} className="result-stat-card card">
              <span className="result-stat-icon" style={{ color: s.color }}>{s.icon}</span>
              <span className="result-stat-value" style={{ color: s.color }}>{s.value}</span>
              <span className="result-stat-label">{s.label}</span>
            </div>
          ))}
        </div>

        {/* ── Level info ── */}
        <div className="results-level-strip animate-fadeInUp" style={{ animationDelay: '0.3s' }}>
          <span className="results-level-emoji">{levelConfig?.emoji}</span>
          <span>{levelConfig?.title} Level</span>
          <span>·</span>
          <span>Total XP: <strong style={{ color: 'var(--orange-primary)' }}>{progress?.totalXP}</strong></span>
          <span>·</span>
          <span>Player Level: <strong style={{ color: 'var(--orange-primary)' }}>Lv.{progress?.level}</strong></span>
        </div>

        {/* ── Action Buttons ── */}
        <div className="results-actions animate-fadeInUp" style={{ animationDelay: '0.4s' }}>
          <button id="retry-quiz-btn" className="btn btn-primary btn-lg" onClick={() => navigate(`/quiz/${level}`)}>
            <RotateCcw size={18} />
            Retry Quiz
          </button>
          <button id="choose-level-btn" className="btn btn-ghost btn-lg" onClick={() => { navigate('/'); setTimeout(() => document.getElementById('difficulties')?.scrollIntoView({ behavior: 'smooth' }), 200); }}>
            <Target size={18} />
            Choose Level
          </button>
          <button id="review-answers-btn" className="btn btn-secondary btn-lg" onClick={() => setShowReview((v) => !v)}>
            <BookOpen size={18} />
            {showReview ? 'Hide Review' : 'Review Answers'}
          </button>
          <button id="go-home-btn" className="btn btn-secondary" onClick={() => navigate('/')}>
            <Home size={18} />
            Home
          </button>
        </div>

        {/* ── Answer Review Section ── */}
        {showReview && (
          <div className="answer-review-section animate-fadeInUp">
            <h2 className="review-section-title">
              <BookOpen size={20} />
              Answer Review
            </h2>
            <p className="review-section-subtitle">Click any question to see the full details and explanation.</p>
            <div className="review-list">
              {answers.map((ans, i) => (
                <AnswerReviewCard key={ans.questionId || i} answer={ans} index={i} />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResultsPage;
