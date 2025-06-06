import tkinter as tk
from tkinter import ttk, messagebox
import threading
import re
import os
from datetime import datetime

from dashboard import generar_reporte
from gmail_service import enviar_correo
from correo_programado import esperar_y_enviar_cada_lunes

def validar_correo(correo):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, correo) is not None

def enviar_reporte(pais, ciudad, correo, estado_label):
    try:
        generar_reporte(pais, ciudad)

        if not os.path.exists("reporte_diario.txt"):
            estado_label.config(text="Error: No se encontró reporte_diario.txt", foreground="red")
            return

        with open("reporte_diario.txt", "r", encoding="utf-8") as f:
            contenido = f.read()

        try:
            fecha = re.search(r"Reporte Diario - (.*)", contenido).group(1)
            ciudad_ = re.search(r"Ciudad: (.*)", contenido).group(1)
            pais_ = re.search(r"País: (.*) \| Ciudad:", contenido).group(1)
            clima = re.search(r"Clima: (.*) \| Temp:", contenido).group(1)
            temp = re.search(r"Temp: (.*)°C", contenido).group(1)
            noticias = re.search(r"Principales noticias:(.*)", contenido, re.DOTALL).group(1).strip()
        except Exception as e:
            estado_label.config(text=f"❌ Error al leer el reporte: {e}", foreground="red")
            return

        def tarea_envio():
            estado_label.config(text="📨 Enviando correo...", foreground="blue")
            try:
                enviar_correo(correo, fecha, pais_, ciudad_, clima, temp, noticias)
                estado_label.config(text="✅ Correo enviado con éxito.", foreground="green")
            except Exception as e:
                estado_label.config(text=f"❌ Error al enviar el correo: {e}", foreground="red")

        threading.Thread(target=tarea_envio, daemon=True).start()

    except Exception as e:
        estado_label.config(text=f"❌ Error general: {e}", foreground="red")

def iniciar_interfaz():
    root = tk.Tk()
    root.title("Reporte Express de Clima y Noticias")
    root.geometry("480x400")
    root.resizable(False, False)
    root.config(bg="#eaf2f8")

    fuente_label = ("Arial", 11, "bold")
    fuente_entry = ("Arial", 11)
    fuente_btn = ("Arial", 12, "bold")

    main_frame = tk.Frame(root, bg="#eaf2f8", padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)

    titulo = tk.Label(main_frame, text="🌍 Reporte Express", font=("Arial", 17, "bold"), bg="#eaf2f8", fg="#1f4e79")
    titulo.pack(pady=(0, 15))

    form_frame = tk.Frame(main_frame, bg="#eaf2f8")
    form_frame.pack(fill=tk.X, pady=5)

    # País
    tk.Label(form_frame, text="Código país (ej: cl):", font=fuente_label, bg="#eaf2f8", fg="#2d3436").grid(row=0, column=0, sticky="w", pady=6)
    entry_pais = ttk.Entry(form_frame, font=fuente_entry, width=28)
    entry_pais.grid(row=0, column=1, pady=6, padx=10)
    entry_pais.insert(0, "cl")

    # Ciudad
    tk.Label(form_frame, text="Ciudad:", font=fuente_label, bg="#eaf2f8", fg="#2d3436").grid(row=1, column=0, sticky="w", pady=6)
    entry_ciudad = ttk.Entry(form_frame, font=fuente_entry, width=28)
    entry_ciudad.grid(row=1, column=1, pady=6, padx=10)
    entry_ciudad.insert(0, "La Serena")

    # Correo
    tk.Label(form_frame, text="Correo destino:", font=fuente_label, bg="#eaf2f8", fg="#2d3436").grid(row=2, column=0, sticky="w", pady=6)
    entry_correo = ttk.Entry(form_frame, font=fuente_entry, width=28)
    entry_correo.grid(row=2, column=1, pady=6, padx=10)

    # Estado
    estado_label = tk.Label(main_frame, text="", font=("Arial", 10), bg="#eaf2f8")
    estado_label.pack(pady=(10, 5))

    def actualizar_estado_label(mensaje, color):
        estado_label.config(text=mensaje, foreground=color)

    def al_enviar():
        pais = entry_pais.get().strip()
        ciudad = entry_ciudad.get().strip()
        correo = entry_correo.get().strip()

        if not pais or not ciudad or not correo:
            messagebox.showerror("Campos incompletos", "Por favor, completa todos los campos.")
            return

        if not validar_correo(correo):
            messagebox.showerror("Correo inválido", "Introduce un correo válido.")
            return

        enviar_reporte(pais, ciudad, correo, estado_label)

    def al_programar_envio():
        pais = entry_pais.get().strip()
        ciudad = entry_ciudad.get().strip()
        correo = entry_correo.get().strip()

        if not pais or not ciudad or not correo:
            messagebox.showerror("Campos incompletos", "Por favor, completa todos los campos.")
            return

        if not validar_correo(correo):
            messagebox.showerror("Correo inválido", "Introduce un correo válido.")
            return

        esperar_y_enviar_cada_lunes(correo, pais, ciudad, callback_estado=actualizar_estado_label)
        messagebox.showinfo("Programado", "✅ Envío automático programado para cada lunes a las 8:00 AM.")

    boton_enviar = tk.Button(main_frame, text="📤 Enviar Ahora", font=fuente_btn, bg="#3498db", fg="white",
                             activebackground="#2980b9", activeforeground="white", relief="flat", padx=10, pady=7,
                             command=al_enviar)
    boton_enviar.pack(pady=(10, 7))

    boton_programar = tk.Button(main_frame, text="⏰ Programar Envío Semanal", font=fuente_btn, bg="#2ecc71", fg="white",
                               activebackground="#27ae60", activeforeground="white", relief="flat", padx=10, pady=7,
                               command=al_programar_envio)
    boton_programar.pack(pady=7)

    root.mainloop()

if __name__ == "__main__":
    iniciar_interfaz()
