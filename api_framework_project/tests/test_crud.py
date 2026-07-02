# tests/test_crud.py

import pytest
from datetime import date
from services.booker_service import BookerServices

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
    
    # Pydantic автоматично перетворив рядки дат на об'єкти datetime.date
    assert fetched_booking.bookingdates.checkin == date(2026, 7, 1)
    assert fetched_booking.lastname == "Doe"