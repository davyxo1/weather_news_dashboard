import requests

PAISES = {
    "cl": "Chile",
    "ar": "Argentina",
    "mx": "México",
    "us": "Estados Unidos",
    "co": "Colombia",
    "br": "Brasil"
}

def get_country_name(code):
    return PAISES.get(code.lower(), "Desconocido")

def get_country_info(code="cl"):
    nombre = get_country_name(code)
    url = f"https://restcountries.com/v3.1/name/{nombre}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Error al obtener datos del país: {response.status_code}")

    datos = response.json()[0]

    return {
        "nombre": datos["name"]["common"],
        "capital": datos["capital"][0],
        "poblacion": datos["population"],
        "moneda": list(datos["currencies"].keys())[0]
    }

if __name__ == "__main__":
    try:
        info = get_country_info("cl")
        for clave, valor in info.items():
            print(f"{clave.capitalize()}: {valor}")
    except Exception as e:
        print("❌ Error:", e)