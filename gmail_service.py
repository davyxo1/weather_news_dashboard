import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_USER, EMAIL_PASS

def enviar_correo(destinatario, contenido):
    if not EMAIL_USER or not EMAIL_PASS:
        raise ValueError("❌ EMAIL_USER o EMAIL_PASS no están definidos. Verifica tu archivo .env.")

    if not contenido or not destinatario:
        raise ValueError("❌ El contenido o el destinatario están vacíos.")

    asunto = "📬 Reporte Automático - Clima y Noticias"

    mensaje = MIMEMultipart()
    mensaje["From"] = EMAIL_USER
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto

    cuerpo = MIMEText(contenido, "plain", "utf-8")
    mensaje.attach(cuerpo)

    try:
        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(EMAIL_USER, EMAIL_PASS)
        servidor.sendmail(EMAIL_USER, destinatario, mensaje.as_string())
        servidor.quit()
        print(f"✅ Correo enviado exitosamente a {destinatario}")
    except Exception as e:
        print(f"❌ Error al enviar el correo: {e}")
        raise