def test_quiz_completion_and_scoring(client):
    """Test finalizing a quiz calculates correct score, percentage, and XP."""
    # Create quiz with 2 questions
    q_res = client.post("/api/quizzes", json={"difficulty": "basic", "question_count": 2})
    quiz_id = q_res.json()["id"]
    questions = q_res.json()["questions"]

    # Submit 1 correct and 1 wrong answer
    q1 = questions[0]
    q2 = questions[1]

    # For q1, answer correctly
    correct_ans = "B" if q1["id"] in ["test_b01", "test_b03"] else "A"
    client.post(
        f"/api/quizzes/{quiz_id}/answers",
        json={"question_id": q1["id"], "selected_answer": correct_ans},
    )

    # For q2, answer wrongly (D is always wrong in our test basic questions)
    client.post(
        f"/api/quizzes/{quiz_id}/answers",
        json={"question_id": q2["id"], "selected_answer": "D"},
    )

    # Complete the quiz
    comp_res = client.post(f"/api/quizzes/{quiz_id}/complete")
    assert comp_res.status_code == 200
    data = comp_res.json()

    assert data["quiz_id"] == quiz_id
    assert data["total"] == 2
    assert data["score"] == 1
    assert data["correct_answers"] == 1
    assert data["incorrect_answers"] == 1
    assert data["percentage"] == 50.0
    # Basic = 10 XP per correct question -> 10 XP
    assert data["xp_earned"] == 10
    assert len(data["answers"]) == 2


def test_idempotent_quiz_completion(client, user_token):
    """Test that repeatedly calling /complete does not double award points or create duplicate attempts."""
    headers = {"Authorization": f"Bearer {user_token}"}
    q_res = client.post(
        "/api/quizzes",
        json={"difficulty": "intermediate", "question_count": 1},
        headers=headers,
    )
    quiz_id = q_res.json()["id"]
    q1 = q_res.json()["questions"][0]

    # Correct answer for test_i01 is C
    client.post(
        f"/api/quizzes/{quiz_id}/answers",
        json={"question_id": q1["id"], "selected_answer": "C"},
        headers=headers,
    )

    # Check user XP before completion
    user_before = client.get("/api/auth/me", headers=headers).json()
    xp_before = user_before["total_xp"]

    # First completion: 1 correct intermediate question (20 XP) + 100% bonus (50 XP) = 70 XP
    res1 = client.post(f"/api/quizzes/{quiz_id}/complete", headers=headers)
    assert res1.status_code == 200
    xp_earned = res1.json()["xp_earned"]
    assert xp_earned == 70

    user_after1 = client.get("/api/auth/me", headers=headers).json()
    assert user_after1["total_xp"] == xp_before + 70

    # Second completion: must NOT add another 70 XP!
    res2 = client.post(f"/api/quizzes/{quiz_id}/complete", headers=headers)
    assert res2.status_code == 200
    assert res2.json()["xp_earned"] == 70

    user_after2 = client.get("/api/auth/me", headers=headers).json()
    assert user_after2["total_xp"] == xp_before + 70  # Still the same, no duplicate points!


def test_get_quiz_results_endpoint(client):
    """Test retrieving finalized results via GET /api/quizzes/{quiz_id}/results."""
    q_res = client.post("/api/quizzes", json={"difficulty": "basic", "question_count": 1})
    quiz_id = q_res.json()["id"]
    q1 = q_res.json()["questions"][0]

    client.post(
        f"/api/quizzes/{quiz_id}/answers",
        json={"question_id": q1["id"], "selected_answer": "D"},
    )
    client.post(f"/api/quizzes/{quiz_id}/complete")

    results_res = client.get(f"/api/quizzes/{quiz_id}/results")
    assert results_res.status_code == 200
    data = results_res.json()
    assert data["quiz_id"] == quiz_id
    assert data["status"] == "completed"
    assert len(data["answers"]) == 1
    assert data["answers"][0]["question"]["explanation"] is not None
