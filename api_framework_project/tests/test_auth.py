# tests/test_auth.py

from services.booker_service import BookerServices

def test_auth_success(booker_service):
	# using service which validate response through Pydantic
	token = booker_service.create_token(username="admin", password="password123")

	assert token is not None
	assert isinstance(token, str)
	assert len(token) > 0

def test_auth_invalid_credentials(api_client):
	# directly using base client
	# because the create_token method 'll fail with ValidationError (it 'll not find "token" field)
	payload = {"username": "admin", "password": "wrong_password"}
	response = api_client.post("auth", json=payload)

	# restful–booker 'll return 200 even with bad credentials 
	# but in the body 'll returns {"reason": "Bad credentials"}
	assert response.status_code == 200
	assert response.json().get("reason") == "Bad credentials"