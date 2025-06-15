import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import locale

# Intentar establecer configuración regional para Colombia
try:
    locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')
except:
    locale.setlocale(locale.LC_ALL, '')

# Lista para guardar los movimientos
movimientos = []

def formatear_cop(valor):
    try:
        return locale.currency(valor, grouping=True)
    except:
        # Formato manual si falla locale
        return f"${valor:,.2f}".replace(",", "#").replace(".", ",").replace("#", ".")

def agregar_movimiento():
    tipo = tipo_var.get()
    descripcion = entrada_descripcion.get()
    monto = entrada_monto.get()

    if not descripcion or not monto:
        messagebox.showwarning("Campos vacíos", "Completa todos los campos.")
        return

    try:
        monto = float(monto)
    except ValueError:
        messagebox.showerror("Error", "El monto debe ser un número.")
        return

    if tipo == "Gasto":
        monto = -abs(monto)

    fecha = datetime.now().strftime("%d/%m/%Y")
    movimientos.append((fecha, descripcion, monto))

    actualizar_lista()
    limpiar_campos()

def actualizar_lista():
    lista.delete(0, tk.END)
    total = 0
    for mov in movimientos:
        fecha, desc, monto = mov
        lista.insert(tk.END, f"{fecha} - {desc}: {formatear_cop(monto)}")
        total += monto
    etiqueta_total.config(text=f"Balance total: {formatear_cop(total)}")

def limpiar_campos():
    entrada_descripcion.delete(0, tk.END)
    entrada_monto.delete(0, tk.END)
    tipo_var.set("Gasto")

# Ventana principal
ventana = tk.Tk()
ventana.title("💰 App de Gastos Personales")
ventana.geometry("400x500")
ventana.resizable(False, False)

# Elementos de entrada
tk.Label(ventana, text="Descripción:").pack()
entrada_descripcion = tk.Entry(ventana, width=40)
entrada_descripcion.pack()

tk.Label(ventana, text="Monto:").pack()
entrada_monto = tk.Entry(ventana, width=20)
entrada_monto.pack()

tipo_var = tk.StringVar(value="Gasto")
tk.Radiobutton(ventana, text="Gasto", variable=tipo_var, value="Gasto").pack()
tk.Radiobutton(ventana, text="Ingreso", variable=tipo_var, value="Ingreso").pack()

tk.Button(ventana, text="Agregar movimiento", command=agregar_movimiento).pack(pady=10)

# Lista de movimientos
tk.Label(ventana, text="Historial:").pack()
lista = tk.Listbox(ventana, width=50)
lista.pack(pady=5)

# Balance total
etiqueta_total = tk.Label(ventana, text="Balance total: $0.00", font=("Arial", 12, "bold"))
etiqueta_total.pack(pady=10)

ventana.mainloop()
