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


class TestSetup:
    @pytest.fixture(autouse=True)
    def test_db(self):
        Base.metadata.create_all(bind=engine)
        yield
        Base.metadata.drop_all(bind=engine)

    user_request = {
        "username": "user5482",
        "email": "test@test.com",
        "password": "testpass"
    }
    user_request_invalid = {
        "username": "user5482",
        "email": "test@test.com",
        "password": "testpass56"
    }
    room_request = {"name": "Test Room"}
    desk_request = {
        "number": 4,
        "room_id": 1,
    }
    booking_request = {
        "approved_status": False,
        "date": str(datetime.date(2020, 5, 17)),
        "desk_number": 4,
        "username": "user5482",
        "room_id": 1
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}


class TestCreateAndGet(TestSetup):

    def test_create_and_get_user(self):
        response = client.post(
            "/register",
            json=self.user_request,
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["email"] == "test@test.com"

        response = client.get(f"/users/{1}")
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["email"] == "test@test.com"

    def test_create_and_get_room(self):
        response = client.post(
            "/rooms",
            json=self.room_request,
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["name"] == "Test Room"

        response = client.get(f"/rooms/{1}")
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["name"] == "Test Room"

    def test_create_and_get_desk(self):
        client.post(
            "/rooms",
            json=self.room_request,
        )
        response = client.post(
            "/desks",
            json=self.desk_request,
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["number"] == 4
        assert data["room_id"] == 1

        response = client.get(f"/desks/{1}")
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["number"] == 4
        assert data["room_id"] == 1

    def test_create_and_get_booking(self):
        client.post(
            "/register",
            json=self.user_request,
        )
        client.post(
            "/rooms",
            json=self.room_request,
        )
        client.post(
            "/desks",
            json=self.desk_request,
        )
        response = client.post(
            "/bookings",
            json=self.booking_request,
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["approved_status"] == False
        assert data["date"] == str(datetime.date(2020, 5, 17))
        assert data["user_id"] == 1
        assert data["desk_id"] == 1

        date = data["date"]

        response = client.get(f"/bookings/{date}/{1}")
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["approved_status"] == False
        assert data["date"] == str(datetime.date(2020, 5, 17))
        assert data["desk_id"] == 1
        assert data["user_id"] == 1


class TestUserAuth(TestSetup):
    def test_register_and_login(self):
        client.post(
            "/register",
            json=self.user_request,
        )

        response = client.post(
            "/login",
            data=self.user_request,
            headers=self.headers
        )

        assert response.status_code == 200, response.text

    def test_register_and_fail_login(self):
        client.post(
            "/register",
            json=self.user_request,
        )

        response = client.post(
            "/login",
            data=self.user_request_invalid,
            headers=self.headers
        )

        assert response.status_code == 401, response.text
