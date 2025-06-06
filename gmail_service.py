import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()  # Carga las variables del archivo .env

def crear_cuerpo_correo(fecha, pais, ciudad, clima, temp, noticias):
    cuerpo = f"""Reporte Diario — {fecha}

Pais: {pais}
Ciudad: {ciudad}
Clima: {clima}
Temperatura: {temp}°C

Noticias principales:
"""
    for i, noticia in enumerate(noticias, 1):
        cuerpo += f"{i}. {noticia['titulo']} ({noticia['fuente']})\n   {noticia['url']}\n\n"

    return cuerpo

def enviar_correo(destinatario, fecha, pais, ciudad, clima, temp, noticias):
    remitente = os.getenv("EMAIL_USER")
    contrasena = os.getenv("EMAIL_PASS")

    mensaje = EmailMessage()
    mensaje["Subject"] = f"Reporte Diario - {fecha}"
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje.set_content(crear_cuerpo_correo(fecha, pais, ciudad, clima, temp, noticias))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(remitente, contrasena)
            smtp.send_message(mensaje)
        print("✅ Correo enviado correctamente.")
    except Exception as e:
        print(f"❌ Error al enviar el correo: {e}")
