import datetime
import pytest
import sqlalchemy as sa
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from api.models import Base
from api.api import app, get_db
from sqlalchemy_utils import create_database, drop_database, database_exists

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost:5432/desk_booking_db_testing"

engine = create_engine(SQLALCHEMY_DATABASE_URL)


def get_test_db():
    SessionLocal = sessionmaker(bind=engine)
    test_db = SessionLocal()

    try:
        yield test_db
    finally:
        test_db.close()


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    """
    Create a clean database on every test case.
    We use the `sqlalchemy_utils` package here for a few helpers in consistently
    creating and dropping the database.
    """
    if database_exists(SQLALCHEMY_DATABASE_URL):
        drop_database(SQLALCHEMY_DATABASE_URL)
    create_database(SQLALCHEMY_DATABASE_URL)  # Create the test database.
    Base.metadata.create_all(engine)  # Create the tables.
    # Mock the Database Dependency
    app.dependency_overrides[get_db] = get_test_db
    yield  # Run the tests.
    drop_database(SQLALCHEMY_DATABASE_URL)  # Drop the test database.


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def request_data():
    return {'user_request': {
        "username": "user5482",
        "email": "test@test.com",
        "password": "testpass"
    }, 'user_request_invalid': {
        "username": "user5482",
        "email": "test@test.com",
        "password": "testpass56"
    }, 'room_request': {"name": "Test Room"}, 'desk_request': {
        "number": 4,
        "room_id": 1,
    }, 'booking_request': {
        "approved_status": False,
        "date": str(datetime.date(2020, 5, 17)),
        "desk_id": 1,
        "user_id": 1,
    }}


@pytest.fixture()
def response_data():
    return {'user_response':
            {'username': 'user5482', 'email': 'test@test.com', 'admin': False, 'id': 1},
            'room_response': {'name': 'Test Room', 'id': 1},
            'desk_response': {'number': 4, 'room_id': 1, 'id': 1},
            'booking_response': {'approved_status': False, 'date': '2020-05-17', 'desk_id': 1, 'user_id': 1, 'id': 1}}


@pytest.fixture()
def headers():
    return {'Content-Type': 'application/x-www-form-urlencoded'}
