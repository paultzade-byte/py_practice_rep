# core/base_client.py

import requests

class BaseAPIClient:
	def __init__(self, base_url: str):

		self.base_url = base_url
		self.session = requests.Session()

	def _request(self, method: str, endpoint: str, **kwargs):
		url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

		try:
			response = self.session.request(method, url, **kwargs)
			response.raise_for_status()
			return response
		except requests.exceptions.HTTPError as e:
			print(f"API Error [{method}] {url}: {e.response.status_code}")
			print(f"Server response: {e.response.text}")

	def get(self, endpoint: str, **kwargs):
		return self._request("GET", endpoint, **kwargs)

	def post(self, endpoint: str, **kwargs):
		return self._request("POST", endpoint, **kwargs)

	def put(self, endpoint: str, **kwargs):
		return self._request("PUT", endpoint, **kwargs)

	def delete(self, endpoint: str, **kwargs):
		return self._request("DELETE", endpoint, **kwargs)
			
	def close(self):
		self.session.close()

		# handling context manager 'with' 
		#in case BaseAPIClient called by 'with' context will be closed automatically
	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.close()