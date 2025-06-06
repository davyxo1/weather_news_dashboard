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
    articles = data.get("articles", [])

    # Si no hay noticias, hacer búsqueda alternativa
    if not articles:
        print("⚠️ No se encontraron titulares. Usando búsqueda alternativa por palabra clave.")
        return buscar_noticias("Chile", max_noticias)

    noticias = []
    for article in articles[:max_noticias]:
        noticias.append({
            "titulo": article["title"],
            "fuente": article["source"]["name"],
            "url": article["url"]
        })

    return noticias

def buscar_noticias(query="Chile", max_noticias=5):
    url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&language=es&apiKey={NEWS_API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Error en búsqueda de noticias: {response.status_code} - {response.text}")

    data = response.json()
    articles = data.get("articles", [])

    noticias = []
    for article in articles[:max_noticias]:
        noticias.append({
            "titulo": article["title"],
            "fuente": article["source"]["name"],
            "url": article["url"]
        })

    return noticias