import os
import requests
from dotenv import load_dotenv

load_dotenv()

RAPID_API_KEY = os.getenv("RAPID_API_KEY")
WEATHER_HOST = os.getenv("WEATHER_API")
BASE_URL = f"https://api.weatherapi.com/v1/current.json?key={WEATHER_HOST}&q="

def get_weather(place: str) -> dict:
    """Fetch current weather data for a given place using RapidAPI."""
    print("getting weather for ", place)
    
    response = requests.get(f"{BASE_URL}{place}")
    print(f"{BASE_URL}{place}")
    print(response.text)
    
    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        return {"error": response.text}

def format_weather(data: dict) -> str:
    try:
        location = data.get("location", {})
        current = data.get("current", {})

        name = location.get("name", "Unknown")
        region = location.get("region", "")
        country = location.get("country", "")
        localtime = location.get("localtime", "N/A")

        condition = current.get("condition", {}).get("text", "No description").capitalize()
        temp_c = current.get("temp_c", "N/A")
        feels_like_c = current.get("feelslike_c", "N/A")
        humidity = current.get("humidity", "N/A")
        wind_speed = current.get("wind_kph", "N/A")
        wind_dir = current.get("wind_dir", "N/A")
        clouds = current.get("cloud", "N/A")
        visibility = current.get("vis_km", "N/A")
        uv = current.get("uv", "N/A")

        weather_report = (
            f"🌍 Location: {name}, {region}, {country}\n"
            f"🕒 Local Time: {localtime}\n"
            f"⛅ Condition: {condition}\n"
            f"🌡️ Temperature: {temp_c}°C (Feels like {feels_like_c}°C)\n"
            f"💧 Humidity: {humidity}%\n"
            f"🌬️ Wind: {wind_speed} kph from {wind_dir}\n"
            f"☁️ Cloudiness: {clouds}%\n"
            f"👁️ Visibility: {visibility} km\n"
            f"🌞 UV Index: {uv}\n"
        )

        return weather_report

    except Exception as e:
        return f"⚠️ Error formatting weather: {str(e)}"
