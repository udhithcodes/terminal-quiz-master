import React from 'react';

const ProgressBar = ({ value = 0, max = 100, label, showPercent = false, height = 8, color }) => {
  const pct = Math.min(100, Math.max(0, (value / max) * 100));

  return (
    <div className="progress-wrapper" role="progressbar" aria-valuenow={value} aria-valuemin={0} aria-valuemax={max}>
      {(label || showPercent) && (
        <div className="progress-header" style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
          {label && <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', fontWeight: 500 }}>{label}</span>}
          {showPercent && <span style={{ fontSize: '0.85rem', color: 'var(--orange-primary)', fontWeight: 700 }}>{Math.round(pct)}%</span>}
        </div>
      )}
      <div className="progress-bar-track" style={{ height }}>
        <div
          className="progress-bar-fill"
          style={{
            width: `${pct}%`,
            background: color || 'linear-gradient(90deg, var(--orange-primary), var(--orange-bright))',
          }}
        />
      </div>
    </div>
  );
};

export default ProgressBar;
