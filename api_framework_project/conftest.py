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
def auth_token():
	pass