# Terminal Quiz Master V2

Terminal Quiz Master V2 is an interactive Python quiz application featuring a sleek **React (Vite)** frontend and a robust **Python (FastAPI + SQLAlchemy + SQLite)** backend.

---

## Features

- **Frontend (React + Vite)**: Modern anime-themed gamified interface with mascots, speed-lines, progress bars, tier ranks, streaks, and responsive dark/light modes.
- **Backend (FastAPI + Python 3.13)**: RESTful architecture with Pydantic v2 validation, SQLite database (`terminal_quiz_master.db`), and SQLAlchemy ORM models.
- **Randomized Quizzes**: Server-controlled question selection, preventing correct answers and explanations from leaking to the client prior to submission.
- **Server-Authoritative Scoring**: Backend validation of submitted choices, duplicate submission prevention, percentage calculation, and XP rewards.
- **45 Seeded Python Questions**: At least 15 verified questions each for Basic, Intermediate, and Advanced tiers, with explanations and code snippets.
- **XP Progression & Leaderboard**: Real-time user ranking, tiered ranks (*Training Arc*, *Rising Challenger*, *Skilled Coder*, *Coding Legend*), and attempt history.
- **Security & Integrity**: Bcrypt password hashing, JWT Bearer authentication, CORS support, and anonymous quiz session support.
- **Automated Test Suite**: 25 comprehensive Pytest test cases covering database models, APIs, answer logic, and access control.

---

## Quick Start (macOS)

### 1. Start the Backend API

```bash
# 1. Create and activate Python virtual environment
python3 -m venv backend/venv
source backend/venv/bin/activate

# 2. Install backend dependencies
pip install -r backend/requirements.txt

# 3. Seed the database (45 questions & demo users)
python backend/seed.py

# 4. Start the FastAPI server
uvicorn app.main:app --host 127.0.0.1 --port 8000 --app-dir backend --reload
```
API Documentation will be live at:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 2. Start the React Frontend

In another terminal window:

```bash
# Install Node dependencies (if not already installed)
npm install

# Start Vite development server
npm run dev
```
The React frontend will be accessible at: [http://localhost:5173](http://localhost:5173).

---

## Running Backend Tests

```bash
backend/venv/bin/pytest backend/tests -v
```

---

## Documentation

For full backend architectural details, database schemas, and REST endpoint specifications, see [`backend/README.md`](file:///Users/apple/Desktop/udhith%20repos/terminal-quiz-master/backend/README.md).