from datetime import datetime, timezone
from typing import Optional, List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.question import Question
from app.models.quiz_session import QuizSession, QuizSessionQuestion, QuizAnswer
from app.models.quiz_attempt import QuizAttempt
from app.schemas.question import QuestionDetail
from app.schemas.result import QuizResultResponse, AnswerReviewItem


XP_MULTIPLIERS = {
    "basic": 10,
    "intermediate": 20,
    "advanced": 30,
}


def calculate_xp(difficulty: str, correct_answers: int, total_questions: int) -> int:
    multiplier = XP_MULTIPLIERS.get(difficulty.lower(), 10)
    base_xp = correct_answers * multiplier
    # Bonus for 100% completion
    if total_questions > 0 and correct_answers == total_questions:
        base_xp += 50
    return base_xp


def complete_quiz(
    db: Session,
    quiz_id: str,
    user: Optional[User] = None,
) -> QuizResultResponse:
    session = db.query(QuizSession).filter(QuizSession.id == quiz_id).first()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quiz session '{quiz_id}' not found.",
        )

    # Permission check
    if session.user_id and user and session.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to finalize this quiz session.",
        )

    # Idempotency check: if already completed, return existing results without re-awarding XP
    existing_attempt = (
        db.query(QuizAttempt)
        .filter(QuizAttempt.quiz_session_id == quiz_id)
        .first()
    )
    if existing_attempt:
        return build_result_response(db, session, existing_attempt)

    # Calculate final scores
    total_q = session.total_questions
    correct_q = session.correct_answers
    incorrect_q = max(0, total_q - correct_q)
    percentage = round((correct_q / total_q) * 100.0, 2) if total_q > 0 else 0.0
    xp_earned = calculate_xp(session.difficulty_level, correct_q, total_q)

    now = datetime.now(timezone.utc)
    session.status = "completed"
    session.completion_time = now

    # Determine user to associate
    user_id = session.user_id or (user.id if user else None)
    if user and not session.user_id:
        session.user_id = user.id

    # Create attempt record
    attempt = QuizAttempt(
        user_id=user_id,
        quiz_session_id=session.id,
        difficulty_level=session.difficulty_level,
        total_questions=total_q,
        correct_answers=correct_q,
        incorrect_answers=incorrect_q,
        percentage_score=percentage,
        xp_earned=xp_earned,
        completed_at=now,
    )
    db.add(attempt)

    # Update user XP if user is linked
    if user_id:
        user_record = db.query(User).filter(User.id == user_id).first()
        if user_record:
            user_record.total_xp += xp_earned

    db.commit()
    db.refresh(session)
    db.refresh(attempt)

    return build_result_response(db, session, attempt)


def get_quiz_results(
    db: Session,
    quiz_id: str,
    user: Optional[User] = None,
) -> QuizResultResponse:
    session = db.query(QuizSession).filter(QuizSession.id == quiz_id).first()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quiz session '{quiz_id}' not found.",
        )

    if session.user_id and user and session.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view results for this quiz session.",
        )

    attempt = (
        db.query(QuizAttempt)
        .filter(QuizAttempt.quiz_session_id == quiz_id)
        .first()
    )
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Quiz session '{quiz_id}' is not yet finalized. Call /complete first.",
        )

    return build_result_response(db, session, attempt)


def build_result_response(
    db: Session,
    session: QuizSession,
    attempt: QuizAttempt,
) -> QuizResultResponse:
    # Build detailed answer review list
    answers_map = {
        ans.question_id: ans
        for ans in db.query(QuizAnswer).filter(QuizAnswer.quiz_session_id == session.id).all()
    }

    session_questions = (
        db.query(QuizSessionQuestion)
        .filter(QuizSessionQuestion.quiz_session_id == session.id)
        .order_by(QuizSessionQuestion.order_index)
        .all()
    )

    review_list: List[AnswerReviewItem] = []
    for sq in session_questions:
        q = sq.question
        user_ans = answers_map.get(q.id)

        question_detail = QuestionDetail(
            id=q.id,
            question_text=q.question_text,
            option_a=q.option_a,
            option_b=q.option_b,
            option_c=q.option_c,
            option_d=q.option_d,
            difficulty_level=q.difficulty_level,
            topic=q.topic,
            code_snippet=q.code_snippet,
            correct_answer=q.get_correct_text(),
            explanation=q.explanation,
            is_active=q.is_active,
            created_at=q.created_at,
        )

        review_list.append(
            AnswerReviewItem(
                question_id=q.id,
                selected=user_ans.selected_answer if user_ans else None,
                correct=user_ans.is_correct if user_ans else False,
                question=question_detail,
            )
        )

    # Time taken
    time_taken = None
    if session.start_time and session.completion_time:
        diff = session.completion_time - session.start_time
        time_taken = max(0, int(diff.total_seconds()))

    return QuizResultResponse(
        id=attempt.id,
        quiz_id=session.id,
        difficulty_level=session.difficulty_level,
        level=session.difficulty_level,
        score=attempt.correct_answers,
        total=attempt.total_questions,
        correct_answers=attempt.correct_answers,
        incorrect_answers=attempt.incorrect_answers,
        percentage=attempt.percentage_score,
        percentage_score=attempt.percentage_score,
        xp_earned=attempt.xp_earned,
        time_taken_seconds=time_taken,
        status=session.status,
        completed_at=attempt.completed_at,
        answers=review_list,
    )
