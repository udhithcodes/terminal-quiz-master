import React from 'react';
import './AnimeMascot.css';

/**
 * Anime-style programmer mascot SVG component.
 * Modes: 'hero' | 'correct' | 'wrong' | 'thinking' | 'celebrate'
 */
const AnimeMascot = ({ mode = 'hero', size = 260, animate = true }) => {
  const getMoodColor = () => {
    switch (mode) {
      case 'correct': return '#22C55E';
      case 'wrong': return '#EF4444';
      case 'celebrate': return '#FF7900';
      default: return '#FF9F1C';
    }
  };

  const moodColor = getMoodColor();

  return (
    <div
      className={`mascot-container ${animate ? 'mascot-float' : ''} mascot-${mode}`}
      style={{ width: size, height: size }}
      aria-label={`Mascot in ${mode} mode`}
      role="img"
    >
      {/* Glow aura */}
      <div className="mascot-aura" style={{ background: `radial-gradient(circle, ${moodColor}33 0%, transparent 70%)` }} />

      <svg
        viewBox="0 0 260 280"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="mascot-svg"
      >
        {/* ── Shadow ── */}
        <ellipse cx="130" cy="268" rx="55" ry="9" fill="rgba(0,0,0,0.08)" />

        {/* ── Body / Hoodie ── */}
        <path
          d="M65 180 Q60 220 58 255 L202 255 Q200 220 195 180 Q175 168 145 165 L130 175 L115 165 Q85 168 65 180Z"
          fill="#FF7900"
        />
        {/* Hoodie pocket */}
        <rect x="105" y="210" width="50" height="30" rx="8" fill="rgba(0,0,0,0.12)" />
        {/* Hoodie string */}
        <path d="M122 185 Q125 205 124 215" stroke="rgba(255,255,255,0.4)" strokeWidth="2" strokeLinecap="round" />
        <path d="M138 185 Q135 205 136 215" stroke="rgba(255,255,255,0.4)" strokeWidth="2" strokeLinecap="round" />

        {/* ── Laptop ── */}
        <rect x="68" y="230" width="124" height="8" rx="4" fill="#2A2A3E" />
        <rect x="75" y="195" width="110" height="70" rx="6" fill="#1E1E2E" />
        <rect x="79" y="199" width="102" height="62" rx="4" fill="#252540" />
        {/* Code on screen */}
        <rect x="85" y="206" width="45" height="3" rx="2" fill="#FF7900" opacity="0.8" />
        <rect x="85" y="212" width="70" height="3" rx="2" fill="#50FA7B" opacity="0.7" />
        <rect x="85" y="218" width="55" height="3" rx="2" fill="#8BE9FD" opacity="0.7" />
        <rect x="85" y="224" width="38" height="3" rx="2" fill="#FF79C6" opacity="0.7" />
        <rect x="85" y="230" width="60" height="3" rx="2" fill="#F1FA8C" opacity="0.7" />
        {/* Cursor blink */}
        <rect x="85" y="236" width="6" height="10" rx="1" fill="#FF7900" className="mascot-cursor" />

        {/* ── Neck ── */}
        <rect x="116" y="158" width="28" height="20" rx="6" fill="#FDDCB5" />

        {/* ── Head ── */}
        <ellipse cx="130" cy="125" rx="50" ry="52" fill="#FDDCB5" />

        {/* ── Hair ── */}
        <path
          d="M82 118 Q80 85 100 70 Q118 58 130 60 Q148 58 158 68 Q172 82 175 105 Q178 120 175 118 Q165 90 148 80 Q135 73 122 76 Q102 82 92 100 Q87 112 90 118Z"
          fill="#242424"
        />
        {/* Wild hair spikes */}
        <path d="M82 108 Q70 95 78 78 Q82 90 88 100Z" fill="#242424" />
        <path d="M175 105 Q188 90 180 75 Q176 88 170 100Z" fill="#242424" />
        <path d="M110 62 Q112 45 125 42 Q118 52 115 65Z" fill="#242424" />
        <path d="M148 62 Q150 44 138 42 Q142 52 145 65Z" fill="#242424" />

        {/* ── Headphones ── */}
        {/* Band */}
        <path d="M88 118 Q88 72 130 68 Q172 72 172 118" stroke="#1A1A2E" strokeWidth="9" fill="none" strokeLinecap="round" />
        {/* Left ear cup */}
        <ellipse cx="88" cy="120" rx="13" ry="16" fill="#FF7900" />
        <ellipse cx="88" cy="120" rx="8" ry="10" fill="#E05A00" />
        {/* Right ear cup */}
        <ellipse cx="172" cy="120" rx="13" ry="16" fill="#FF7900" />
        <ellipse cx="172" cy="120" rx="8" ry="10" fill="#E05A00" />

        {/* ── Eyes ── */}
        {mode === 'correct' ? (
          <>
            {/* Happy curved eyes */}
            <path d="M108 122 Q115 115 122 122" stroke="#242424" strokeWidth="3" fill="none" strokeLinecap="round" />
            <path d="M138 122 Q145 115 152 122" stroke="#242424" strokeWidth="3" fill="none" strokeLinecap="round" />
          </>
        ) : mode === 'wrong' ? (
          <>
            {/* Worried eyes */}
            <ellipse cx="115" cy="123" rx="9" ry="10" fill="#242424" />
            <ellipse cx="145" cy="123" rx="9" ry="10" fill="#242424" />
            <ellipse cx="117" cy="121" rx="3" ry="3" fill="white" />
            <ellipse cx="147" cy="121" rx="3" ry="3" fill="white" />
            {/* Sweat drop */}
            <path d="M158 110 Q162 118 159 122 Q155 118 158 110Z" fill="#6EC6FF" opacity="0.8" />
          </>
        ) : mode === 'celebrate' ? (
          <>
            {/* Star eyes */}
            <text x="106" y="130" fontSize="16" fill={moodColor}>★</text>
            <text x="136" y="130" fontSize="16" fill={moodColor}>★</text>
          </>
        ) : (
          <>
            {/* Normal focused eyes */}
            <ellipse cx="115" cy="123" rx="10" ry="11" fill="#242424" />
            <ellipse cx="145" cy="123" rx="10" ry="11" fill="#242424" />
            <ellipse cx="118" cy="120" rx="4" ry="4" fill="white" />
            <ellipse cx="148" cy="120" rx="4" ry="4" fill="white" />
            <ellipse cx="120" cy="119" rx="2" ry="2" fill="white" opacity="0.9" />
            <ellipse cx="150" cy="119" rx="2" ry="2" fill="white" opacity="0.9" />
          </>
        )}

        {/* ── Blush cheeks ── */}
        <ellipse cx="104" cy="134" rx="10" ry="6" fill="rgba(255,121,0,0.25)" />
        <ellipse cx="156" cy="134" rx="10" ry="6" fill="rgba(255,121,0,0.25)" />

        {/* ── Mouth ── */}
        {mode === 'correct' || mode === 'celebrate' ? (
          <path d="M118 142 Q130 152 142 142" stroke="#242424" strokeWidth="2.5" fill="none" strokeLinecap="round" />
        ) : mode === 'wrong' ? (
          <path d="M120 148 Q130 142 140 148" stroke="#242424" strokeWidth="2.5" fill="none" strokeLinecap="round" />
        ) : (
          <path d="M120 143 Q130 148 140 143" stroke="#242424" strokeWidth="2" fill="none" strokeLinecap="round" />
        )}

        {/* ── Glasses (hero/thinking mode) ── */}
        {(mode === 'hero' || mode === 'thinking') && (
          <>
            <rect x="100" y="113" width="26" height="19" rx="6" stroke="#E05A00" strokeWidth="2.5" fill="rgba(255,121,0,0.08)" />
            <rect x="134" y="113" width="26" height="19" rx="6" stroke="#E05A00" strokeWidth="2.5" fill="rgba(255,121,0,0.08)" />
            <line x1="126" y1="122" x2="134" y2="122" stroke="#E05A00" strokeWidth="2.5" />
          </>
        )}

        {/* ── XP Badge (celebrate) ── */}
        {mode === 'celebrate' && (
          <>
            <circle cx="190" cy="90" r="20" fill="#FF7900" />
            <text x="190" y="96" textAnchor="middle" fill="white" fontSize="10" fontWeight="bold" fontFamily="sans-serif">+XP</text>
          </>
        )}

        {/* ── Floating stars (correct) ── */}
        {mode === 'correct' && (
          <>
            <text x="60" y="90" fontSize="14" fill="#22C55E" className="star-float-1">✦</text>
            <text x="195" y="85" fontSize="18" fill="#22C55E" className="star-float-2">✦</text>
            <text x="175" y="110" fontSize="10" fill="#22C55E" className="star-float-3">✦</text>
          </>
        )}
      </svg>

      {/* Mode label */}
      {mode === 'correct' && <div className="mascot-label mascot-label-correct">+XP ✓</div>}
      {mode === 'wrong' && <div className="mascot-label mascot-label-wrong">Try again!</div>}
      {mode === 'celebrate' && <div className="mascot-label mascot-label-celebrate">Legend! 🏆</div>}
    </div>
  );
};

export default AnimeMascot;
