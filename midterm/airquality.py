import requests
import json

def get_air_quality(lat, long, api_key) :
    """
    Get the live air quality of a place 
    """
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={long}&appid={api_key}"
    response = requests.get(url)
    data = response.json()

    return data["list"][0]["main"]["aqi"] if data["list"][0]["main"]["aqi"] else None