import React from 'react';
import { Trophy, Star, Flame, Zap } from 'lucide-react';
import { DEMO_LEADERBOARD } from '../data/questions';
import './Leaderboard.css';

const medalColors = ['#FFD700', '#C0C0C0', '#CD7F32'];
const medalEmoji = ['🥇', '🥈', '🥉'];

const Leaderboard = () => {
  const topThree = DEMO_LEADERBOARD.slice(0, 3);
  const rest = DEMO_LEADERBOARD.slice(3);

  return (
    <main className="leaderboard-page">
      <div className="lb-bg">
        <div className="lb-bg-circle" />
      </div>
      <div className="container lb-container">
        {/* Header */}
        <div className="lb-header text-center animate-fadeInUp">
          <div className="badge badge-orange" style={{ marginBottom: '1rem' }}>
            <Trophy size={12} />
            HALL OF LEGENDS
          </div>
          <h1 className="section-title">Leaderboard</h1>
          <p className="section-subtitle">Top Python warriors ranked by XP — Demo data for illustration</p>
          <div className="lb-demo-notice">
            ℹ️ This leaderboard uses sample data and does not represent real users.
          </div>
        </div>

        {/* Podium */}
        <div className="podium-section animate-fadeInUp" style={{ animationDelay: '0.1s' }}>
          {/* Reorder: 2nd, 1st, 3rd */}
          {[topThree[1], topThree[0], topThree[2]].filter(Boolean).map((player, podiumIdx) => {
            const actualRank = podiumIdx === 0 ? 2 : podiumIdx === 1 ? 1 : 3;
            const heights = ['180px', '230px', '160px'];
            return (
              <div key={player.id} className={`podium-item podium-rank-${actualRank}`} style={{ height: heights[podiumIdx] }}>
                <div className="podium-avatar">{player.avatar}</div>
                <div className="podium-name">{player.name}</div>
                <div className="podium-xp"><Zap size={12} fill="currentColor" />{player.xp.toLocaleString()} XP</div>
                <div className="podium-medal">{medalEmoji[actualRank - 1]}</div>
                <div className="podium-rank-num">{actualRank}</div>
              </div>
            );
          })}
        </div>

        {/* Full Table */}
        <div className="lb-table animate-fadeInUp" style={{ animationDelay: '0.2s' }}>
          <div className="lb-table-header">
            <span>Rank</span>
            <span>Player</span>
            <span>XP</span>
            <span>Quizzes</span>
            <span>Streak</span>
          </div>
          {DEMO_LEADERBOARD.map((player, i) => (
            <div key={player.id} className={`lb-row ${i < 3 ? 'lb-row-top' : ''}`}>
              <div className="lb-rank">
                {i < 3 ? (
                  <span className="lb-medal" style={{ color: medalColors[i] }}>{medalEmoji[i]}</span>
                ) : (
                  <span className="lb-rank-num">#{player.rank}</span>
                )}
              </div>
              <div className="lb-player">
                <div className="lb-avatar">{player.avatar}</div>
                <span className="lb-name">{player.name}</span>
              </div>
              <div className="lb-xp">
                <Zap size={12} fill="var(--orange-primary)" color="var(--orange-primary)" />
                <span>{player.xp.toLocaleString()}</span>
              </div>
              <div className="lb-quizzes">
                <Trophy size={12} color="var(--text-muted)" />
                <span>{player.quizzes}</span>
              </div>
              <div className="lb-streak">
                <Flame size={12} color="var(--warning)" />
                <span>{player.streak}d</span>
              </div>
            </div>
          ))}
        </div>

        {/* Rank Guide */}
        <div className="rank-guide animate-fadeInUp" style={{ animationDelay: '0.3s' }}>
          <h3 className="rank-guide-title"><Star size={18} /> Anime Ranks</h3>
          <div className="rank-guide-grid">
            {[
              { icon: '📚', rank: 'Training Arc', range: '0–39%', color: '#777' },
              { icon: '🔥', rank: 'Rising Challenger', range: '40–69%', color: '#F59E0B' },
              { icon: '⭐', rank: 'Skilled Coder', range: '70–89%', color: '#22C55E' },
              { icon: '🏆', rank: 'Coding Legend', range: '90–100%', color: '#FF7900' },
            ].map((r) => (
              <div key={r.rank} className="rank-item" style={{ borderColor: r.color + '44', background: r.color + '11' }}>
                <span className="rank-item-icon">{r.icon}</span>
                <div>
                  <div className="rank-item-name" style={{ color: r.color }}>{r.rank}</div>
                  <div className="rank-item-range">{r.range} score</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </main>
  );
};

export default Leaderboard;
