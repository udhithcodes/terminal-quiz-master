from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.quiz_attempt import QuizAttempt
from app.schemas.user import UserProgressResponse, LevelStats, UserHistoryItem

router = APIRouter(prefix="/users", tags=["User Progress"])


@router.get("/me/progress", response_model=UserProgressResponse)
def get_user_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieve cumulative learning progress, level, and stats for the authenticated user."""
    # Compute level stats for basic, intermediate, advanced
    def get_stats(level_str: str) -> LevelStats:
        attempts = (
            db.query(QuizAttempt)
            .filter(
                QuizAttempt.user_id == current_user.id,
                QuizAttempt.difficulty_level == level_str,
            )
            .all()
        )
        completed_count = len(attempts)
        best = max([int(a.percentage_score) for a in attempts], default=0)
        return LevelStats(
            completed=completed_count,
            best_score=best,
            attempts=completed_count,
        )

    basic_stats = get_stats("basic")
    inter_stats = get_stats("intermediate")
    adv_stats = get_stats("advanced")

    # Compute Level (1 level per 200 XP, starting at Level 1)
    user_level = (current_user.total_xp // 200) + 1

    return UserProgressResponse(
        total_xp=current_user.total_xp,
        level=user_level,
        basic=basic_stats,
        intermediate=inter_stats,
        advanced=adv_stats,
    )


@router.get("/me/history", response_model=List[UserHistoryItem])
def get_user_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieve historical quiz attempts of the authenticated user in reverse chronological order."""
    attempts = (
        db.query(QuizAttempt)
        .filter(QuizAttempt.user_id == current_user.id)
        .order_by(QuizAttempt.completed_at.desc())
        .all()
    )
    return [UserHistoryItem.model_validate(a) for a in attempts]
