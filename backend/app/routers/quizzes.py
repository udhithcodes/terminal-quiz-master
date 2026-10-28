from typing import Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user_optional
from app.models.user import User
from app.schemas.quiz import (
    QuizCreateRequest,
    QuizSessionResponse,
    AnswerSubmitRequest,
    AnswerSubmitResponse,
)
from app.schemas.result import QuizResultResponse
from app.schemas.question import QuestionPublic
from app.services.quiz_service import (
    create_quiz_session,
    get_quiz_session_or_404,
    submit_answer,
)
from app.services.scoring_service import complete_quiz, get_quiz_results

router = APIRouter(prefix="/quizzes", tags=["Quiz Sessions"])


@router.post("", response_model=QuizSessionResponse, status_code=status.HTTP_201_CREATED)
def start_quiz(
    payload: QuizCreateRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    """
    Create a new quiz session with randomly selected questions for the given difficulty.
    Questions and answer options are returned without the correct answers.
    """
    return create_quiz_session(
        db=db,
        difficulty=payload.difficulty,
        question_count=payload.question_count,
        user=current_user,
    )


@router.get("/{quiz_id}", response_model=QuizSessionResponse)
def get_quiz_status(
    quiz_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    """Retrieve the current state, progress, and questions of a quiz session."""
    session = get_quiz_session_or_404(db, quiz_id, current_user)

    # Reconstruct questions in order
    questions_list = [
        QuestionPublic.model_validate(sq.question)
        for sq in session.session_questions
    ]

    return QuizSessionResponse(
        id=session.id,
        quiz_id=session.id,
        difficulty_level=session.difficulty_level,
        status=session.status,
        total_questions=session.total_questions,
        correct_answers=session.correct_answers,
        current_score=session.current_score,
        start_time=session.start_time,
        completion_time=session.completion_time,
        questions=questions_list,
    )


@router.post("/{quiz_id}/answers", response_model=AnswerSubmitResponse)
def submit_quiz_answer(
    quiz_id: str,
    payload: AnswerSubmitRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    """
    Submit an answer for a specific question within this quiz session.
    Validates choice, checks duplicate submissions, updates progress, and returns feedback.
    """
    return submit_answer(
        db=db,
        quiz_id=quiz_id,
        question_id=payload.question_id,
        selected_answer=payload.selected_answer,
        user=current_user,
    )


@router.post("/{quiz_id}/complete", response_model=QuizResultResponse)
def finalize_quiz(
    quiz_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    """
    Finalize a completed quiz session, calculating final score, percentage, and awarding XP.
    Idempotent: Repeated calls return the finalized results without re-awarding XP.
    """
    return complete_quiz(
        db=db,
        quiz_id=quiz_id,
        user=current_user,
    )


@router.get("/{quiz_id}/results", response_model=QuizResultResponse)
def get_quiz_final_results(
    quiz_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    """Retrieve the finalized results and comprehensive answer review of a quiz session."""
    return get_quiz_results(
        db=db,
        quiz_id=quiz_id,
        user=current_user,
    )
