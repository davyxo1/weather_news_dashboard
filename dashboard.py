import json
from datetime import datetime
from weather_service import get_weather
from news_service import get_news
from country_service import get_country_info

def obtener_icono_climatico(descripcion):
    desc = descripcion.lower()
    if "lluvia" in desc:
        return "🌧️"
    elif "nieve" in desc:
        return "❄️"
    elif "tormenta" in desc:
        return "⛈️"
    elif "nublado" in desc:
        return "☁️"
    elif "soleado" in desc or "despejado" in desc:
        return "☀️"
    elif "niebla" in desc:
        return "🌫️"
    else:
        return "🌤️"

def correlacionar_noticias_con_clima(noticias, clima_descripcion):
    clima_keywords = clima_descripcion.lower().split()
    relacionadas = []

    for noticia in noticias:
        titulo = noticia.get("titulo", "").lower()
        if any(palabra in titulo for palabra in clima_keywords):
            relacionadas.append(noticia)

    return relacionadas

def generar_reporte(country_code="cl", ciudad="La Serena"):
    # Obtener información
    clima = get_weather(ciudad)
    pais_info = get_country_info(country_code)
    noticias = get_news(country_code)
    icono_clima = obtener_icono_climatico(clima["descripcion"])
    relacionadas = correlacionar_noticias_con_clima(noticias, clima["descripcion"])

    # Mostrar en consola
    print("\n===== DASHBOARD DEL DÍA =====")
    print(f"🌍 País: {pais_info['nombre']} | Ciudad: {ciudad}")
    print(f"{icono_clima} Clima: {clima['descripcion'].capitalize()} | Temp: {clima['temperatura']}°C\n")
    print("📰 Principales noticias:")
    for i, noticia in enumerate(noticias[:5], 1):
        print(f"{i}. {noticia['titulo']}")
        print(f"   Fuente: {noticia['fuente']}")
        print(f"   URL: {noticia['url']}\n")

    if relacionadas:
        print("🔗 Noticias relacionadas con el clima:")
        for r in relacionadas:
            print(f"- {r['titulo']}")

    # Guardar en JSON
    reporte = {
        "fecha": datetime.now().isoformat(),
        "pais": pais_info["nombre"],
        "ciudad": ciudad,
        "clima": clima,
        "noticias": noticias[:5],
        "noticias_relacionadas_con_clima": relacionadas
    }

    with open("reporte_diario.json", "w", encoding="utf-8") as f:
        json.dump(reporte, f, ensure_ascii=False, indent=4)

    # Guardar en texto plano
    with open("reporte_diario.txt", "w", encoding="utf-8") as f:
        f.write(f"Reporte Diario - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"País: {pais_info['nombre']} | Ciudad: {ciudad}\n")
        f.write(f"Clima: {clima['descripcion'].capitalize()} | Temp: {clima['temperatura']}°C\n\n")
        f.write("Principales noticias:\n")
        for i, noticia in enumerate(noticias[:5], 1):
            f.write(f"{i}. {noticia['titulo']} ({noticia['fuente']})\n")
            f.write(f"   URL: {noticia['url']}\n\n")
        if relacionadas:
            f.write("Noticias relacionadas con el clima:\n")
            for r in relacionadas:
                f.write(f"- {r['titulo']}\n")

    print("✅ Reportes guardados en 'reporte_diario.json' y 'reporte_diario.txt'")