import uuid
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class QuizSession(Base):
    __tablename__ = "quiz_sessions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    difficulty_level = Column(String(20), nullable=False, index=True)
    status = Column(String(20), default="in_progress", nullable=False, index=True)  # in_progress, completed, abandoned
    total_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, default=0, nullable=False)
    current_score = Column(Integer, default=0, nullable=False)
    start_time = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completion_time = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    user = relationship("User", back_populates="sessions")
    session_questions = relationship(
        "QuizSessionQuestion",
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="QuizSessionQuestion.order_index",
    )
    answers = relationship("QuizAnswer", back_populates="session", cascade="all, delete-orphan")
    attempt = relationship("QuizAttempt", back_populates="session", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<QuizSession(id='{self.id}', status='{self.status}', score={self.current_score}/{self.total_questions})>"


class QuizSessionQuestion(Base):
    """Stores the specific questions selected for a quiz session in fixed sequence."""
    __tablename__ = "quiz_session_questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_session_id = Column(String(36), ForeignKey("quiz_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(String(50), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    order_index = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("quiz_session_id", "question_id", name="uq_session_assigned_question"),
    )

    # Relationships
    session = relationship("QuizSession", back_populates="session_questions")
    question = relationship("Question")

    def __repr__(self):
        return f"<QuizSessionQuestion(session='{self.quiz_session_id}', question='{self.question_id}', order={self.order_index})>"


class QuizAnswer(Base):
    __tablename__ = "quiz_answers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_session_id = Column(String(36), ForeignKey("quiz_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(String(50), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    selected_answer = Column(String(255), nullable=False)
    is_correct = Column(Boolean, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("quiz_session_id", "question_id", name="uq_session_question_answer"),
    )

    # Relationships
    session = relationship("QuizSession", back_populates="answers")
    question = relationship("Question")

    def __repr__(self):
        return f"<QuizAnswer(session='{self.quiz_session_id}', question='{self.question_id}', correct={self.is_correct})>"
