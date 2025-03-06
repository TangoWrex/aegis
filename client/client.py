# client/client.py
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
    server = ServerComm(base_url="http://localhost:8000", api_key=api_key)
    device_id = "test_device"

    # Interactive chat input
    print("Chat room active. Type a message and press Enter to send (or 'quit' to exit).")
    while True:
        message = input(f"[{device_id}] You: ")
        if message.lower() == 'quit':
            break
        if message.strip():
            server.send_chat(device_id, message)  # Send only the message
            print(f"[{device_id}] Sent: {message}")

        lat, lon = gps.get_position()
        if lat and lon:
            success = server.send_gps(device_id, lat, lon)
            print(f"Sent GPS: {{lat: {lat}, lon: {lon}}}, Success: {success}")
        else:
            print("No GPS fix yet")
        time.sleep(1)

if __name__ == "__main__":
    main()