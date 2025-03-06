import requests

class ServerComm:
    def __init__(self, base_url="http://localhost:8000", api_key=None):
        self.base_url = base_url
        self.headers = {"X-API-Key": api_key} if api_key else {}

    def send_gps(self, device_id, latitude, longitude):
        data = {
            "device_id": device_id,
            "latitude": latitude,
            "longitude": longitude
        }
        try:
            response = requests.post(f"{self.base_url}/api/locations/", json=data, headers=self.headers)
            print(f"GPS Request: Status {response.status_code}, Response: {response.text}")
            return response.status_code == 201
        except requests.RequestException as e:
            print(f"Server error: {e}")
            return False
        
    def send_chat(self, device_id, message):
        data = {
            "device_id": device_id,
            "message": message
        }
        try:
            response = requests.post(f"{self.base_url}/api/chat/", json=data, headers=self.headers)
            return response.status_code == 201
        except requests.RequestException as e:
            print(f"Server error: {e}")
            return False