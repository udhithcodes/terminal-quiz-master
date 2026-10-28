def test_create_quiz_session(client):
    """Test successful quiz creation with randomized questions and concealed answers."""
    response = client.post("/api/quizzes", json={"difficulty": "basic", "question_count": 2})
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["difficulty_level"] == "basic"
    assert data["status"] == "in_progress"
    assert len(data["questions"]) == 2
    # Ensure correct answers are hidden
    for q in data["questions"]:
        assert "correct_answer" not in q
        assert "explanation" not in q


def test_create_quiz_invalid_difficulty(client):
    """Test rejection of invalid difficulty level."""
    response = client.post("/api/quizzes", json={"difficulty": "extreme", "question_count": 5})
    assert response.status_code == 400
    assert "Invalid difficulty" in response.json()["detail"]


def test_create_quiz_invalid_count(client):
    """Test rejection of negative or zero question count."""
    response = client.post("/api/quizzes", json={"difficulty": "basic", "question_count": 0})
    assert response.status_code == 422 or response.status_code == 400


def test_submit_correct_answer(client):
    """Test submitting a correct answer choice."""
    # Create quiz
    q_res = client.post("/api/quizzes", json={"difficulty": "basic", "question_count": 2})
    quiz_id = q_res.json()["id"]
    first_q = q_res.json()["questions"][0]

    # For test_b01: correct answer is B ("A named storage location for data")
    # For test_b02: correct answer is A ("'aaa'")
    # For test_b03: correct answer is B ("1")
    # We can submit using the correct option text or correct letter
    # Let's inspect which question we got:
    q_id = first_q["id"]
    correct_choice = "B" if q_id in ["test_b01", "test_b03"] else "A"

    ans_res = client.post(
        f"/api/quizzes/{quiz_id}/answers",
        json={"question_id": q_id, "selected_answer": correct_choice},
    )
    assert ans_res.status_code == 200
    ans_data = ans_res.json()
    assert ans_data["is_correct"] is True
    assert ans_data["current_score"] == 1
    assert "explanation" in ans_data
    assert "correct_answer" in ans_data


def test_submit_incorrect_answer(client):
    """Test submitting an incorrect answer choice."""
    q_res = client.post("/api/quizzes", json={"difficulty": "basic", "question_count": 2})
    quiz_id = q_res.json()["id"]
    first_q = q_res.json()["questions"][0]
    q_id = first_q["id"]

    # D is wrong for all basic test questions
    ans_res = client.post(
        f"/api/quizzes/{quiz_id}/answers",
        json={"question_id": q_id, "selected_answer": "D"},
    )
    assert ans_res.status_code == 200
    ans_data = ans_res.json()
    assert ans_data["is_correct"] is False
    assert ans_data["current_score"] == 0
    assert "explanation" in ans_data


def test_submit_invalid_answer_choice(client):
    """Test submitting an invalid option like 'Z'."""
    q_res = client.post("/api/quizzes", json={"difficulty": "basic", "question_count": 2})
    quiz_id = q_res.json()["id"]
    first_q = q_res.json()["questions"][0]

    ans_res = client.post(
        f"/api/quizzes/{quiz_id}/answers",
        json={"question_id": first_q["id"], "selected_answer": "Z"},
    )
    assert ans_res.status_code == 400
    assert "Invalid answer choice" in ans_res.json()["detail"]


def test_submit_question_not_in_quiz_session(client):
    """Test submitting an answer for a question not assigned to this quiz session."""
    q_res = client.post("/api/quizzes", json={"difficulty": "basic", "question_count": 1})
    quiz_id = q_res.json()["id"]

    # Submit for 'test_a01' which is an advanced question not in this basic session
    ans_res = client.post(
        f"/api/quizzes/{quiz_id}/answers",
        json={"question_id": "test_a01", "selected_answer": "A"},
    )
    assert ans_res.status_code == 400
    assert "does not belong to quiz session" in ans_res.json()["detail"]


def test_duplicate_answer_submission_prevented(client):
    """Test that duplicate answer submissions for the same question in a session are rejected."""
    q_res = client.post("/api/quizzes", json={"difficulty": "basic", "question_count": 2})
    quiz_id = q_res.json()["id"]
    first_q = q_res.json()["questions"][0]
    q_id = first_q["id"]

    # First submission succeeds
    ans1 = client.post(
        f"/api/quizzes/{quiz_id}/answers",
        json={"question_id": q_id, "selected_answer": "A"},
    )
    assert ans1.status_code == 200

    # Second submission for the same question must fail
    ans2 = client.post(
        f"/api/quizzes/{quiz_id}/answers",
        json={"question_id": q_id, "selected_answer": "A"},
    )
    assert ans2.status_code == 400
    assert "Duplicate submission" in ans2.json()["detail"]
