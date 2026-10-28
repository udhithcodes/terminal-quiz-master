from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    quiz_session_id = Column(String(36), ForeignKey("quiz_sessions.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    difficulty_level = Column(String(20), nullable=False, index=True)
    total_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, nullable=False)
    incorrect_answers = Column(Integer, nullable=False)
    percentage_score = Column(Float, nullable=False)
    xp_earned = Column(Integer, nullable=False)
    completed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("quiz_session_id", name="uq_attempt_quiz_session"),
    )

    # Relationships
    user = relationship("User", back_populates="attempts")
    session = relationship("QuizSession", back_populates="attempt")

    def __repr__(self):
        return (
            f"<QuizAttempt(id={self.id}, user_id={self.user_id}, "
            f"score={self.correct_answers}/{self.total_questions}, xp={self.xp_earned})>"
        )
