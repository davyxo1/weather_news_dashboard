import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

def crear_cuerpo_html(fecha, pais, ciudad, clima, temp, noticias):
    cuerpo = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <h2 style="color: #2E86C1;">🌎 Reporte Diario — {fecha}</h2>
        <p><strong>País:</strong> {pais}<br>
        <strong>Ciudad:</strong> {ciudad}<br>
        <strong>Clima:</strong> {clima}<br>
        <strong>Temperatura:</strong> {temp}°C</p>
        <hr>
        <h3 style="color: #2E86C1;">📰 Noticias principales:</h3>
        <ul>
    """
    for noticia in noticias:
        cuerpo += f"""<li>
            <strong>{noticia['titulo']}</strong> <em>({noticia['fuente']})</em><br>
            <a href="{noticia['url']}" target="_blank">Leer más</a>
        </li><br>"""

    cuerpo += """
        </ul>
    </body>
    </html>
    """
    return cuerpo

def enviar_correo(destinatario, fecha, pais, ciudad, clima, temp, noticias):
    remitente = os.getenv("EMAIL_USER")
    contrasena = os.getenv("EMAIL_PASS")

    mensaje = EmailMessage()
    mensaje["Subject"] = f"Reporte Diario - {fecha}"
    mensaje["From"] = remitente
    mensaje["To"] = destinatario

    cuerpo_html = crear_cuerpo_html(fecha, pais, ciudad, clima, temp, noticias)
    mensaje.add_alternative(cuerpo_html, subtype="html")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(remitente, contrasena)
            smtp.send_message(mensaje)
        print("✅ Correo enviado correctamente.")
    except Exception as e:
        print(f"❌ Error al enviar el correo: {e}")
