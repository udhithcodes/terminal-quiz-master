import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Ensure backend root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import Base, get_db
from app.main import app
from app.models.question import Question
from app.models.user import User
from app.auth.security import hash_password, create_access_token

# In-memory SQLite engine for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Provides a transactional database session per test with rolled back data."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    # Seed core test questions
    sample_questions = [
        Question(
            id="test_b01",
            difficulty_level="basic",
            topic="Variables",
            question_text="What is a variable in Python?",
            option_a="A reserved keyword",
            option_b="A named storage location for data",
            option_c="A built-in module",
            option_d="A loop construct",
            correct_answer="B",
            explanation="Variables refer to reserved memory locations to store values.",
            is_active=True,
        ),
        Question(
            id="test_b02",
            difficulty_level="basic",
            topic="Strings",
            question_text="What is 'a' * 3?",
            option_a="'aaa'",
            option_b="'a3'",
            option_c="'3a'",
            option_d="TypeError",
            correct_answer="A",
            explanation="String repetition operator * repeats the string.",
            is_active=True,
        ),
        Question(
            id="test_b03",
            difficulty_level="basic",
            topic="Operators",
            question_text="What is 5 % 2 in Python?",
            option_a="2.5",
            option_b="1",
            option_c="2",
            option_d="0",
            correct_answer="B",
            explanation="Modulo operator % returns the remainder.",
            is_active=True,
        ),
        Question(
            id="test_i01",
            difficulty_level="intermediate",
            topic="Functions",
            question_text="What does a function return if no return statement is specified?",
            option_a="0",
            option_b="False",
            option_c="None",
            option_d="undefined",
            correct_answer="C",
            explanation="Python functions implicitly return None by default.",
            is_active=True,
        ),
        Question(
            id="test_a01",
            difficulty_level="advanced",
            topic="Generators",
            question_text="Which keyword defines a generator function?",
            option_a="yield",
            option_b="return",
            option_c="generate",
            option_d="produce",
            correct_answer="A",
            explanation="The yield keyword turns a function into a generator.",
            is_active=True,
        ),
    ]
    for q in sample_questions:
        session.merge(q)

    # Seed test users
    user1 = User(
        id=1,
        username="testwarrior",
        email="testwarrior@example.com",
        hashed_password=hash_password("Password123!"),
        total_xp=150,
    )
    user2 = User(
        id=2,
        username="otherwarrior",
        email="otherwarrior@example.com",
        hashed_password=hash_password("Password123!"),
        total_xp=50,
    )
    session.merge(user1)
    session.merge(user2)
    session.commit()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def user_token(db_session):
    return create_access_token(subject=1)


@pytest.fixture(scope="function")
def other_user_token(db_session):
    return create_access_token(subject=2)
