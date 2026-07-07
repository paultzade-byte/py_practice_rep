# services/booker_service.py

from core.endpoints import Endpoints
from schemas.booking import AuthResponse, CreateBookingResponse, BookingModel

class BookerServices:
	def __init__(self, client):
		self.client = client # BaseAPIClient

	def create_token(self, username: str, password: str) -> str:
		payload = {
			"username": username,
			"password": password
		}

		response = self.client.post(Endpoints.AUTH, json=payload)
		
		# response validation by schemas.booking module
		validated_data = AuthResponse.model_validate(response.json())
		return validated_data.token

	def create_booking(self, booking_data: dict) -> CreateBookingResponse:
		response = self.client.post(Endpoints.BOOKING, json=booking_data)
		# in case API returns invalid data then test fail here with detailed Error
		return CreateBookingResponse.model_validate(response.json())

	def get_booking(self, booking_id: int) -> BookingModel:
		# formatting URL with/from ID
		endpoint = Endpoints.BOOKING_DETAIL.format(id=booking_id)
		response = self.client.get(endpoint)

		return BookingModel.model_validate(response.json())

	def delete_booking(self, booking_id: int, token: str):
		# specific restful-booker header
		headers = {
			"Cookie": f"token={token}"
		}
		response = self.client.delete(f"booking/{booking_id}", headers=headers)
		return response