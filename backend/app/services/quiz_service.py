import random
from typing import List, Optional, Tuple
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.question import Question
from app.models.quiz_session import QuizSession, QuizSessionQuestion, QuizAnswer
from app.schemas.question import QuestionPublic
from app.schemas.quiz import QuizSessionResponse, AnswerSubmitResponse

VALID_DIFFICULTIES = ["basic", "intermediate", "advanced"]


def get_available_question_count(db: Session, difficulty: str) -> int:
    return (
        db.query(Question)
        .filter(
            Question.difficulty_level == difficulty.lower(),
            Question.is_active.is_(True),
        )
        .count()
    )


def create_quiz_session(
    db: Session,
    difficulty: str,
    question_count: int = 10,
    user: Optional[User] = None,
) -> QuizSessionResponse:
    diff = difficulty.strip().lower()
    if diff not in VALID_DIFFICULTIES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid difficulty '{difficulty}'. Allowed levels are: {', '.join(VALID_DIFFICULTIES)}",
        )

    if question_count < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question count must be at least 1.",
        )

    # Fetch active questions for requested difficulty
    available_questions = (
        db.query(Question)
        .filter(
            Question.difficulty_level == diff,
            Question.is_active.is_(True),
        )
        .all()
    )

    if not available_questions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No questions found for difficulty '{difficulty}'.",
        )

    # Sample randomly up to requested count
    count_to_take = min(question_count, len(available_questions))
    selected_questions = random.sample(available_questions, count_to_take)

    # Create quiz session
    session = QuizSession(
        user_id=user.id if user else None,
        difficulty_level=diff,
        status="in_progress",
        total_questions=len(selected_questions),
        correct_answers=0,
        current_score=0,
    )
    db.add(session)
    db.flush()  # Generate session.id

    # Add questions in ordered sequence
    session_questions = []
    for idx, q in enumerate(selected_questions):
        sq = QuizSessionQuestion(
            quiz_session_id=session.id,
            question_id=q.id,
            order_index=idx,
        )
        db.add(sq)
        session_questions.append(
            QuestionPublic(
                id=q.id,
                question_text=q.question_text,
                option_a=q.option_a,
                option_b=q.option_b,
                option_c=q.option_c,
                option_d=q.option_d,
                difficulty_level=q.difficulty_level,
                topic=q.topic,
                code_snippet=q.code_snippet,
            )
        )

    db.commit()
    db.refresh(session)

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
        questions=session_questions,
    )


def get_quiz_session_or_404(
    db: Session,
    quiz_id: str,
    user: Optional[User] = None,
) -> QuizSession:
    session = db.query(QuizSession).filter(QuizSession.id == quiz_id).first()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quiz session '{quiz_id}' not found.",
        )

    # If session is tied to a user and a different authenticated user requests it, deny
    if session.user_id and user and session.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this quiz session.",
        )

    return session


def submit_answer(
    db: Session,
    quiz_id: str,
    question_id: str,
    selected_answer: str,
    user: Optional[User] = None,
) -> AnswerSubmitResponse:
    session = get_quiz_session_or_404(db, quiz_id, user)

    if session.status != "in_progress":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot submit answers: Quiz session is already '{session.status}'.",
        )

    # Verify that the question belongs to this session
    session_q = (
        db.query(QuizSessionQuestion)
        .filter(
            QuizSessionQuestion.quiz_session_id == quiz_id,
            QuizSessionQuestion.question_id == question_id,
        )
        .first()
    )
    if not session_q:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Question '{question_id}' does not belong to quiz session '{quiz_id}'.",
        )

    question = session_q.question

    # Validate choice is valid A/B/C/D or one of option texts
    valid_letters = ["A", "B", "C", "D"]
    valid_texts = [question.option_a, question.option_b, question.option_c, question.option_d]

    cleaned_answer = selected_answer.strip()
    is_valid_choice = (
        cleaned_answer.upper() in valid_letters
        or any(cleaned_answer.lower() == opt.strip().lower() for opt in valid_texts)
    )
    if not is_valid_choice:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid answer choice '{selected_answer}'. Must be A, B, C, D or match an option.",
        )

    # Check for duplicate submission
    existing_answer = (
        db.query(QuizAnswer)
        .filter(
            QuizAnswer.quiz_session_id == quiz_id,
            QuizAnswer.question_id == question_id,
        )
        .first()
    )
    if existing_answer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Duplicate submission: Question '{question_id}' has already been answered in this session.",
        )

    # Evaluate answer
    is_correct = question.check_is_correct(cleaned_answer)

    # Record answer in DB
    answer = QuizAnswer(
        quiz_session_id=quiz_id,
        question_id=question_id,
        selected_answer=cleaned_answer,
        is_correct=is_correct,
    )
    db.add(answer)

    # Update session progress
    if is_correct:
        session.correct_answers += 1
        session.current_score += 1

    db.commit()
    db.refresh(session)

    # Count how many answers have been submitted
    answers_count = (
        db.query(QuizAnswer)
        .filter(QuizAnswer.quiz_session_id == quiz_id)
        .count()
    )

    return AnswerSubmitResponse(
        question_id=question_id,
        selected_answer=cleaned_answer,
        is_correct=is_correct,
        correct_answer=question.get_correct_text(),
        correct_option=question.get_correct_letter(),
        explanation=question.explanation,
        current_score=session.current_score,
        questions_answered=answers_count,
        total_questions=session.total_questions,
    )
