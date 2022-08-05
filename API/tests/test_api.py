import datetime

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..database import Base
from ..main import app, get_db

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost:5432/desk_booking_db_testing"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    connection = engine.connect()

    # begin a non-ORM transaction
    transaction = connection.begin()

    # bind an individual Session to the connection
    db = TestingSessionLocal(bind=connection)
    # db = Session(engine)

    yield db

    db.rollback()
    connection.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_user():
    response = client.post(
        "/users/",
        json={"name": "John Smith", "email": "test@test.com", "password": "testpass"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "test@test.com"
    user_email = data["email"]

    response = client.get(f"/users/{user_email}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "test@test.com"


def test_create_team():
    response = client.post(
        "/teams/",
        json={"name": "Test Team"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Test Team"
    team_name = data["name"]

    response = client.get(f"/teams/{team_name}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Test Team"


def test_create_room():
    response = client.post(
        "/rooms/",
        json={"name": "Test Room"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Test Room"
    room_name = data["name"]

    response = client.get(f"/rooms/{room_name}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Test Room"


def test_create_desk_with_no_team():
    client.post(
        "/rooms/",
        json={"name": "Test Room"},
    )
    response = client.post(
        "/desks/",
        json={
            "number": 4,
            "room": "Test Room",
            "assigned_team": None
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["number"] == 4
    assert data["room"] == "Test Room"
    assert "assigned_team" in data

    desk_number = data["number"]
    room_name = data["room"]

    response = client.get(f"/desks/{room_name}/{desk_number}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["number"] == 4
    assert data["room"] == "Test Room"


def test_create_desk_with_team():
    client.post(
        "/rooms/",
        json={"name": "Test Room"},
    )

    client.post(
        "/teams/",
        json={"name": "Test Team"},
    )

    response = client.post(
        "/desks/",
        json={
            "number": 4,
            "room": "Test Room",
            "assigned_team": "Test Team"
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["number"] == 4
    assert data["room"] == "Test Room"
    assert data["assigned_team"] == "Test Team"

    desk_number = data["number"]
    room_name = data["room"]

    response = client.get(f"/desks/{room_name}/{desk_number}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["number"] == 4
    assert data["room"] == "Test Room"
    assert data["assigned_team"] == "Test Team"


def test_create_booking():
    client.post(
        "/users/",
        json={"email": "test@test.com", "password": "testpass"},
    )

    client.post(
        "/rooms/",
        json={"name": "Test Room"},
    )

    client.post(
        "/teams/",
        json={"name": "Test Team"},
    )

    client.post(
        "/desks/",
        json={
            "number": 4,
            "room": "Test Room",
            "assigned_team": "Test Team"
        },
    )

    response = client.post(
        "/bookings/",
        json={
            "approved_status": False,
            "date": str(datetime.date(2020, 5, 17)),
            "desk_number": 4,
            "user_email": "test@test.com",
            "room_name": "Test Room"
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["approved_status"] == False
    assert data["date"] == datetime.date(2020, 5, 17)
    assert data["desk_number"] == 4
    assert data["user_email"] == "test@test.com"
    assert data["room_name"] == "Test Room"

    date = data["date"]
    user_email = data["email"]

    response = client.get(f"/bookings/{date}/{user_email}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["approved_status"] == False
    assert data["date"] == datetime.date(2020, 5, 17)
    assert data["desk_number"] == 4
    assert data["user_email"] == "test@test.com"
    assert data["room_name"] == "Test Room"
