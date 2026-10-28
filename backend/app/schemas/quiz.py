from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.question import QuestionPublic


class QuizCreateRequest(BaseModel):
    difficulty: str = Field("basic", description="Difficulty level: 'basic', 'intermediate', or 'advanced'")
    question_count: int = Field(10, ge=1, le=50, description="Requested number of questions")


class QuizSessionQuestionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_index: int
    question: QuestionPublic


class QuizSessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    quiz_id: str
    difficulty_level: str
    status: str
    total_questions: int
    correct_answers: int
    current_score: int
    start_time: datetime
    completion_time: Optional[datetime] = None
    questions: List[QuestionPublic] = []

    # Extra aliases for frontend convenience
    @property
    def level(self) -> str:
        return self.difficulty_level


class AnswerSubmitRequest(BaseModel):
    question_id: str = Field(..., description="ID of the question being answered")
    selected_answer: str = Field(..., description="Selected option ('A'/'B'/'C'/'D' or option text)")


class AnswerSubmitResponse(BaseModel):
    question_id: str
    selected_answer: str
    is_correct: bool
    correct_answer: str
    correct_option: str  # 'A', 'B', 'C', or 'D'
    explanation: str
    current_score: int
    questions_answered: int
    total_questions: int
