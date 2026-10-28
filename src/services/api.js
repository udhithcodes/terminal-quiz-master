// ─────────────────────────────────────────────────────────────────
// API Service — Connects Terminal Quiz Master React to FastAPI
// ─────────────────────────────────────────────────────────────────

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

const getAuthHeaders = () => {
  const token = localStorage.getItem('tqm_token');
  return token ? { Authorization: `Bearer ${token}` } : {};
};

const request = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;
  const headers = {
    'Content-Type': 'application/json',
    ...getAuthHeaders(),
    ...options.headers,
  };

  try {
    const res = await fetch(url, { ...options, headers });
    if (!res.ok) {
      const errorBody = await res.json().catch(() => ({}));
      const error = new Error(errorBody.detail || `Request failed with status ${res.status}`);
      error.status = res.status;
      error.body = errorBody;
      throw error;
    }
    return await res.json();
  } catch (err) {
    console.warn(`[API] ${options.method || 'GET'} ${endpoint} error:`, err.message);
    throw err;
  }
};

export const api = {
  // Health
  checkHealth: () => request('/health'),

  // Questions
  getQuestionCounts: () => request('/questions/count'),
  getQuestions: (difficulty, topic) => {
    const params = new URLSearchParams();
    if (difficulty) params.append('difficulty', difficulty);
    if (topic) params.append('topic', topic);
    return request(`/questions?${params.toString()}`);
  },
  getQuestionById: (id) => request(`/questions/${id}`),

  // Quiz Lifecycle
  startQuiz: (difficulty = 'basic', questionCount = 10) =>
    request('/quizzes', {
      method: 'POST',
      body: JSON.stringify({ difficulty, question_count: questionCount }),
    }),

  getQuiz: (quizId) => request(`/quizzes/${quizId}`),

  submitAnswer: (quizId, questionId, selectedAnswer) =>
    request(`/quizzes/${quizId}/answers`, {
      method: 'POST',
      body: JSON.stringify({
        question_id: questionId,
        selected_answer: selectedAnswer,
      }),
    }),

  completeQuiz: (quizId) =>
    request(`/quizzes/${quizId}/complete`, {
      method: 'POST',
    }),

  getQuizResults: (quizId) => request(`/quizzes/${quizId}/results`),

  // Leaderboard
  getLeaderboard: (limit = 50) => request(`/leaderboard?limit=${limit}`),

  // User & History
  getUserProgress: () => request('/users/me/progress'),
  getUserHistory: () => request('/users/me/history'),

  // Authentication
  login: async (username, password) => {
    const data = await request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
    if (data.access_token) {
      localStorage.setItem('tqm_token', data.access_token);
      localStorage.setItem('tqm_user', JSON.stringify(data.user));
    }
    return data;
  },

  register: async (username, email, password) => {
    const data = await request('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, email, password }),
    });
    if (data.access_token) {
      localStorage.setItem('tqm_token', data.access_token);
      localStorage.setItem('tqm_user', JSON.stringify(data.user));
    }
    return data;
  },

  getMe: () => request('/auth/me'),

  logout: () => {
    localStorage.removeItem('tqm_token');
    localStorage.removeItem('tqm_user');
  },
};

export default api;
