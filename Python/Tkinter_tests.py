import pandas as pd 
import tkinter as tk 
from tkinter import ttk
root = tk.Tk()
root.title("Demo Tkinter")
root.geometry("500x400")   # tamaño fijo
root.resizable(False, False)  # evita cambios

label = tk.Label(text="Bienvenido a Tkinter")
label.pack()

# Funciónes:
#al hacer click en este botn, genera una nueva ventana con un texto diferente
def cambiar_texto():
    root2 = tk.Tk()
    root2.title("Texto cambiado")
    root2.geometry("500x400")   # tamaño fijo
    root2.resizable(False, False)  # evita cambios
    
    label2 = tk.Label(root2,text="¡Hiciste clic!")
    label2.pack()

# otra función de prueba. Se especializa en otro boton de salida
def test():
    root3 = tk.Tk()
    root3.title("Otro texto")
    root3.geometry("500x400")   # tamaño fijo
    root3.resizable(False, False)  # evita cambios

    label3 = tk.Label(root3,text="¡Otra ventana!")
    label3.pack()
    ttk.Button(root3, text="Salir", command=root3.destroy).pack(pady=20)


# Botones
boton = tk.Button(root, text="Click aquí", command=cambiar_texto)
boton.pack(pady=20)

boton = tk.Button(root, text="prueba", command=test)
boton.pack(pady=20)

boton = tk.Button(root, text="Salir", command=root.quit)
boton.pack(pady=20)

root.mainloop()