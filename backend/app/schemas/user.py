from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict, Field


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100)


class UserLogin(BaseModel):
    username: str = Field(..., description="Username or email")
    password: str = Field(..., min_length=1)


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    total_xp: int
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class LevelStats(BaseModel):
    completed: int = 0
    best_score: int = 0
    attempts: int = 0


class UserProgressResponse(BaseModel):
    total_xp: int = 0
    level: int = 1
    basic: LevelStats
    intermediate: LevelStats
    advanced: LevelStats


class UserHistoryItem(BaseModel):
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
