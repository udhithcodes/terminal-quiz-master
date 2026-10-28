import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Clock, Zap, X, ChevronRight, CheckCircle, XCircle, ArrowLeft, BookOpen } from 'lucide-react';
import AnimeMascot from '../components/AnimeMascot';
import ProgressBar from '../components/ProgressBar';
import { getQuestionsByLevel, getLevelConfig } from '../data/questions';
import { saveQuizResult, updateHighScore } from '../utils/storage';
import './QuizPage.css';

import api from '../services/api';

/* ─── Code block renderer ─── */
const CodeBlock = ({ code }) => {
  if (!code) return null;
  // Simple syntax highlighting
  const highlighted = code
    .replace(/(def |class |return |import |from |if |else:|elif |for |in |while |try:|except |finally:|with |as |lambda |yield |print|True|False|None)/g,
      (m) => `<span class="code-keyword">${m}</span>`)
    .replace(/(".*?"|'.*?')/g, (m) => `<span class="code-string">${m}</span>`)
    .replace(/(#.*)/g, (m) => `<span class="code-comment">${m}</span>`)
    .replace(/\b(\d+)\b/g, (m) => `<span class="code-number">${m}</span>`);

  return (
    <div className="code-block quiz-code-block" dangerouslySetInnerHTML={{ __html: highlighted }} />
  );
};

/* ─── Single Answer Option ─── */
const AnswerOption = ({ option, label, state, onClick, disabled }) => {
  const stateClass = state === 'correct' ? 'option-correct' : state === 'wrong' ? 'option-wrong' : state === 'selected' ? 'option-selected' : '';
  return (
    <button
      className={`answer-option ${stateClass}`}
      onClick={onClick}
      disabled={disabled}
      aria-pressed={state === 'selected' || state === 'correct' || state === 'wrong'}
      id={`answer-option-${label.toLowerCase()}`}
    >
      <span className="option-label">{label}</span>
      <span className="option-text">{option}</span>
      {state === 'correct' && <CheckCircle size={18} className="option-icon-right" />}
      {state === 'wrong' && <XCircle size={18} className="option-icon-wrong" />}
    </button>
  );
};

/* ─── Timer ─── */
const useTimer = (seconds, onExpire, active) => {
  const [remaining, setRemaining] = useState(seconds);
  useEffect(() => {
    if (!active) return;
    setRemaining(seconds);
  }, [seconds, active]);

  useEffect(() => {
    if (!active) return;
    if (remaining <= 0) { onExpire(); return; }
    const t = setTimeout(() => setRemaining((r) => r - 1), 1000);
    return () => clearTimeout(t);
  }, [remaining, active, onExpire]);

  return remaining;
};

const LABELS = ['A', 'B', 'C', 'D'];
const TIMER_SECONDS = 30;

const QuizPage = () => {
  const { level } = useParams();
  const navigate = useNavigate();
  const [quizId, setQuizId] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [levelConfig, setLevelConfig] = useState(null);
  const [currentIdx, setCurrentIdx] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [submitted, setSubmitted] = useState(false);
  const [score, setScore] = useState(0);
  const [answers, setAnswers] = useState([]); // track each answer for review
  const [mascotMode, setMascotMode] = useState('hero');
  const [timerActive, setTimerActive] = useState(true);
  const [timeTaken, setTimeTaken] = useState(0); // total seconds elapsed
  const [quizStartTime] = useState(Date.now());
  const [showExplanation, setShowExplanation] = useState(false);

  useEffect(() => {
    const configs = getLevelConfig();
    const cfg = configs.find((c) => c.id === level);
    if (!cfg) {
      navigate('/');
      return;
    }
    setLevelConfig(cfg);

    let isMounted = true;
    // Attempt backend quiz creation
    api.startQuiz(level, 10)
      .then((session) => {
        if (!isMounted) return;
        if (session && session.questions && session.questions.length > 0) {
          setQuizId(session.id);
          setQuestions(session.questions);
        } else {
          loadFallback();
        }
      })
      .catch((err) => {
        console.warn('Backend unavailable, running in local mode:', err);
        if (isMounted) loadFallback();
      });

    const loadFallback = () => {
      const qs = getQuestionsByLevel(level);
      if (!qs.length) {
        navigate('/');
        return;
      }
      const shuffled = [...qs].sort(() => Math.random() - 0.5).slice(0, 10);
      setQuestions(shuffled);
    };

    return () => { isMounted = false; };
  }, [level, navigate]);

  const handleTimerExpire = useCallback(() => {
    if (submitted) return;
    setTimerActive(false);
    setSubmitted(true);
    setMascotMode('wrong');
    setAnswers((prev) => [...prev, {
      questionId: questions[currentIdx].id,
      selected: null,
      correct: false,
      question: questions[currentIdx],
    }]);
  }, [submitted, currentIdx, questions]);

  const timeLeft = useTimer(TIMER_SECONDS, handleTimerExpire, timerActive && !submitted && questions.length > 0);
  const timerPct = (timeLeft / TIMER_SECONDS) * 100;

  const currentQ = questions[currentIdx];
  const isLastQuestion = currentIdx === questions.length - 1;

  const handleSelectAnswer = (opt) => {
    if (submitted) return;
    setSelectedAnswer(opt);
  };

  const applySubmissionResult = (isCorrect, correctAnswerText, explanationText) => {
    if (isCorrect) {
      setScore((s) => s + 1);
      setMascotMode('correct');
    } else {
      setMascotMode('wrong');
    }

    setAnswers((prev) => [
      ...prev,
      {
        questionId: currentQ.id,
        selected: selectedAnswer,
        correct: isCorrect,
        question: {
          ...currentQ,
          answer: correctAnswerText || currentQ.answer,
          explanation: explanationText || currentQ.explanation,
        },
      },
    ]);
    setShowExplanation(true);
  };

  const handleSubmit = async () => {
    if (!submitted && !selectedAnswer) return;
    if (submitted) return;

    setTimerActive(false);
    setSubmitted(true);

    if (quizId) {
      try {
        const result = await api.submitAnswer(quizId, currentQ.id, selectedAnswer);
        applySubmissionResult(result.is_correct, result.correct_answer, result.explanation);
        return;
      } catch (err) {
        console.warn('Backend submit failed, falling back to local evaluation:', err);
      }
    }

    // Local evaluation fallback
    const isCorrect = selectedAnswer === currentQ.answer;
    applySubmissionResult(isCorrect, currentQ.answer, currentQ.explanation);
  };

  const handleNext = async () => {
    if (isLastQuestion) {
      const totalSeconds = Math.round((Date.now() - quizStartTime) / 1000);
      const xpEarned = score * (levelConfig?.xpPerQuestion || 10);

      // Finalize on backend if quizId is active
      if (quizId) {
        api.completeQuiz(quizId).catch((err) => console.warn('Complete quiz backend sync:', err));
      }

      const savedProgress = saveQuizResult({
        level,
        score,
        total: questions.length,
        xpEarned,
      });
      updateHighScore(level, Math.round((score / questions.length) * 100));

      navigate('/results', {
        state: {
          level,
          levelConfig,
          score,
          total: questions.length,
          timeTaken: totalSeconds,
          xpEarned,
          answers,
          questions,
          progress: savedProgress,
        },
      });
    } else {
      setCurrentIdx((i) => i + 1);
      setSelectedAnswer(null);
      setSubmitted(false);
      setMascotMode('hero');
      setShowExplanation(false);
      setTimerActive(true);
    }
  };

  if (!currentQ || !levelConfig) {
    return (
      <div className="quiz-loading">
        <div className="loading-spinner" />
        <p>Loading your quest...</p>
      </div>
    );
  }

  const getOptionState = (opt) => {
    if (!submitted) return selectedAnswer === opt ? 'selected' : '';
    const lastAns = answers[answers.length - 1];
    const correctAns = lastAns?.question?.answer || currentQ.answer;
    if (opt === correctAns) return 'correct';
    if (opt === selectedAnswer && opt !== correctAns) return 'wrong';
    return '';
  };

  return (
    <div className="quiz-page">
      {/* ── Background ── */}
      <div className="quiz-bg">
        <div className="quiz-bg-circle" />
      </div>

      <div className="quiz-container container">
        {/* ── Header Bar ── */}
        <div className="quiz-header">
          <button className="quiz-back-btn" onClick={() => navigate('/')} aria-label="Exit quiz">
            <ArrowLeft size={18} />
            Exit
          </button>

          <div className="quiz-level-info">
            <span className="quiz-level-emoji">{levelConfig.emoji}</span>
            <span className="quiz-level-name">{levelConfig.title} Level</span>
          </div>

          <div className="quiz-score-display">
            <Zap size={14} color="var(--orange-primary)" fill="var(--orange-primary)" />
            <span>{score * levelConfig.xpPerQuestion} XP</span>
          </div>
        </div>

        {/* ── Progress ── */}
        <div className="quiz-progress-section">
          <ProgressBar
            value={currentIdx + (submitted ? 1 : 0)}
            max={questions.length}
            label={`Question ${currentIdx + 1} of ${questions.length}`}
            showPercent
            height={10}
          />
        </div>

        <div className="quiz-main">
          {/* ── Question Panel ── */}
          <div className="quiz-question-panel" key={currentIdx}>
            {/* Topic badge */}
            <div className="quiz-topic-row">
              <span className="badge badge-orange quiz-topic-badge">
                <BookOpen size={11} />
                {currentQ.topic}
              </span>

              {/* Timer */}
              <div className={`quiz-timer ${timeLeft <= 10 && !submitted ? 'timer-warning' : ''}`}>
                <Clock size={14} />
                <span>{timeLeft}s</span>
                <div className="timer-track">
                  <div
                    className={`timer-fill ${timeLeft <= 10 ? 'timer-fill-warning' : ''}`}
                    style={{ width: `${timerPct}%` }}
                  />
                </div>
              </div>
            </div>

            {/* Question text */}
            <h2 className="question-text">{currentQ.question}</h2>

            {/* Code block (if any) */}
            {currentQ.code && <CodeBlock code={currentQ.code} />}

            {/* Answer options */}
            <div className="options-grid">
              {currentQ.options.map((opt, i) => (
                <AnswerOption
                  key={opt}
                  option={opt}
                  label={LABELS[i]}
                  state={getOptionState(opt)}
                  onClick={() => handleSelectAnswer(opt)}
                  disabled={submitted}
                />
              ))}
            </div>

            {/* Explanation (shown after submit) */}
            {showExplanation && submitted && (
              <div className={`explanation-box ${answers[answers.length - 1]?.correct ? 'explanation-correct' : 'explanation-wrong'}`}>
                <div className="explanation-header">
                  {answers[answers.length - 1]?.correct
                    ? <><CheckCircle size={16} /> Correct! Well done!</>
                    : <><XCircle size={16} /> Incorrect — Correct answer: <strong>{answers[answers.length - 1]?.question?.answer || currentQ.answer}</strong></>
                  }
                </div>
                <p className="explanation-text">{answers[answers.length - 1]?.question?.explanation || currentQ.explanation}</p>
              </div>
            )}

            {/* Action buttons */}
            <div className="quiz-actions">
              {!submitted ? (
                <button
                  id="submit-answer-btn"
                  className="btn btn-primary quiz-submit-btn"
                  onClick={handleSubmit}
                  disabled={!selectedAnswer}
                >
                  Submit Answer
                  <ChevronRight size={18} />
                </button>
              ) : (
                <button
                  id="next-question-btn"
                  className="btn btn-primary quiz-submit-btn animate-scaleIn"
                  onClick={handleNext}
                >
                  {isLastQuestion ? '🏆 View Results' : 'Next Question'}
                  <ChevronRight size={18} />
                </button>
              )}
            </div>
          </div>

          {/* ── Mascot Panel ── */}
          <div className="quiz-mascot-panel">
            <AnimeMascot mode={mascotMode} size={220} animate />

            {/* Score mini card */}
            <div className="quiz-score-card">
              <div className="score-card-item">
                <span className="score-card-label">Score</span>
                <span className="score-card-value">{score}/{questions.length}</span>
              </div>
              <div className="score-card-divider" />
              <div className="score-card-item">
                <span className="score-card-label">XP Earned</span>
                <span className="score-card-value" style={{ color: 'var(--orange-primary)' }}>
                  {score * levelConfig.xpPerQuestion}
                </span>
              </div>
              <div className="score-card-divider" />
              <div className="score-card-item">
                <span className="score-card-label">Remaining</span>
                <span className="score-card-value">{questions.length - currentIdx - 1}</span>
              </div>
            </div>

            {/* Q indicators */}
            <div className="question-dots">
              {questions.map((_, i) => {
                const a = answers[i];
                const dotClass = i < answers.length
                  ? (a?.correct ? 'dot-correct' : 'dot-wrong')
                  : i === currentIdx ? 'dot-current' : 'dot-pending';
                return <div key={i} className={`question-dot ${dotClass}`} title={`Q${i + 1}`} />;
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default QuizPage;
