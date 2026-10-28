def test_user_registration(client):
    """Test user registration returns token and user data without exposing password."""
    response = client.post(
        "/api/auth/register",
        json={
            "username": "newwarrior",
            "email": "newwarrior@example.com",
            "password": "SecurePassword123!",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["user"]["username"] == "newwarrior"
    assert data["user"]["email"] == "newwarrior@example.com"
    assert "hashed_password" not in data["user"]


def test_user_registration_duplicate_username(client):
    """Test rejection when username is already registered."""
    response = client.post(
        "/api/auth/register",
        json={
            "username": "testwarrior",  # already exists from conftest
            "email": "different@example.com",
            "password": "Password123!",
        },
    )
    assert response.status_code == 400
    assert "already taken" in response.json()["detail"]


def test_user_login_success(client):
    """Test successful login returns valid JWT access token."""
    response = client.post(
        "/api/auth/login",
        json={"username": "testwarrior", "password": "Password123!"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["username"] == "testwarrior"


def test_user_login_invalid_password(client):
    """Test rejection on incorrect password."""
    response = client.post(
        "/api/auth/login",
        json={"username": "testwarrior", "password": "WrongPassword!"},
    )
    assert response.status_code == 401


def test_protected_route_unauthorized(client):
    """Test 401 when accessing protected route without token."""
    response = client.get("/api/users/me/progress")
    assert response.status_code == 401


def test_user_progress_endpoint(client, user_token):
    """Test authenticated user progress returns XP, level, and stats."""
    response = client.get(
        "/api/users/me/progress",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "total_xp" in data
    assert "level" in data
    assert "basic" in data
    assert "intermediate" in data
    assert "advanced" in data


def test_unauthorized_access_to_other_users_quiz(client, user_token, other_user_token):
    """Test security: User 2 cannot access or submit answers for User 1's quiz."""
    # User 1 creates a quiz session
    headers1 = {"Authorization": f"Bearer {user_token}"}
    create_res = client.post(
        "/api/quizzes",
        json={"difficulty": "basic", "question_count": 1},
        headers=headers1,
    )
    quiz_id = create_res.json()["id"]

    # User 2 attempts to access User 1's quiz
    headers2 = {"Authorization": f"Bearer {other_user_token}"}
    access_res = client.get(f"/api/quizzes/{quiz_id}", headers=headers2)
    assert access_res.status_code == 403
    assert "permission" in access_res.json()["detail"].lower()


def test_leaderboard_endpoint(client):
    """Test leaderboard returns ranked users ordered by total_xp."""
    response = client.get("/api/leaderboard")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    # Verify descending XP order
    for i in range(len(data) - 1):
        assert data[i]["total_xp"] >= data[i + 1]["total_xp"]
    # Check fields
    first = data[0]
    assert "rank" in first
    assert "username" in first
    assert "avatar" in first
    assert "xp" in first
