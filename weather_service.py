import requests
from config import WEATHER_API_KEY

def get_weather(city):
    if not city:
        raise ValueError("Debe proporcionar una ciudad.")

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=es"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Error en la API del clima: {response.status_code} - {response.text}")

    data = response.json()

    return {
        "ciudad": data.get("name"),
        "descripcion": data["weather"][0]["description"],
        "temperatura": data["main"]["temp"],
        "humedad": data["main"]["humidity"],
        "viento_kmh": data["wind"]["speed"] * 3.6  # m/s a km/h
    }