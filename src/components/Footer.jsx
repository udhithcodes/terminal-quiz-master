import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Zap, Github, Heart, Code2, BookOpen, Trophy, LayoutDashboard } from 'lucide-react';
import './Footer.css';

const Footer = () => {
  const navigate = useNavigate();
  const year = new Date().getFullYear();

  const links = [
    { section: 'Navigate', items: [
      { label: 'Home', action: () => navigate('/') },
      { label: 'Quizzes', action: () => { navigate('/'); setTimeout(() => document.getElementById('difficulties')?.scrollIntoView({ behavior: 'smooth' }), 200); } },
      { label: 'Leaderboard', action: () => navigate('/leaderboard') },
      { label: 'Dashboard', action: () => navigate('/dashboard') },
    ]},
    { section: 'Difficulty', items: [
      { label: '🌱 Basic Quest', action: () => navigate('/quiz/basic') },
      { label: '🔥 Intermediate Quest', action: () => navigate('/quiz/intermediate') },
      { label: '👑 Advanced Quest', action: () => navigate('/quiz/advanced') },
    ]},
    { section: 'Built With', items: [
      { label: 'React.js', icon: <Code2 size={12} /> },
      { label: 'Vite', icon: <Zap size={12} /> },
      { label: 'Lucide Icons', icon: <Heart size={12} /> },
      { label: 'CSS3 Animations', icon: <BookOpen size={12} /> },
    ]},
  ];

  return (
    <footer className="footer" id="about">
      <div className="footer-glow" />
      <div className="container">
        <div className="footer-top">
          {/* Brand */}
          <div className="footer-brand">
            <div className="footer-logo">
              <div className="footer-logo-icon"><Zap size={20} fill="currentColor" /></div>
              <div>
                <div className="footer-logo-name">Terminal Quiz Master</div>
                <div className="footer-logo-tag">Level Up Your Brain. Become a Coding Legend.</div>
              </div>
            </div>
            <p className="footer-description">
              An interactive anime-inspired coding quiz platform designed to help you master Python programming
              through gamified learning. Track your progress, earn XP, and rise through the ranks.
            </p>
            <div className="footer-stats">
              <div className="footer-stat"><Trophy size={14} /><span>30 Questions</span></div>
              <div className="footer-stat"><BookOpen size={14} /><span>3 Levels</span></div>
              <div className="footer-stat"><LayoutDashboard size={14} /><span>Progress Tracking</span></div>
            </div>
          </div>

          {/* Links */}
          {links.map((section) => (
            <div key={section.section} className="footer-section">
              <h4 className="footer-section-title">{section.section}</h4>
              <ul>
                {section.items.map((item) => (
                  <li key={item.label}>
                    {item.action ? (
                      <button className="footer-link" onClick={item.action}>
                        {item.icon && item.icon}
                        {item.label}
                      </button>
                    ) : (
                      <span className="footer-link-static">
                        {item.icon && item.icon}
                        {item.label}
                      </span>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="footer-bottom">
          <p>© {year} Terminal Quiz Master. Built with <Heart size={13} className="heart" /> for learners everywhere.</p>
          <p className="footer-disclaimer">
            This is a demo project. Leaderboard scores are sample data and do not represent real users.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
