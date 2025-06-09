import threading
from datetime import datetime, timedelta
import time
import json
from dashboard import generar_reporte
from gmail_service import enviar_correo

# NUEVO: función de prueba para enviar en 1 minuto
def calcular_proxima_ejecucion_prueba():
    return datetime.now() + timedelta(minutes=1)

def esperar_y_enviar_cada_minuto_prueba(destinatario, pais, ciudad, callback_estado=None):
    def tarea():
        while True:
            proximo_envio = calcular_proxima_ejecucion_prueba()
            ahora = datetime.now()
            segundos_espera = (proximo_envio - ahora).total_seconds()

            if callback_estado:
                callback_estado(f"⌛ Envío de prueba programado para {proximo_envio.strftime('%Y-%m-%d %H:%M:%S')}", "blue")

            time.sleep(segundos_espera)

            if callback_estado:
                callback_estado("📨 Enviando correo de prueba...", "blue")

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
                    callback_estado(f"✅ Correo de prueba enviado el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "green")
            except Exception as e:
                if callback_estado:
                    callback_estado(f"❌ Error en envío de prueba: {e}", "red")

            # NUEVO: espera solo 1 minuto para repetir (repetición rápida)
            time.sleep(60)

    print("🕒 Programador de prueba iniciado...")
    hilo = threading.Thread(target=tarea, daemon=True)
    hilo.start()
