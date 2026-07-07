
def test_auth_invalid_credentials(api_client):
	# directly using base client
	# because the create_token method 'll fail with ValidationError (it 'll not find "token" field)
	payload = {"username": "admin", "password": "wrong_password"}
	response = api_client.post("auth", json=payload)

	# restful–booker 'll return 200 even with bad credentials
	# but in the body 'll return {"reason": "Bad credentials"}
	assert response.status_code == 200
	assert response.json().get("reason") == "Bad credentials"


def test_auth_invalid_endpoint(api_client):
    payload = {
        "username": "admin",
        "password": "password123"
    }

    response = api_client.post("auto", json=payload)

    assert response.status_code == 404
    assert response.text == "Not Found"


def test_auth_missing_password(api_client):
    payload = {"username": "admin"}
    response = api_client.post("auth", json=payload)

    assert response.status_code == 200
    assert response.json().get("reason") == "Bad credentials"


def test_create_booking_without_name(api_client):
    # 1. preparing test data
    payload = {
        "lastname": "Doe",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-07-01",
            "checkout": "2026-07-10"
        }
    }

    response = api_client.post("booking", json=payload)
    assert response.status_code == 500
    assert response.text == "Internal Server Error"
