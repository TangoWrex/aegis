#!/usr/bin/env python3
import gpsd
import time

class GPSClient:
    def __init__(self):
        gpsd.connect()

    def get_position(self):
        try:
            packet = gpsd.get_current()
            latitude = packet.lat
            longitude = packet.lon
            if latitude is not None and longitude is not None:
                return latitude, longitude
            return None, None
        except (gpsd.NoFixError, AttributeError):
            return None, None

def run_gps():
    gps = GPSClient()
    while True:
        lat, lon = gps.get_position()
        if lat and lon:
            print(f"Lat: {lat}, Lon: {lon}")
        else:
            print("No fix—waiting for GPS data")
        time.sleep(1)

if __name__ == "__main__":
    run_gps()