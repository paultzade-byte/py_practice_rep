# tests/conftest.py

import pytest
from core.base_client import BaseAPIClient
from services.booker_service import BookerServices

@pytest.fixture(scope="session")
def api_client():
	with BaseAPIClient(base_url="https://restful-booker.herokuapp.com/") as client:
		yield client

@pytest.fixture(scope="session")
def booker_service(api_client):
	return BookerServices(client=api_client)

@pytest.fixture(scope="session")
def auth_token(api_client):
	"""get token for tests"""
	payload = {
		"username": "admin",
		"password": "password123"
	}
	response = api_client.post("auth", json=payload)

	# check if the authorization was successful , OR print "Token not recieved"
	assert response.status_code == 200, "Token not recieved"

	token = response.json().get("token")
	return token

@pytest.fixture(scope="session")
def temp_booking_id(booker_service):
	# First create booking to get atomicity of the test
	# 1. Preparing test data
	payload = {
		"firstname": "Dohn",
		"lastname": "Joe",
		"totalprice": 150,
		"depositpaid": True,
		"bookingdates": {
			"checkin": "2026-07-01",
			"checkout": "2026-07-10"
		}
	}

	# 2. Creating booking
	created_booking = booker_service.create_booking(payload)
	yield created_booking.bookingid
