import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
import QuizPage from './pages/QuizPage';
import ResultsPage from './pages/ResultsPage';
import Leaderboard from './pages/Leaderboard';
import Dashboard from './pages/Dashboard';
import { getTheme, saveTheme } from './utils/storage';

// Scroll to top on route change
const ScrollToTop = () => {
  const { pathname } = useLocation();
  useEffect(() => { window.scrollTo(0, 0); }, [pathname]);
  return null;
};

// Pages where footer should not show
const NO_FOOTER_ROUTES = ['/quiz/'];

const AppContent = () => {
  const location = useLocation();
  const showFooter = !NO_FOOTER_ROUTES.some((r) => location.pathname.startsWith(r));

  const [theme, setTheme] = useState(() => getTheme());

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    saveTheme(theme);
  }, [theme]);

  const toggleTheme = () => setTheme((t) => (t === 'light' ? 'dark' : 'light'));

  return (
    <>
      <ScrollToTop />
      <Navbar theme={theme} toggleTheme={toggleTheme} />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/quiz/:level" element={<QuizPage />} />
        <Route path="/results" element={<ResultsPage />} />
        <Route path="/leaderboard" element={<Leaderboard />} />
        <Route path="/dashboard" element={<Dashboard />} />
        {/* Fallback */}
        <Route path="*" element={<Home />} />
      </Routes>
      {showFooter && <Footer />}
    </>
  );
};

const App = () => (
  <BrowserRouter>
    <AppContent />
  </BrowserRouter>
);

export default App;
