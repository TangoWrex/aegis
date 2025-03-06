#!/usr/bin/env python3
import os
from gps_client import GPSClient
from server_comm import ServerComm
import time

def main():
    gps = GPSClient()
    api_key = os.getenv("AEGIS_API_KEY")
    if not api_key:
        raise ValueError("AEGIS_API_KEY environment variable not set")
    server = ServerComm(base_url="http://localhost:8000", api_key=api_key)  # Localhost since server is on same host
    device_id = "test_device"

    server.send_chat(device_id, "Hello from test_device!")
    while True:
        lat, lon = gps.get_position()
        if lat and lon:
            success = server.send_gps(device_id, lat, lon)
            print(f"Sent: {{lat: {lat}, lon: {lon}}}, Success: {success}")
        else:
            print("No GPS fix yet")
        time.sleep(1)

if __name__ == "__main__":
    main()