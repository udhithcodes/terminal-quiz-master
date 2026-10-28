from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.schemas.question import QuestionDetail


class AnswerReviewItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    question_id: str
    selected: Optional[str] = None
    correct: bool
    question: QuestionDetail


class QuizResultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    quiz_id: str
    difficulty_level: str
    level: str
    score: int
    total: int
    correct_answers: int
    incorrect_answers: int
    percentage: float
    percentage_score: float
    xp_earned: int
    time_taken_seconds: Optional[int] = None
    status: str
    completed_at: datetime
    answers: List[AnswerReviewItem] = []


class QuizAttemptSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    quiz_session_id: str
    difficulty_level: str
    total_questions: int
    correct_answers: int
    incorrect_answers: int
    percentage_score: float
    xp_earned: int
    completed_at: datetime
