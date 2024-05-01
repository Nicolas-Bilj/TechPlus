import requests
import json

def get_air_quality(lat, long, api_key):
    """
    Get the air quality index of a location using the OpenWeatherMap Air Pollution API.

    Parameters:
        lat (float): The latitude of the location.
        long (float): The longitude of the location.
        api_key (str): The API key for OpenWeatherMap.

    Returns:
        int: The air quality index of the location.
    """
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={long}&appid={api_key}"
    response = requests.get(url)
    data = response.json()

    return data["list"][0]["main"]["aqi"] if data["list"][0]["main"]["aqi"] else None