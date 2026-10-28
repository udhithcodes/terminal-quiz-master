from typing import Optional
from pydantic import BaseModel, ConfigDict


class LeaderboardUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    username: str
    avatar: str = "🧑‍💻"
    xp: int
    total_xp: int
    quizzes: int = 0
    streak: int = 1
    rank: int
