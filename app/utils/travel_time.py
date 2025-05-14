from datetime import datetime, timedelta
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TRAVELTIME_APP_ID = os.getenv("TRAVELTIME_APP_ID")
TRAVELTIME_API_KEY = os.getenv("TRAVELTIME_API_KEY")

def get_eta_from_traveltime(bus_lat: float, bus_lon: float, stop_lat: float, stop_lon: float, mode="driving"):

    now = datetime.now()

    url = "https://api.traveltimeapp.com/v4/time-filter"

    headers = {
        "X-Application-Id": TRAVELTIME_APP_ID,
        "X-Api-Key": TRAVELTIME_API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "locations": [
            {
                "id": "bus",
                "coords": { "lat": bus_lat, "lng": bus_lon }
            },
            {
                "id": "stop",
                "coords": { "lat": stop_lat, "lng": stop_lon }
            }
        ],
        "departure_searches": [
            {
                "id": "bus_to_stop",
                "departure_location_id": "bus",
                "arrival_location_ids": ["stop"],
                "transportation": { "type": mode },
                "departure_time": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "travel_time": 1800,
                "properties": ["travel_time", "distance"]
            }
        ]
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()

        travel_time_seconds = result["results"][0]["locations"][0]["properties"][0]["travel_time"]
        travel_time_minutes = round((timedelta(seconds=travel_time_seconds).total_seconds() / 60), 2)

        return travel_time_minutes
    except Exception as e:
        print(f"Erro ao consultar TravelTime (NORMAL): {e}")
        print(f"Resposta completa: {response.text}")
        return None
