import time
import datetime
import threading
import json
import re  # Importamos todo el módulo re correctamente
from dashboard import generar_reporte
from gmail_service import enviar_correo

CONFIG_FILE = "config_envio.json"

def cargar_configuracion():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ No se pudo leer la configuración: {e}")
        return None

def envio_automatico():
    while True:
        config = cargar_configuracion()
        if not config:
            time.sleep(60)
            continue

        hora_actual = datetime.datetime.now().time()
        hora_objetivo = datetime.time(
            int(config["hora"]), int(config["minuto"])
        )

        if (
            hora_actual.hour == hora_objetivo.hour
            and hora_actual.minute == hora_objetivo.minute
        ):
            try:
                print("⏰ Enviando correo automático diario...")

                generar_reporte(config["pais"], config["ciudad"])

                with open("reporte_diario.txt", "r", encoding="utf-8") as f:
                    contenido = f.read()

                asunto = f"Reporte Diario - {datetime.datetime.now().strftime('%Y-%m-%d')}"

                cuerpo = contenido

                enviar_correo(
                    destinatario=config["correo"],
                    asunto=asunto,
                    mensaje=cuerpo
                )

                print("✅ Correo automático enviado.")
                time.sleep(61)  # esperar más de 1 minuto para evitar envíos dobles
            except Exception as e:
                print(f"❌ Error en envío automático: {e}")
        else:
            time.sleep(20)

def iniciar_programador():
    hilo = threading.Thread(target=envio_automatico, daemon=True)
    hilo.start()
