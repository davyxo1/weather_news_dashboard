import threading
from datetime import datetime, timedelta
import time
import json
from dashboard import generar_reporte
from gmail_service import enviar_correo

def calcular_proximo_lunes_8am():
    ahora = datetime.now()
    # Día de la semana: lunes es 0, domingo es 6
    dias_hasta_lunes = (0 - ahora.weekday()) % 7
    proximo_lunes = ahora + timedelta(days=dias_hasta_lunes)
    proximo_lunes_8am = proximo_lunes.replace(hour=8, minute=0, second=0, microsecond=0)

    # Si ya pasó el lunes a las 8am de esta semana, pasa al siguiente lunes
    if proximo_lunes_8am <= ahora:
        proximo_lunes_8am += timedelta(days=7)

    return proximo_lunes_8am

def esperar_y_enviar_cada_lunes(destinatario, pais, ciudad, callback_estado=None):
    def tarea():
        while True:
            proximo_envio = calcular_proximo_lunes_8am()
            ahora = datetime.now()
            segundos_espera = (proximo_envio - ahora).total_seconds()

            if callback_estado:
                callback_estado(f"⌛ Próximo correo programado: {proximo_envio.strftime('%Y-%m-%d %H:%M')}", "blue")

            # Esperar hasta el próximo lunes a las 8am
            time.sleep(segundos_espera)

            if callback_estado:
                callback_estado("📨 Enviando correo programado...", "blue")

            try:
                generar_reporte(pais, ciudad)
                with open("reporte_diario.json", "r", encoding="utf-8") as f:
                    reporte = json.load(f)

                fecha = reporte.get("fecha", "")
                pais = reporte.get("pais", "")
                ciudad = reporte.get("ciudad", "")
                clima = reporte.get("clima", {})
                temp = f"{clima.get('temperatura', '')}°C" if clima else ""
                descripcion_clima = clima.get("descripcion", "")
                noticias = reporte.get("noticias", [])

                enviar_correo(destinatario, fecha, pais, ciudad, descripcion_clima, temp, noticias)

                if callback_estado:
                    callback_estado("✅ Correo programado enviado con éxito.", "green")
            except Exception as e:
                if callback_estado:
                    callback_estado(f"❌ Error en envío programado: {e}", "red")

            # Esperar 60 segundos antes de calcular la próxima fecha para evitar ciclos rápidos si algo falla
            time.sleep(60)

    hilo = threading.Thread(target=tarea, daemon=True)
    hilo.start()
