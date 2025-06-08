import threading
from datetime import datetime, timedelta
import time
import json
from dashboard import generar_reporte
from gmail_service import enviar_correo

def calcular_proximo_lunes_8am():
    ahora = datetime.now()
    dias_hasta_lunes = (0 - ahora.weekday()) % 7
    proximo_lunes = ahora + timedelta(days=dias_hasta_lunes)
    proximo_lunes_8am = proximo_lunes.replace(hour=8, minute=0, second=0, microsecond=0)

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
                callback_estado(f"⌛ Próximo correo programado para el {proximo_envio.strftime('%Y-%m-%d %H:%M')}", "blue")

            time.sleep(segundos_espera)

            if callback_estado:
                callback_estado("📨 Enviando correo programado...", "blue")

            try:
                generar_reporte(pais, ciudad)
                with open("reporte_diario.json", "r", encoding="utf-8") as f:
                    reporte = json.load(f)

                fecha = reporte.get("fecha", "")
                pais_r = reporte.get("pais", "")
                ciudad_r = reporte.get("ciudad", "")
                clima = reporte.get("clima", {})
                temp = f"{clima.get('temperatura', '')}°C" if clima else ""
                descripcion_clima = clima.get("descripcion", "")
                noticias = reporte.get("noticias", [])

                enviar_correo(destinatario, fecha, pais_r, ciudad_r, descripcion_clima, temp, noticias)

                if callback_estado:
                    callback_estado(f"✅ Correo enviado el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "green")
            except Exception as e:
                if callback_estado:
                    callback_estado(f"❌ Error en envío programado: {e}", "red")

            time.sleep(60)

    hilo = threading.Thread(target=tarea, daemon=True)
    hilo.start()
