# Terminal Quiz Master V2 — Backend & Database

A production-grade Python backend built with **FastAPI**, **SQLAlchemy ORM**, **SQLite**, and **Pydantic v2**. Provides robust REST APIs, randomized quiz sessions, server-authoritative scoring, XP progression, and JWT authentication.

---

## Architecture Overview

```
backend/
├── app/
│   ├── main.py              # FastAPI application, CORS, lifespans & router mount
│   ├── config.py            # Environment settings (Pydantic SettingsConfigDict)
│   ├── database.py          # SQLAlchemy engine, sessionmaker & foreign key pragma
│   ├── dependencies.py      # Auth and transactional DB session dependencies
│   ├── models/              # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── user.py          # Users table with hashed passwords and total XP
│   │   ├── question.py      # Questions table with 4 options and difficulty levels
│   │   ├── quiz_session.py  # QuizSessions, SessionQuestions, QuizAnswers
│   │   └── quiz_attempt.py  # QuizAttempts for historical and XP tracking
│   ├── schemas/             # Pydantic validation & response schemas
│   │   ├── __init__.py
│   │   ├── user.py          # UserCreate, UserLogin, UserResponse, UserProgress
│   │   ├── question.py      # QuestionPublic, QuestionDetail, QuestionCount
│   │   ├── quiz.py          # QuizCreateRequest, QuizSessionResponse, AnswerSubmit
│   │   ├── result.py        # QuizResultResponse, AnswerReviewItem
│   │   └── leaderboard.py   # LeaderboardUserResponse
│   ├── routers/             # REST API route handlers
│   │   ├── __init__.py
│   │   ├── health.py        # GET /api/health
│   │   ├── questions.py     # GET /api/questions, /count, /{id}
│   │   ├── quizzes.py       # POST /api/quizzes, submit answers, complete, results
│   │   ├── users.py         # GET /api/users/me/progress, /history
│   │   ├── leaderboard.py   # GET /api/leaderboard
│   │   └── auth.py          # POST /api/auth/register, /login, GET /api/auth/me
│   ├── services/            # Pure business logic services
│   │   ├── __init__.py
│   │   ├── quiz_service.py  # Session lifecycle, question sampling, answer checks
│   │   └── scoring_service.py # Scoring, XP calculations, idempotent completion
│   └── auth/                # Security utilities
│       ├── __init__.py
│       └── security.py      # Bcrypt password hashing & JWT token management
├── tests/                   # Pytest test suite (25 automated tests)
│   ├── __init__.py
│   ├── conftest.py          # In-memory SQLite fixtures & mock client
│   ├── test_questions.py    # Health, category counts, filtering, answer secrecy
│   ├── test_quizzes.py      # Quiz creation, answer validation, duplicate checks
│   ├── test_scoring.py      # Scoring calculations, XP rules, completion idempotency
│   └── test_auth.py         # Registration, login, auth protection, forbidden access
├── seed.py                  # Idempotent database seeder (45 questions + demo users)
├── requirements.txt         # Pinned backend dependencies
├── .env.example             # Example environment configuration
├── .env                     # Local environment file
└── README.md                # This documentation file
```

---

## Database Design (`terminal_quiz_master.db`)

1. **`users`**:
   - `id` (INTEGER, PK, autoincrement)
   - `username` (VARCHAR(50), UNIQUE, INDEX)
   - `email` (VARCHAR(100), UNIQUE, INDEX)
   - `hashed_password` (VARCHAR(255))
   - `total_xp` (INTEGER, DEFAULT 0)
   - `created_at` (TIMESTAMP)

2. **`questions`**:
   - `id` (VARCHAR(50), PK)
   - `question_text` (TEXT)
   - `option_a`, `option_b`, `option_c`, `option_d` (TEXT)
   - `correct_answer` (VARCHAR(50))
   - `explanation` (TEXT)
   - `difficulty_level` (VARCHAR(20), INDEX: 'basic', 'intermediate', 'advanced')
   - `topic` (VARCHAR(100), INDEX)
   - `code_snippet` (TEXT, nullable)
   - `created_at` (TIMESTAMP)
   - `is_active` (BOOLEAN, DEFAULT True)

3. **`quiz_sessions`**:
   - `id` (VARCHAR(36), PK, UUID4)
   - `user_id` (INTEGER, FK `users.id`, nullable for anonymous players)
   - `difficulty_level` (VARCHAR(20))
   - `status` (VARCHAR(20): 'in_progress', 'completed')
   - `total_questions` (INTEGER)
   - `correct_answers` (INTEGER)
   - `current_score` (INTEGER)
   - `start_time` (TIMESTAMP)
   - `completion_time` (TIMESTAMP, nullable)

4. **`quiz_session_questions`**:
   - Links selected questions in fixed sequence for a quiz session.
   - `UniqueConstraint('quiz_session_id', 'question_id')`

5. **`quiz_answers`**:
   - `id` (INTEGER, PK)
   - `quiz_session_id` (VARCHAR(36), FK `quiz_sessions.id`)
   - `question_id` (VARCHAR(50), FK `questions.id`)
   - `selected_answer` (VARCHAR(255))
   - `is_correct` (BOOLEAN)
   - `created_at` (TIMESTAMP)
   - `UniqueConstraint('quiz_session_id', 'question_id')` — prevents duplicate submissions.

6. **`quiz_attempts`**:
   - Persisted completed quiz results.
   - `quiz_session_id` is UNIQUE to guarantee idempotency and prevent duplicate points.

---

## Setup & Running Instructions (macOS)

### 1. Create and Activate Virtual Environment

```bash
cd "/Users/apple/Desktop/udhith repos/terminal-quiz-master"
python3 -m venv backend/venv
source backend/venv/bin/activate
```

### 2. Install Backend Dependencies

```bash
pip install -r backend/requirements.txt
```

### 3. Initialize & Seed Database

```bash
python backend/seed.py
```
*Seeds 45 questions (15 Basic, 15 Intermediate, 15 Advanced) and 8 demo users idempotently.*

### 4. Start FastAPI Server

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --app-dir backend --reload
```
Server runs at: `http://127.0.0.1:8000`

### 5. Run the Automated Tests

```bash
pytest backend/tests -v
```

### 6. Interactive API Documentation

Open your browser to:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## REST API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Check service & SQLite database health |
| `GET` | `/api/questions/count` | Total active questions by difficulty |
| `GET` | `/api/questions` | Query questions with `difficulty` & `topic` filters (answers hidden) |
| `GET` | `/api/questions/{id}` | Retrieve individual question (answers hidden) |
| `POST` | `/api/quizzes` | Create quiz session with randomized questions |
| `GET` | `/api/quizzes/{quiz_id}` | Retrieve current session status & questions |
| `POST` | `/api/quizzes/{quiz_id}/answers` | Submit answer (`A`/`B`/`C`/`D` or option text) with instant feedback |
| `POST` | `/api/quizzes/{quiz_id}/complete` | Finalize session, calculate score & award XP (idempotent) |
| `GET` | `/api/quizzes/{quiz_id}/results` | Retrieve final score, review cards & explanations |
| `GET` | `/api/leaderboard` | Top players ranked by XP |
| `GET` | `/api/users/me/progress` | Authenticated user learning progress & stats |
| `GET` | `/api/users/me/history` | Authenticated user past quiz attempts |
| `POST` | `/api/auth/register` | Register new user account |
| `POST` | `/api/auth/login` | Authenticate user & return JWT Bearer token |
| `GET` | `/api/auth/me` | Current authenticated user profile |
