import os
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

if not WEATHER_API_KEY:
    raise ValueError("Falta configurar WEATHER_API_KEY en el archivo .env")

if not NEWS_API_KEY:
    raise ValueError("Falta configurar NEWS_API_KEY en el archivo .env")

if not EMAIL_USER or not EMAIL_PASS:
    raise ValueError("Faltan credenciales de correo (EMAIL_USER o EMAIL_PASS) en el archivo .env")