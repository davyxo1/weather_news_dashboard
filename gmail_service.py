import smtplib
from email.message import EmailMessage

def crear_cuerpo_correo(fecha, pais, ciudad, clima, temp, noticias):
    cuerpo = f"""\
🌤️ Reporte Diario — {fecha}

📍 País: {pais}  
🏙️ Ciudad: {ciudad}

🌡️ Clima: {clima}  
🌡️ Temperatura: {temp}°C

---

📰 Principales Noticias:
"""
    for i, noticia in enumerate(noticias, 1):
        titulo = noticia['titulo']
        fuente = noticia['fuente']
        url = noticia['url']
        cuerpo += f"{i}. {titulo} ({fuente})\n   🔗 {url}\n\n"

    return cuerpo


def enviar_correo(destinatario, fecha, pais, ciudad, clima, temp, noticias):
    remitente = "tucorreo@gmail.com"
    contraseña = "tu_contraseña_de_app"  # Usa una contraseña de aplicación de Gmail

    # Crear el mensaje
    mensaje = EmailMessage()
    mensaje['Subject'] = f"🌍 Reporte Diario - {fecha}"
    mensaje['From'] = remitente
    mensaje['To'] = destinatario

    # Crear el cuerpo del mensaje
    cuerpo = crear_cuerpo_correo(fecha, pais, ciudad, clima, temp, noticias)
    mensaje.set_content(cuerpo)

    # Enviar el correo
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(remitente, contraseña)
            smtp.send_message(mensaje)
        print("✅ Correo enviado correctamente.")
    except Exception as e:
        print(f"❌ Error al enviar el correo: {e}")