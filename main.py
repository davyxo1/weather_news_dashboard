import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import threading
import time
import os
import re

from dashboard import generar_reporte
from gmail_service import enviar_correo

def validar_correo(correo):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, correo) is not None

def enviar_reporte(pais, ciudad, correo, tipo_envio, valor_extra, estado_label):
    try:
        generar_reporte(pais, ciudad)

        if not os.path.exists("reporte_diario.txt"):
            estado_label.config(text="❌ No se encontró reporte_diario.txt")
            return

        with open("reporte_diario.txt", "r", encoding="utf-8") as f:
            reporte = f.read()

        if tipo_envio == "Ahora":
            delay = 0
        elif tipo_envio == "En X minutos":
            try:
                minutos = int(valor_extra)
                delay = minutos * 60
            except ValueError:
                estado_label.config(text="❌ Minutos inválidos.")
                return
        elif tipo_envio == "Fecha específica":
            try:
                fecha_obj = datetime.strptime(valor_extra, "%d-%m-%Y %H:%M")
                delay = (fecha_obj - datetime.now()).total_seconds()
                if delay < 0:
                    estado_label.config(text="❌ Fecha ya pasó.")
                    return
            except ValueError:
                estado_label.config(text="❌ Formato de fecha inválido.")
                return
        else:
            estado_label.config(text="❌ Tipo de envío no reconocido.")
            return

        def tarea_envio():
            if delay > 0:
                estado_label.config(text=f"⏳ Esperando {round(delay / 60, 2)} minutos...")
                time.sleep(delay)

            estado_label.config(text="📨 Enviando correo...")
            try:
                enviar_correo(correo, reporte)
                estado_label.config(text="✅ Correo enviado con éxito.")
            except Exception as e:
                if "535" in str(e):
                    estado_label.config(text="❌ Error de autenticación SMTP. Revisa EMAIL_USER y EMAIL_PASS.")
                elif "10060" in str(e):
                    estado_label.config(text="❌ No se pudo conectar al servidor SMTP. Revisa tu red o firewall.")
                else:
                    estado_label.config(text=f"❌ Error al enviar el correo: {e}")

        threading.Thread(target=tarea_envio, daemon=True).start()

    except Exception as e:
        estado_label.config(text=f"❌ Error general: {e}")

def iniciar_interfaz():
    root = tk.Tk()
    root.title("📧 Envío de Reporte Climático y de Noticias")
    root.geometry("500x430")
    root.resizable(False, False)

    fuente = ("Segoe UI", 10)

    ttk.Label(root, text="🌍 Código del país (ej: cl):", font=fuente).pack(pady=5)
    entry_pais = ttk.Entry(root)
    entry_pais.pack()

    ttk.Label(root, text="🏙️ Ciudad:", font=fuente).pack(pady=5)
    entry_ciudad = ttk.Entry(root)
    entry_ciudad.pack()

    ttk.Label(root, text="✉️ Correo destinatario:", font=fuente).pack(pady=5)
    entry_correo = ttk.Entry(root)
    entry_correo.pack()

    ttk.Label(root, text="⏰ ¿Cuándo enviar el correo?", font=fuente).pack(pady=10)
    combo_opciones = ttk.Combobox(root, values=["Ahora", "En X minutos", "Fecha específica"], state="readonly")
    combo_opciones.current(0)
    combo_opciones.pack()

    entry_valor = ttk.Entry(root, state="disabled")
    entry_valor.pack(pady=5)

    estado_label = ttk.Label(root, text="", font=fuente, foreground="blue")
    estado_label.pack(pady=10)

    def actualizar_estado_entry(event=None):
        seleccion = combo_opciones.get()
        if seleccion == "Ahora":
            entry_valor.config(state="disabled")
            entry_valor.delete(0, tk.END)
        elif seleccion == "En X minutos":
            entry_valor.config(state="normal")
            entry_valor.delete(0, tk.END)
            entry_valor.insert(0, "5")
        elif seleccion == "Fecha específica":
            entry_valor.config(state="normal")
            entry_valor.delete(0, tk.END)
            entry_valor.insert(0, "05-06-2025 20:00")

    combo_opciones.bind("<<ComboboxSelected>>", actualizar_estado_entry)
    actualizar_estado_entry()

    def al_enviar():
        pais = entry_pais.get().strip()
        ciudad = entry_ciudad.get().strip()
        correo = entry_correo.get().strip()
        tipo_envio = combo_opciones.get()
        valor = entry_valor.get().strip()

        if not pais or not ciudad or not correo:
            messagebox.showerror("Campos incompletos", "Todos los campos son obligatorios.")
            return

        if not validar_correo(correo):
            messagebox.showerror("Correo inválido", "Por favor, introduce un correo válido.")
            return

        enviar_reporte(pais, ciudad, correo, tipo_envio, valor, estado_label)

    ttk.Button(root, text="📤 Enviar Reporte", command=al_enviar).pack(pady=15)

    root.mainloop()

if __name__ == "__main__":
    iniciar_interfaz()