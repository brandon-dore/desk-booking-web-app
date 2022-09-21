import datetime
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models import Base
from app.main import app, get_db
from sqlalchemy_utils import create_database, drop_database, database_exists

SQLALCHEMY_DATABASE_URL = os.environ.get('SQLALCHEMY_DATABASE_URL', 'postgresql://postgres:password@localhost:5432/desk_booking_db_testing')

engine = create_engine(SQLALCHEMY_DATABASE_URL)


def get_test_db():
    """
    Mock override for get_db() dependancy
    """
    SessionLocal = sessionmaker(bind=engine)
    test_db = SessionLocal()

    try:
        yield test_db
    finally:
        test_db.close()


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    """
    Create a new database for each test file
    """
    if database_exists(SQLALCHEMY_DATABASE_URL):
        drop_database(SQLALCHEMY_DATABASE_URL)
    create_database(SQLALCHEMY_DATABASE_URL) 
    Base.metadata.create_all(engine)
    
    app.dependency_overrides[get_db] = get_test_db
    yield
    drop_database(SQLALCHEMY_DATABASE_URL) 

@pytest.fixture(scope="class", autouse=True)
def test_db():
    """
    Recreate tables (remove data) after every test class
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    """
    Creates a mock client for fast api
    """
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def request_data():
    """
    Provide reusable data to send request
    """
    return {
        "user_request": {
            "username": "user5482",
            "email": "test@test.com",
            "password": "testpass",
        },
        "user_request_2": {
            "username": "user1234",
            "email": "test2@test2.com",
            "password": "passtest",
        },
        "user_request_3": {
            "username": "test",
            "email": "test@rando.com",
            "password": "testtest",
        },
        "user_request_edited": {
            "username": "user1234",
            "email": "newemail@gmail.com",
            "password": "passtest",
        },
        "user_request_invalid": {
            "username": "user5482",
            "email": "test@test.com",
            "password": "testpass56",
        },
        "room_request": {"name": "Test Room"},
        "room_request_edited": {"name": "Test Room Edited"},
        "desk_request": {
            "number": 4,
            "room_id": 1,
        },
        "desk_request_edited": {
            "number": 29,
            "room_id": 1,
        },
        "desk_request_multiple": [
            {
                "number": 10,
                "room_id": 1,
            },
            {
                "number": 12,
                "room_id": 1,
            },
            {
                "number": 14,
                "room_id": 1,
            },
        ],
        "booking_request": {
            "approved_status": False,
            "date": str(datetime.date(2020, 5, 17)),
            "desk_id": 1,
            "user_id": 1,
        },
        "booking_request_2": {
            "approved_status": True,
            "date": str(datetime.date(2020, 5, 17)),
            "desk_id": 3,
            "user_id": 2,
        },
        "booking_request_edited": {
            "approved_status": True,
            "date": str(datetime.date(2020, 5, 17)),
            "desk_id": 1,
            "user_id": 1,
        },
    }


@pytest.fixture()
def response_data():
    """
    Provide reusable data to assert against responses
    """
    return {
        "user_response": {
            "username": "user5482",
            "email": "test@test.com",
            "admin": False,
            "id": 1,
        },
        "room_response": {"name": "Test Room", "id": 1},
        "desk_response": {"number": 4, "room_id": 1, "id": 1},
        "booking_response": {
            "approved_status": False,
            "date": "2020-05-17",
            "desk_id": 1,
            "user_id": 1,
            "id": 1,
        },
        "room_response_multiple": [{'number': 4, 'room_id': 1, 'id': 1}, {'number': 10, 'room_id': 1, 'id': 2}, {'number': 12, 'room_id': 1, 'id': 3}, {'number': 14, 'room_id': 1, 'id': 4}],
        "booking_response_multiple": [{'approved_status': False, 'date': '2020-05-17', 'desk_id': 1, 'user_id': 1, 'id': 1}, {'approved_status': True, 'date': '2020-05-17', 'desk_id': 3, 'user_id': 2, 'id': 2}],
        "user_patched_response": {
            "username": "user1234",
            "email": "newemail@gmail.com",
            'admin': False,
            "id": 1
        },
        "room_patched_response": {'name': 'Test Room Edited', 'id': 1},
        "desk_patched_response": {'number': 29, 'room_id': 1, 'id': 1},
        "booking_patched_response": {'approved_status': True, 'date': '2020-05-17', 'desk_id': 1, 'user_id': 1, 'id': 1},
        "logged_in_user_response": {'username': 'user5482', 'email': 'test@test.com', 'admin': False, 'id': 3},
        "logged_in_user_bookings": {'approved_status': False, 'date': '2022-05-17', 'desk_id': 1, 'user_id': 1, 'id': 1}
    }


@pytest.fixture()
def headers():
    return {"Content-Type": "application/x-www-form-urlencoded"}
