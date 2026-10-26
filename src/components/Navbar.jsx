import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Sun, Moon, Menu, X, Zap } from 'lucide-react';
import './Navbar.css';

const Navbar = ({ theme, toggleTheme }) => {
  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  // Close mobile menu on route change
  useEffect(() => { setMobileOpen(false); }, [location.pathname]);

  const navLinks = [
    { label: 'Home', path: '/' },
    { label: 'Quizzes', path: '/#difficulties' },
    { label: 'Leaderboard', path: '/leaderboard' },
    { label: 'Dashboard', path: '/dashboard' },
    { label: 'About', path: '/#about' },
  ];

  const handleNavClick = (e, path) => {
    e.preventDefault();
    if (path.includes('#')) {
      const id = path.split('#')[1];
      if (location.pathname !== '/') {
        navigate('/');
        setTimeout(() => document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' }), 200);
      } else {
        document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
      }
    } else {
      navigate(path);
    }
    setMobileOpen(false);
  };

  return (
    <nav className={`navbar ${scrolled ? 'navbar-scrolled' : ''}`} role="navigation" aria-label="Main navigation">
      <div className="navbar-inner container">
        {/* Logo */}
        <a href="/" className="navbar-logo" onClick={(e) => handleNavClick(e, '/')}>
          <div className="logo-icon">
            <Zap size={18} fill="currentColor" />
          </div>
          <div className="logo-text">
            <span className="logo-name">TQM</span>
            <span className="logo-tag">Quiz Master</span>
          </div>
        </a>

        {/* Desktop Links */}
        <ul className="navbar-links" role="list">
          {navLinks.map((link) => (
            <li key={link.label}>
              <a
                href={link.path}
                className={`nav-link ${location.pathname === link.path ? 'nav-link-active' : ''}`}
                onClick={(e) => handleNavClick(e, link.path)}
              >
                {link.label}
              </a>
            </li>
          ))}
        </ul>

        {/* Right Controls */}
        <div className="navbar-actions">
          <button
            className="theme-toggle"
            onClick={toggleTheme}
            aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
            title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
          >
            {theme === 'light' ? <Moon size={18} /> : <Sun size={18} />}
          </button>

          <button
            id="navbar-start-quiz"
            className="btn btn-primary btn-sm navbar-cta"
            onClick={() => navigate('/quiz/basic')}
          >
            <Zap size={14} />
            Start Quiz
          </button>

          <button
            className="hamburger"
            onClick={() => setMobileOpen((v) => !v)}
            aria-label="Toggle mobile menu"
            aria-expanded={mobileOpen}
          >
            {mobileOpen ? <X size={22} /> : <Menu size={22} />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      <div className={`mobile-menu ${mobileOpen ? 'mobile-menu-open' : ''}`} aria-hidden={!mobileOpen}>
        <ul role="list">
          {navLinks.map((link) => (
            <li key={link.label}>
              <a href={link.path} className="mobile-nav-link" onClick={(e) => handleNavClick(e, link.path)}>
                {link.label}
              </a>
            </li>
          ))}
          <li>
            <button className="btn btn-primary w-full" onClick={() => { navigate('/quiz/basic'); setMobileOpen(false); }}>
              <Zap size={16} /> Start Quiz
            </button>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
