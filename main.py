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
            estado_label.config(text="Error: No se encontró reporte_diario.txt", foreground="red")
            return

        with open("reporte_diario.txt", "r", encoding="utf-8") as f:
            contenido = f.read()

        # Extracción datos omitida para brevedad...

        # Cálculo delay omitido para brevedad...

        def tarea_envio():
            if delay > 0:
                estado_label.config(text=f"⏳ Esperando {round(delay / 60, 2)} minutos...", foreground="orange")
                time.sleep(delay)

            estado_label.config(text="📨 Enviando correo...", foreground="blue")
            try:
                enviar_correo(correo, fecha, pais, ciudad, clima, temp, noticias)
                estado_label.config(text="✅ Correo enviado con éxito.", foreground="green")
            except Exception as e:
                estado_label.config(text=f"❌ Error al enviar el correo: {e}", foreground="red")

        threading.Thread(target=tarea_envio, daemon=True).start()

    except Exception as e:
        estado_label.config(text=f"❌ Error general: {e}", foreground="red")

def iniciar_interfaz():
    root = tk.Tk()
    root.title("Envio de Reporte Climatico y Noticias")
    root.geometry("520x400")
    root.resizable(False, False)
    root.config(bg="#f5f7fa")  # Fondo suave

    fuente_label = ("Helvetica", 11, "bold")
    fuente_entry = ("Helvetica", 11)
    fuente_btn = ("Helvetica", 12, "bold")

    # Contenedor principal con padding
    main_frame = tk.Frame(root, bg="#f5f7fa", padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Titulo
    titulo = tk.Label(main_frame, text="Enviar Reporte Climático y Noticias", font=("Helvetica", 16, "bold"), bg="#f5f7fa", fg="#333")
    titulo.pack(pady=(0,15))

    # Frame para inputs
    form_frame = tk.Frame(main_frame, bg="#f5f7fa")
    form_frame.pack(fill=tk.X, pady=10)

    # País
    tk.Label(form_frame, text="Código del país (ej: cl):", font=fuente_label, bg="#f5f7fa", fg="#555").grid(row=0, column=0, sticky="w", pady=6)
    entry_pais = ttk.Entry(form_frame, font=fuente_entry, width=30)
    entry_pais.grid(row=0, column=1, pady=6, padx=10)

    # Ciudad
    tk.Label(form_frame, text="Ciudad:", font=fuente_label, bg="#f5f7fa", fg="#555").grid(row=1, column=0, sticky="w", pady=6)
    entry_ciudad = ttk.Entry(form_frame, font=fuente_entry, width=30)
    entry_ciudad.grid(row=1, column=1, pady=6, padx=10)

    # Correo
    tk.Label(form_frame, text="Correo destinatario:", font=fuente_label, bg="#f5f7fa", fg="#555").grid(row=2, column=0, sticky="w", pady=6)
    entry_correo = ttk.Entry(form_frame, font=fuente_entry, width=30)
    entry_correo.grid(row=2, column=1, pady=6, padx=10)

    # Cuando enviar
    tk.Label(form_frame, text="¿Cuándo enviar el correo?", font=fuente_label, bg="#f5f7fa", fg="#555").grid(row=3, column=0, sticky="w", pady=6)
    combo_opciones = ttk.Combobox(form_frame, values=["Ahora", "En X minutos", "Fecha específica"], state="readonly", font=fuente_entry, width=28)
    combo_opciones.current(0)
    combo_opciones.grid(row=3, column=1, pady=6, padx=10)

    entry_valor = ttk.Entry(form_frame, font=fuente_entry, width=30, state="disabled")
    entry_valor.grid(row=4, column=1, pady=6, padx=10)

    estado_label = tk.Label(main_frame, text="", font=("Helvetica", 10), bg="#f5f7fa")
    estado_label.pack(pady=(10,5))

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
            messagebox.showerror("Campos incompletos", "Por favor, completa todos los campos.")
            return

        if not validar_correo(correo):
            messagebox.showerror("Correo inválido", "Introduce un correo válido.")
            return

        enviar_reporte(pais, ciudad, correo, tipo_envio, valor, estado_label)

    boton_enviar = tk.Button(main_frame, text="Enviar Reporte", font=fuente_btn, bg="#4a90e2", fg="white", activebackground="#357ABD", activeforeground="white", relief="flat", padx=10, pady=8, command=al_enviar)
    boton_enviar.pack(pady=15, fill=tk.X)

    root.mainloop()

if __name__ == "__main__":
    iniciar_interfaz()
