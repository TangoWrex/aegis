# client/server_comm.py
import requests
import json
from datetime import datetime

class ServerComm:
    def __init__(self, base_url="http://localhost:8000", api_key=None):
        self.base_url = base_url
        self.headers = {"X-API-Key": api_key} if api_key else {}

    def send_packet(self, device_id, packet_type, data):
        packet = {
            "type": packet_type,
            "device_id": device_id,
            "api_key": self.headers.get("X-API-Key"),
            "data": data,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        try:
            response = requests.post(f"{self.base_url}/api/packet/", json=packet, headers=self.headers)
            print(f"Packet Request: Status {response.status_code}, Response: {response.text}")
            return response.status_code == 201
        except requests.RequestException as e:
            print(f"Server error: {e}")
            return False

    def send_gps(self, device_id, latitude, longitude):
        data = {"latitude": latitude, "longitude": longitude}
        return self.send_packet(device_id, "gps", data)

    def send_chat(self, device_id, message):
        data = {"message": message}
        return self.send_packet(device_id, "chat", data)