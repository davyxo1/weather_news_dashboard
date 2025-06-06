from news_service import get_news

noticias = get_news()
for noticia in noticias:
    print(noticia)