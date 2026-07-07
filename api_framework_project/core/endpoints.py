# core/endpoints.py

from dataclasses import dataclass

# attention! "overkill"
@dataclass(frozen=True)
class Endpoints:
	AUTH: str = "/auth"
	BOOKING: str = "/booking"
	BOOKING_DETAIL: str = "/booking/{id}"
