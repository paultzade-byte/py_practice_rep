# schemas/booking.py

from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

# submodel for booking dates
class BookingDates(BaseModel):
	checkin: date
	checkout: date 

# main model of Booking object (used in GET, POST, PUT)
class BookingModel(BaseModel):
	firstname: str
	lastname: str
	totalprice: int
	depositpaid: bool 
	bookingdates: BookingDates 
	additionalneeds: Optional[str] = Field(default=None) # not mandatory

# response model when POST /booking
class CreateBookingResponse(BaseModel):
	bookingid: int 
	booking: BookingModel

# response model when POST /auth
class AuthResponse(BaseModel):
	token: str