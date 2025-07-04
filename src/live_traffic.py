import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY")

def get_live_congestion(lat, lon):
    url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/relative0/10/json"
    params ={
        "point" : f"{lat},{lon}",
        "unit": "KMPH",
        "key" : TOMTOM_API_KEY
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()['flowSegmentData']
            free = data['freeFlowSpeed']
            current = data['currentSpeed']

            if current == 0: return 10.0
            return round(free/current, 2)

        else:
            print("API error", response.status_code)
            return 1   
        
    except Exception as e:
        print("An error occurred:", e)
        return 1
