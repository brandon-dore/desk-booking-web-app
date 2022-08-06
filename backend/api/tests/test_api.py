import datetime
import pytest
import sqlalchemy as sa
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import sqlalchemy
from api.database import Base
from api.api import app, get_db

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost:5432/desk_booking_db_testing"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


class TestData:
    user_request = {
        "name": "John Smith",
        "email": "test@test.com",
        "password": "testpass"
    }
    team_request = {"name": "Test Team"}
    room_request = {"name": "Test Room"}
    desk_request_no_team = {
        "number": 4,
        "room": "Test Room",
    }
    desk_request = {
        "number": 4,
        "room": "Test Room",
        "assigned_team": "Test Team"
    }
    booking_request = {
        "approved_status": False,
        "date": str(datetime.date(2020, 5, 17)),
        "desk_number": 4,
        "user_email": "test@test.com",
        "room_name": "Test Room"
    }


class TestCreateAndGet(TestData):

    @pytest.fixture(autouse=True)
    def test_db(self):
        Base.metadata.create_all(bind=engine)
        yield
        Base.metadata.drop_all(bind=engine)

    def test_create_and_get_user(self):
        response = client.post(
            "/users/",
            json=self.user_request,
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["email"] == "test@test.com"
        user_email = data["email"]

        response = client.get(f"/users/{user_email}")
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["email"] == "test@test.com"

    def test_create_and_get_team(self):
        response = client.post(
            "/teams/",
            json=self.team_request,
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["name"] == "Test Team"
        team_name = data["name"]

        response = client.get(f"/teams/{team_name}")
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["name"] == "Test Team"

    def test_create_and_get_room(self):
        response = client.post(
            "/rooms/",
            json=self.room_request,
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["name"] == "Test Room"
        room_name = data["name"]

        response = client.get(f"/rooms/{room_name}")
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["name"] == "Test Room"

    def test_create_and_get_desk_with_no_team(self):
        client.post(
            "/rooms/",
            json=self.room_request,
        )
        response = client.post(
            "/desks/",
            json=self.desk_request_no_team,
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["number"] == 4
        assert data["room"] == "Test Room"

        desk_number = data["number"]
        room_name = data["room"]

        response = client.get(f"/desks/{room_name}/{desk_number}")
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["number"] == 4
        assert data["room"] == "Test Room"

    def test_create_and_get_desk_with_team(self):
        client.post(
            "/rooms/",
            json=self.room_request,
        )

        client.post(
            "/teams/",
            json=self.team_request,
        )

        response = client.post(
            "/desks/",
            json=self.desk_request,
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

    def test_create_and_get_booking(self):
        client.post(
            "/users/",
            json=self.user_request,
        )

        client.post(
            "/rooms/",
            json=self.room_request,
        )

        client.post(
            "/teams/",
            json=self.team_request,
        )

        client.post(
            "/desks/",
            json=self.desk_request,
        )

        response = client.post(
            "/bookings/",
            json=self.booking_request,
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["approved_status"] == False
        assert data["date"] == str(datetime.date(2020, 5, 17))
        assert data["desk"]["number"] == 4
        assert data["user"]["email"] == "test@test.com"
        assert data["desk"]["room"] == "Test Room"

        date = data["date"]
        user_email = data["user"]["email"]

        response = client.get(f"/bookings/{date}/{user_email}")
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["approved_status"] == False
        assert data["date"] == str(datetime.date(2020, 5, 17))
        assert data["desk"]["number"] == 4
        assert data["user"]["email"] == "test@test.com"
        assert data["desk"]["room"] == "Test Room"
