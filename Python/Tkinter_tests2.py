import tkinter as tk
from tkinter import ttk

# Ventana principal
root = tk.Tk()
root.title("Demo CRUD con Frames")
root.geometry("600x400")

# Frame contenedor (aquí cambiaremos el contenido dinámicamente)
contenedor = tk.Frame(root)
contenedor.pack(fill="both", expand=True)

# Función para limpiar el frame
def limpiar_frame():
    for widget in contenedor.winfo_children():
        widget.destroy()

# Funciones de "pantallas"
def pantalla_inicio():
    limpiar_frame()
    label = tk.Label(contenedor, text="🏠 Bienvenido al gestor de datasets", font=("Arial", 16))
    label.pack(pady=20)

def pantalla_cargar():
    limpiar_frame()
    label = tk.Label(contenedor, text="📂 Cargar Dataset", font=("Arial", 14))
    label.pack(pady=10)
    # acá iría el filedialog para cargar un CSV/Excel
    entry = tk.Entry(contenedor)
    entry.pack(pady=5)
    tk.Button(contenedor, text="Aceptar", command=lambda: print("Archivo cargado")).pack()

def pantalla_editar():
    limpiar_frame()
    label = tk.Label(contenedor, text="✏️ Edición de Dataset", font=("Arial", 14))
    label.pack(pady=10)

    # ejemplo de tabla con Treeview
    tree = ttk.Treeview(contenedor, columns=("Col1", "Col2"), show="headings")
    tree.heading("Col1", text="ID")
    tree.heading("Col2", text="Nombre")
    tree.insert("", "end", values=(1, "Ana"))
    tree.insert("", "end", values=(2, "Luis"))
    tree.pack(fill="both", expand=True)

def pantalla_reportes():
    limpiar_frame()
    label = tk.Label(contenedor, text="📊 Reportes", font=("Arial", 14))
    label.pack(pady=10)
    tk.Button(contenedor, text="Ranking clientes", command=lambda: print("Generando ranking...")).pack(pady=5)
    tk.Button(contenedor, text="Ventas por mes", command=lambda: print("Generando ventas mensuales...")).pack(pady=5)

# --- Menú principal ---
menu = tk.Menu(root)
root.config(menu=menu)

menu_principal = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Menú", menu=menu_principal)
menu_principal.add_command(label="Inicio", command=pantalla_inicio)
menu_principal.add_command(label="Cargar Dataset", command=pantalla_cargar)
menu_principal.add_command(label="Editar Dataset", command=pantalla_editar)
menu_principal.add_command(label="Reportes", command=pantalla_reportes)
menu_principal.add_separator()
menu_principal.add_command(label="Salir", command=root.quit)

# Mostrar pantalla inicial
pantalla_inicio()

root.mainloop()
