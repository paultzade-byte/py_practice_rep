# tests/test_auth.py


def test_auth_success(booker_service):
	# using service which validate response through Pydantic
	token = booker_service.create_token(username="admin", password="password123")

	assert token is not None
	assert isinstance(token, str)
	assert len(token) > 0

