import requests
from config import NEWS_API_KEY

def get_news(country_code="cl", category="general", max_noticias=5):
    url = (
        f"https://newsapi.org/v2/top-headlines?"
        f"country={country_code}&category={category}&apiKey={NEWS_API_KEY}"
    )

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Error en la API de noticias: {response.status_code} - {response.text}")

    data = response.json()

    noticias = []
    for article in data.get("articles", [])[:max_noticias]:
        noticias.append({
            "titulo": article["title"],
            "fuente": article["source"]["name"],
            "url": article["url"]
        })

    return noticias