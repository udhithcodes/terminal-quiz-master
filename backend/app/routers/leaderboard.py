from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.user import User
from app.models.quiz_attempt import QuizAttempt
from app.schemas.leaderboard import LeaderboardUserResponse

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])

AVATARS = ["🌸", "🔥", "⚡", "⚔️", "🦁", "🧙", "🎯", "🌩️", "🦊", "🐲"]


@router.get("", response_model=List[LeaderboardUserResponse])
def get_leaderboard(
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Retrieve users ranked by total XP."""
    users = (
        db.query(User)
        .order_by(User.total_xp.desc(), User.created_at.asc())
        .limit(limit)
        .all()
    )

    results: List[LeaderboardUserResponse] = []
    for rank_idx, u in enumerate(users, start=1):
        # Count quizzes completed
        quiz_count = (
            db.query(QuizAttempt)
            .filter(QuizAttempt.user_id == u.id)
            .count()
        )
        avatar = AVATARS[(u.id - 1) % len(AVATARS)]
        results.append(
            LeaderboardUserResponse(
                id=u.id,
                name=u.username,
                username=u.username,
                avatar=avatar,
                xp=u.total_xp,
                total_xp=u.total_xp,
                quizzes=quiz_count,
                streak=max(1, (u.total_xp // 250) + 1),
                rank=rank_idx,
            )
        )

    return results
