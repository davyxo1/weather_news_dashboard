import tkinter as tk
from tkinter import ttk, messagebox
import threading
import json
import re
import os

from dashboard import generar_reporte
from gmail_service import enviar_correo
from programador_envio import esperar_y_enviar_cada_minuto_prueba  # 👈 cambiamos la función

# Validar correo
def validar_correo(correo):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, correo) is not None

# Guardar configuración
def guardar_config(pais, ciudad, correo, hora, minuto):
    config = {
        "pais": pais,
        "ciudad": ciudad,
        "correo": correo,
        "hora": hora,
        "minuto": minuto
    }
    with open("config_envio.json", "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

# Enviar reporte ahora mismo
def enviar_reporte(pais, ciudad, correo, estado_label):
    try:
        generar_reporte(pais, ciudad)
        if not os.path.exists("reporte_diario.txt"):
            estado_label.config(text="❌ No se encontró reporte_diario.txt", foreground="red")
            return

        with open("reporte_diario.txt", "r", encoding="utf-8") as f:
            contenido = f.read()

        def buscar(dato, label):
            match = re.search(fr"{label}:\s+(.*)", contenido)
            if not match:
                raise ValueError(f"No se encontró el campo '{label}' en el reporte")
            return match.group(1)

        fecha = buscar("fecha", "Fecha")
        ciudad = buscar("ciudad", "Ciudad")
        pais = buscar("pais", "País")
        clima = buscar("clima", "Clima")
        temp = buscar("temperatura", "Temperatura")
        noticias = buscar("noticias", "Noticias")

        def tarea_envio():
            estado_label.config(text="📨 Enviando correo...", foreground="blue")
            try:
                enviar_correo(correo, fecha, pais, ciudad, clima, temp, noticias)
                estado_label.config(text="✅ Correo enviado con éxito.", foreground="green")
            except Exception as e:
                estado_label.config(text=f"❌ Error al enviar el correo: {e}", foreground="red")

        threading.Thread(target=tarea_envio, daemon=True).start()

    except Exception as e:
        estado_label.config(text=f"❌ Error al leer el reporte: {e}", foreground="red")

# Interfaz gráfica
def iniciar_interfaz():
    root = tk.Tk()
    root.title("Reporte Express de Clima y Noticias")
    root.geometry("500x430")
    root.config(bg="#eaf2f8")

    fuente_label = ("Arial", 11, "bold")
    fuente_entry = ("Arial", 11)
    fuente_btn = ("Arial", 12, "bold")

    main_frame = tk.Frame(root, bg="#eaf2f8", padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(main_frame, text="🌍 Reporte Express (Modo Prueba)", font=("Arial", 17, "bold"),
             bg="#eaf2f8", fg="#1f4e79").pack(pady=(0, 15))

    form_frame = tk.Frame(main_frame, bg="#eaf2f8")
    form_frame.pack(fill=tk.X)

    labels = ["Código país (ej: cl):", "Ciudad:", "Correo destino:", "Hora (0-23):", "Minuto (0-59):"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(form_frame, text=label, font=fuente_label, bg="#eaf2f8").grid(row=i, column=0, sticky="w", pady=5)
        entry = ttk.Entry(form_frame, font=fuente_entry, width=28)
        entry.grid(row=i, column=1, pady=5, padx=10)
        entries.append(entry)

    entry_pais, entry_ciudad, entry_correo, entry_hora, entry_minuto = entries

    estado_label = tk.Label(main_frame, text="", font=("Arial", 10), bg="#eaf2f8")
    estado_label.pack(pady=(10, 5))

    def al_enviar():
        pais = entry_pais.get().strip()
        ciudad = entry_ciudad.get().strip()
        correo = entry_correo.get().strip()
        hora = entry_hora.get().strip()
        minuto = entry_minuto.get().strip()

        if not (pais and ciudad and correo and hora.isdigit() and minuto.isdigit()):
            messagebox.showerror("Campos incompletos", "Por favor, completa todos los campos correctamente.")
            return

        if not validar_correo(correo):
            messagebox.showerror("Correo inválido", "Introduce un correo válido.")
            return

        guardar_config(pais, ciudad, correo, int(hora), int(minuto))
        enviar_reporte(pais, ciudad, correo, estado_label)

        # Iniciar programador de prueba
        esperar_y_enviar_cada_minuto_prueba(correo, pais, ciudad, lambda msg, color: estado_label.config(text=msg, foreground=color))

    tk.Button(main_frame, text="📤 Enviar Ahora y Probar Automático", font=fuente_btn, bg="#3498db", fg="white",
              activebackground="#2980b9", relief="flat", padx=10, pady=8, command=al_enviar).pack(pady=15, fill=tk.X)

    root.mainloop()

if __name__ == "__main__":
    iniciar_interfaz()
