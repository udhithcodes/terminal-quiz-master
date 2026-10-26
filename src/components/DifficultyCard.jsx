import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowRight, Clock, HelpCircle, CheckCircle } from 'lucide-react';
import ProgressBar from './ProgressBar';
import './DifficultyCard.css';

const DifficultyCard = ({ config, progress, index }) => {
  const navigate = useNavigate();
  const { id, title, subtitle, emoji, color, colorLight, colorBorder, difficulty, description, topics, totalQuestions, estimatedTime, buttonLabel, xpPerQuestion } = config;

  const levelProgress = progress?.[id] || { bestScore: 0, attempts: 0, completed: 0 };
  const bestPct = levelProgress.bestScore || 0;

  const difficultyStars = id === 'basic' ? 1 : id === 'intermediate' ? 2 : 3;

  return (
    <div
      className={`difficulty-card animate-fadeInUp`}
      style={{
        '--card-color': color,
        '--card-color-light': colorLight,
        '--card-color-border': colorBorder,
        animationDelay: `${index * 0.12}s`,
      }}
      id={`difficulty-card-${id}`}
    >
      {/* Card glow */}
      <div className="card-glow" />

      {/* Header */}
      <div className="difficulty-card-header">
        <div className="difficulty-emoji-wrapper">
          <span className="difficulty-emoji">{emoji}</span>
        </div>
        <div className="difficulty-meta">
          <span className="difficulty-label">
            {'⭐'.repeat(difficultyStars)}{'☆'.repeat(3 - difficultyStars)}
          </span>
          <span className="difficulty-badge" style={{ color, background: colorLight, borderColor: colorBorder }}>
            {difficulty}
          </span>
        </div>
      </div>

      {/* Titles */}
      <div className="difficulty-card-titles">
        <h3 className="difficulty-title" style={{ color }}>{title}</h3>
        <span className="difficulty-subtitle">{subtitle}</span>
      </div>

      <p className="difficulty-description">{description}</p>

      {/* Stats Row */}
      <div className="difficulty-stats">
        <div className="diff-stat">
          <HelpCircle size={14} />
          <span>{totalQuestions} Questions</span>
        </div>
        <div className="diff-stat">
          <Clock size={14} />
          <span>{estimatedTime}</span>
        </div>
        <div className="diff-stat">
          <CheckCircle size={14} />
          <span>{xpPerQuestion} XP/Q</span>
        </div>
      </div>

      {/* Topics */}
      <div className="difficulty-topics">
        {topics.map((t) => (
          <span key={t} className="topic-chip" style={{ background: colorLight, borderColor: colorBorder, color }}>
            {t}
          </span>
        ))}
      </div>

      {/* Progress (if attempted) */}
      {levelProgress.attempts > 0 && (
        <div className="difficulty-progress">
          <ProgressBar value={bestPct} max={100} label={`Best: ${bestPct}%`} showPercent color={color} height={6} />
          <span className="attempts-badge">{levelProgress.attempts} attempt{levelProgress.attempts > 1 ? 's' : ''}</span>
        </div>
      )}

      {/* CTA Button */}
      <button
        id={`start-${id}-quiz`}
        className="difficulty-cta"
        style={{ background: `linear-gradient(135deg, ${color}, ${color}CC)`, boxShadow: `0 6px 20px ${colorBorder}` }}
        onClick={() => navigate(`/quiz/${id}`)}
      >
        {buttonLabel}
        <ArrowRight size={16} />
      </button>
    </div>
  );
};

export default DifficultyCard;
