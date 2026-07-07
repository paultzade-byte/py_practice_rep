# tests/test_crud.py

from datetime import date
from schemas.booking import BookingModel as BM
def test_create_and_get_booking(booker_service):
    # 1. preparing test data
    payload = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-07-01",
            "checkout": "2026-07-10"
        },
        "additionalneeds": "Breakfast"
    }

    # 2. creating booking
    created_booking = booker_service.create_booking(payload)
    
    # Object type checking 
    assert created_booking.bookingid > 0
    assert created_booking.booking.firstname == "John"
    
    # 3. GET request for persistent check
    fetched_booking = booker_service.get_booking(created_booking.bookingid)
    
    # Pydantic automatically translated strings to objects datetime.date
    assert fetched_booking.bookingdates.checkin == date(2026, 7, 1)
    assert fetched_booking.lastname == "Doe"

def test_delete_booking(booker_service, api_client, temp_booking_id, auth_token):
    delete_response = booker_service.delete_booking(temp_booking_id, auth_token)
    # Restful-booker returns 201 for deleted data
    assert delete_response.status_code == 201

    # check if data actually deleted
    check_deleted_response = api_client.get(f"booking/{temp_booking_id}")
    assert check_deleted_response.status_code == 404
    assert check_deleted_response.text == "Not Found"

def update_booking(self, booking_id, payload):
    # PUT
    response = self.api_client.put(f"booking/{booking_id}", json=payload)
    return BM(**response.json()) # validation by Pydantic

def partial_update_booking(self, booking_id, payload):
    # PATCH
    response = self.api_client.patch(f"booking/{booking_id}", json=payload)
    return BM(**response.json())