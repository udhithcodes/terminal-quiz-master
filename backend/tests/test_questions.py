def test_health_check(client):
    """Test health endpoint confirms database and service status."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"


def test_question_count_by_difficulty(client):
    """Test question count endpoint returns accurate category totals."""
    response = client.get("/api/questions/count")
    assert response.status_code == 200
    data = response.json()
    assert data["basic"] >= 3
    assert data["intermediate"] >= 1
    assert data["advanced"] >= 1
    assert data["total"] >= 5


def test_question_retrieval_by_difficulty(client):
    """Test retrieving questions filtered by difficulty."""
    response = client.get("/api/questions?difficulty=basic")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3
    for q in data:
        assert q["difficulty_level"] == "basic"
        # Security test: Ensure correct_answer is never exposed!
        assert "correct_answer" not in q
        assert "explanation" not in q
        assert "options" in q
        assert len(q["options"]) == 4


def test_question_retrieval_by_topic(client):
    """Test retrieving questions filtered by topic."""
    response = client.get("/api/questions?topic=Variables")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["topic"] == "Variables"


def test_get_single_question_by_id(client):
    """Test retrieving a single question without exposing the correct answer."""
    response = client.get("/api/questions/test_b01")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "test_b01"
    assert data["question_text"] == "What is a variable in Python?"
    assert "correct_answer" not in data
    assert "explanation" not in data


def test_get_nonexistent_question_404(client):
    """Test 404 response for nonexistent question ID."""
    response = client.get("/api/questions/nonexistent_id")
    assert response.status_code == 404
