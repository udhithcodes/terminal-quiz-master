from typing import List, Optional
from sqlalchemy import Column, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(String(50), primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    option_a = Column(Text, nullable=False)
    option_b = Column(Text, nullable=False)
    option_c = Column(Text, nullable=False)
    option_d = Column(Text, nullable=False)
    correct_answer = Column(String(50), nullable=False)
    explanation = Column(Text, nullable=False)
    difficulty_level = Column(String(20), nullable=False, index=True)
    topic = Column(String(100), nullable=False, index=True)
    code_snippet = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False, index=True)

    @property
    def options_list(self) -> List[str]:
        return [self.option_a, self.option_b, self.option_c, self.option_d]

    def get_correct_letter(self) -> str:
        """Return 'A', 'B', 'C', or 'D' representing the correct option."""
        ans = (self.correct_answer or "").strip()
        if ans.upper() in ["A", "B", "C", "D"]:
            return ans.upper()
        # If it was stored as the text value, find matching option
        for letter, opt in [("A", self.option_a), ("B", self.option_b), ("C", self.option_c), ("D", self.option_d)]:
            if opt.strip().lower() == ans.lower():
                return letter
        return "A"

    def get_correct_text(self) -> str:
        """Return the text value of the correct option."""
        letter = self.get_correct_letter()
        mapping = {"A": self.option_a, "B": self.option_b, "C": self.option_c, "D": self.option_d}
        return mapping.get(letter, self.option_a)

    def check_is_correct(self, user_answer: str) -> bool:
        """Check if submitted answer matches either the letter (A/B/C/D) or text."""
        if not user_answer:
            return False
        cleaned = user_answer.strip()
        # Check against letter
        if cleaned.upper() == self.get_correct_letter():
            return True
        # Check against text
        if cleaned.lower() == self.get_correct_text().strip().lower():
            return True
        return False

    def __repr__(self):
        return f"<Question(id='{self.id}', level='{self.difficulty_level}', topic='{self.topic}')>"
