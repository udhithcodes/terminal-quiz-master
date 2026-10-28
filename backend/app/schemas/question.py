from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, computed_field


class QuestionBase(BaseModel):
    question_text: str = Field(..., description="The main question prompt")
    option_a: str = Field(..., description="Option A text")
    option_b: str = Field(..., description="Option B text")
    option_c: str = Field(..., description="Option C text")
    option_d: str = Field(..., description="Option D text")
    difficulty_level: str = Field(..., description="'basic', 'intermediate', or 'advanced'")
    topic: str = Field(..., description="Topic of the question")
    code_snippet: Optional[str] = Field(None, description="Optional Python code snippet")


class QuestionCreate(QuestionBase):
    id: Optional[str] = Field(None, description="Optional custom ID (e.g., 'b01')")
    correct_answer: str = Field(..., description="Correct option ('A', 'B', 'C', 'D' or option text)")
    explanation: str = Field(..., description="Explanation of why the answer is correct")


class QuestionPublic(BaseModel):
    """Public question representation that strictly conceals the correct answer and explanation."""
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    difficulty_level: str
    topic: str
    code_snippet: Optional[str] = None

    # Frontend-friendly computed properties
    @computed_field
    def question(self) -> str:
        return self.question_text

    @computed_field
    def level(self) -> str:
        return self.difficulty_level

    @computed_field
    def code(self) -> Optional[str]:
        return self.code_snippet

    @computed_field
    def options(self) -> List[str]:
        return [self.option_a, self.option_b, self.option_c, self.option_d]


class QuestionDetail(QuestionPublic):
    """Full question details including correct answer and explanation (for post-submission / admin)."""
    correct_answer: str
    explanation: str
    is_active: bool = True
    created_at: Optional[datetime] = None

    @computed_field
    def answer(self) -> str:
        return self.correct_answer


class QuestionCountResponse(BaseModel):
    basic: int
    intermediate: int
    advanced: int
    total: int
