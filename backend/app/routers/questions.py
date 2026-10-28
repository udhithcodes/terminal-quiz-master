from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.question import Question
from app.schemas.question import QuestionPublic, QuestionCountResponse

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.get("/count", response_model=QuestionCountResponse)
def get_question_counts(db: Session = Depends(get_db)):
    """Return the number of available active questions broken down by difficulty."""
    basic_count = (
        db.query(Question)
        .filter(Question.difficulty_level == "basic", Question.is_active.is_(True))
        .count()
    )
    inter_count = (
        db.query(Question)
        .filter(Question.difficulty_level == "intermediate", Question.is_active.is_(True))
        .count()
    )
    adv_count = (
        db.query(Question)
        .filter(Question.difficulty_level == "advanced", Question.is_active.is_(True))
        .count()
    )
    return QuestionCountResponse(
        basic=basic_count,
        intermediate=inter_count,
        advanced=adv_count,
        total=basic_count + inter_count + adv_count,
    )


@router.get("", response_model=List[QuestionPublic])
def list_questions(
    difficulty: Optional[str] = Query(None, description="Filter by difficulty: basic, intermediate, advanced"),
    topic: Optional[str] = Query(None, description="Filter by topic"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Retrieve public questions with optional difficulty and topic filters (correct answers hidden)."""
    query = db.query(Question).filter(Question.is_active.is_(True))

    if difficulty:
        query = query.filter(Question.difficulty_level == difficulty.strip().lower())
    if topic:
        query = query.filter(Question.topic.ilike(f"%{topic.strip()}%"))

    questions = query.offset(skip).limit(limit).all()
    return [QuestionPublic.model_validate(q) for q in questions]


@router.get("/{question_id}", response_model=QuestionPublic)
def get_question_by_id(question_id: str, db: Session = Depends(get_db)):
    """Retrieve an individual question by ID without exposing its correct answer."""
    question = (
        db.query(Question)
        .filter(Question.id == question_id, Question.is_active.is_(True))
        .first()
    )
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Question '{question_id}' not found.",
        )
    return QuestionPublic.model_validate(question)
