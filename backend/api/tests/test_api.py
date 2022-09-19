import datetime
import pytest
import sqlalchemy as sa
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import sqlalchemy
from api.models import Base
from api.api import app, get_db


class TestPostAndGetEndpoints():

    def test_create_and_get_user(self, client, request_data, response_data):
        response = client.post(
            "/register",
            json=request_data["user_request"],
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data == response_data["user_response"]

        response = client.get(f"/users/{1}")
        assert response.status_code == 200, response.text
        data = response.json()
        assert data == response_data["user_response"]

    def test_create_and_get_room(self, client, request_data, response_data):
        response = client.post(
            "/rooms",
            json=request_data["room_request"],
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data == response_data["room_response"]

        response = client.get(f"/rooms/{1}")
        assert response.status_code == 200, response.text
        data = response.json()
        assert data == response_data["room_response"]

    def test_create_and_get_desk(self, client, request_data, response_data):
        response = client.post(
            "/desks",
            json=request_data["desk_request"],
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data == response_data["desk_response"]
        
        response = client.get(f"/desks/{1}")
        assert response.status_code == 200, response.text
        data = response.json()
        assert data == response_data["desk_response"]


    def test_create_and_get_booking(self, client, request_data, response_data):
        response = client.post(
            "/bookings",
            json=request_data["booking_request"],
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data == response_data["booking_response"]

        response = client.get(f"/bookings/{1}")
        assert response.status_code == 200, response.text
        data = response.json()
        assert data == response_data["booking_response"]



class TestUserAuth():
    def test_register_and_login(self, client, headers, request_data):
        client.post(
            "/register",
            json=request_data["user_request"],
        )

        response = client.post(
            "/login",
            data=request_data["user_request"],
            headers=headers
        )

        assert response.status_code == 200, response.text

    def test_register_and_fail_login(self, client, headers, request_data):
        client.post(
            "/register",
            json=request_data["user_request"],
        )

        response = client.post(
            "/login",
            data=request_data["user_request_invalid"],
            headers=headers
        )

        assert response.status_code == 401, response.text
