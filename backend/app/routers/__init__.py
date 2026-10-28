from app.routers.health import router as health_router
from app.routers.questions import router as questions_router
from app.routers.quizzes import router as quizzes_router
from app.routers.users import router as users_router
from app.routers.leaderboard import router as leaderboard_router
from app.routers.auth import router as auth_router

__all__ = [
    "health_router",
    "questions_router",
    "quizzes_router",
    "users_router",
    "leaderboard_router",
    "auth_router",
]
