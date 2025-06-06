# Weather News Dashboard

## 🌦️ Descripción

`weather_news_dashboard` es una aplicación en Python que unifica datos **meteorológicos** y **noticias relevantes** para un país ingresado por el usuario, generando un **reporte diario** completo. Este informe se imprime por consola, se guarda como archivo `.json` y `.txt`, y ofrece una correlación contextual entre el estado del clima y los titulares del día.

---

## ⚙️ Funcionalidades

- Consulta el **clima actual** de la capital de un país mediante OpenWeatherMap.
- Obtiene **las noticias más importantes del país** desde NewsAPI.
- Realiza una correlación inteligente entre el estado del tiempo y las noticias.
- Genera un **reporte diario combinado** de clima + noticias.
- Exporta el reporte a archivos en **formato JSON y texto plano**.
- Interfaz simple y directa vía **línea de comandos (CLI)**.

---

## 🧰 Requisitos

- **Python 3.7 o superior**
- Librerías necesarias:
  - `requests`
  - `python-dotenv`
- Claves API requeridas:
  - [OpenWeatherMap API Key](https://openweathermap.org/api)
  - [NewsAPI Key](https://newsapi.org/)

### Variables de entorno (.env):

```env
OPENWEATHERMAP_API_KEY=tu_api_key_aqui
NEWS_API_KEY=tu_api_key_aqui