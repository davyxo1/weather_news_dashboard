import requests
from config import NEWS_API_KEY

def get_news(country_code="cl", category="general", max_noticias=5):
    # Paso 1: Buscar titulares principales (top-headlines)
    url_top = (
        f"https://newsapi.org/v2/top-headlines?"
        f"country={country_code}&category={category}&language=es&apiKey={NEWS_API_KEY}"
    )

    response_top = requests.get(url_top)

    if response_top.status_code != 200:
        raise Exception(f"Error en la API de titulares: {response_top.status_code} - {response_top.text}")

    data_top = response_top.json()
    articles_top = data_top.get("articles", [])

    if articles_top:
        return [
            {
                "titulo": article["title"],
                "fuente": article["source"]["name"],
                "url": article["url"]
            }
            for article in articles_top[:max_noticias]
        ]
    
    # Paso 2: Si no hay titulares, usar búsqueda alternativa (everything)
    print("⚠️ No se encontraron titulares. Usando búsqueda alternativa por palabra clave.")
    return buscar_noticias("Chile", max_noticias)


def buscar_noticias(query="Chile", max_noticias=5):
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={query}&sortBy=publishedAt&language=es&apiKey={NEWS_API_KEY}"
    )

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Error en búsqueda de noticias: {response.status_code} - {response.text}")

    data = response.json()
    articles = data.get("articles", [])

    return [
        {
            "titulo": article["title"],
            "fuente": article["source"]["name"],
            "url": article["url"]
        }
        for article in articles[:max_noticias]
    ]
