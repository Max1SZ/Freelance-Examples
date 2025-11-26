'''
-----------------
DataManager_v2c 
El codigo lo que hara sera:
* Permitir al usuario cargar uno o varios archivos CSV.
* Mostrar un menú para agregar, modificar o eliminar filas en los DataFrames cargados.
* Permitir guardar los cambios en los archivos CSV originales.
* Subir los datos modificados a una base de datos SQL.
* Utiliza pandas para manejar los datos y SQLAlchemy para la conexión con la base de datos.
-----------------'''

import pandas as pd
import sqlalchemy
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Conexión a la base de datos (ajusta los datos según tu entorno)
engine = sqlalchemy.create_engine("mysql+pymysql://root:@localhost/empresa_ca")

# Diccionario para almacenar los DataFrames y sus rutas
csvs = {}  # nombre_csv : (df, ruta)

#-----------------
# Cargar uno o varios CSVs
def cargar_csv():
    rutas = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")])
    for ruta in rutas:
        try:
            df = pd.read_csv(ruta)
            nombre = ruta.split("/")[-1].replace(".csv", "")
            csvs[nombre] = (df, ruta)
            messagebox.showinfo("Éxito", f"{nombre} cargado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar {ruta}: {e}")
#-----------------
# Mostrar un CSV
def mostrar_csv(nombre):
    if nombre not in csvs:
        messagebox.showwarning("Atención", f"No se cargó {nombre}")
        return
    df, _ = csvs[nombre]
    # limpiar tabla
    tree.delete(*tree.get_children())
    tree["columns"] = list(df.columns)
    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))
#-----------------
# Guardar cambios en CSV y todos los CSVs
def guardar_csv(nombre):
    if nombre not in csvs:
        messagebox.showwarning("Atención", "No hay CSV cargado.")
        return
    df, ruta = csvs[nombre]
    df.to_csv(ruta, index=False)
    messagebox.showinfo("Éxito", f"Guardado en {ruta}")

def guardar_todos():
    for nombre, (df, ruta) in csvs.items():
        df.to_csv(ruta, index=False)
    messagebox.showinfo("Éxito", "Todos los CSVs fueron guardados.")
#-----------------        
# Modificar un CSV
def modify_csv():
    if not csvs:
        print("No hay CSVs cargados.")
        return
    print("Archivos disponibles:")
    for i, nombre in enumerate(csvs):
        print(f"{i+1}. {nombre}")
    try:
        idx = int(input("Elige el número del CSV: ")) - 1
        nombre = list(csvs.keys())[idx]
        df, ruta = csvs[nombre]
        print("Columnas disponibles:", list(df.columns)) # muestra las columnas del csv
        fila = int(input("Número de fila a modificar: "))
        if fila < 0 or fila >= len(df): # checa que la fila exista
            print("Fila inválida.")
            return
        columna = input("Nombre de la columna a modificar: ").strip()
        if columna not in df.columns:
            print("Columna inválida.")
            return
        nuevo_valor = input("Nuevo valor: ")
        df.at[fila, columna] = nuevo_valor
        df.to_csv(ruta, index=False)
        print("CSV modificado y guardado.")
        csvs[nombre] = (df, ruta) # actualiza el diccionario
    except (ValueError, IndexError):
        print("Entrada inválida.")
#-----------------    
# Subir datos a SQL
def subir_sql(nombre):
    if nombre not in csvs:
        messagebox.showwarning("Atención", "No hay CSV cargado.")
        return
    df, _ = csvs[nombre]
    try:
        df.to_sql(nombre, con=engine, if_exists='replace', index=False)
        messagebox.showinfo("Éxito", f"{nombre} subido a SQL")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo subir {nombre}: {e}")

#-----------------
def mostrar_dataframe(df, titulo="Resultado"):
    # limpiar tabla
    tree.delete(*tree.get_children())
    tree["columns"] = list(df.columns)
    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))

#------------------
# Reportes
def ranking_clientes():
    if "clientes" not in csvs or "facturas_enc" not in csvs:
        messagebox.showwarning("Atención", "Carga clientes y facturas_enc")
        return
    clientes, _ = csvs["clientes"]
    facturas, _ = csvs["facturas_enc"]
    merged = pd.merge(facturas, clientes, on="id_cliente")
    df = merged.groupby("nombre")["total"].sum().reset_index()
    df = df.sort_values(by="total", ascending=False).head(10)
    mostrar_dataframe(df, "Ranking clientes")

def ticket_promedio():
    if "clientes" not in csvs or "facturas_enc" not in csvs:
        messagebox.showwarning("Atención", "Carga clientes y facturas_enc")
        return
    clientes, _ = csvs["clientes"]
    facturas, _ = csvs["facturas_enc"]
    merged = pd.merge(facturas, clientes, on="id_cliente")
    df = merged.groupby("nombre")["total"].mean().reset_index()
    df.rename(columns={"total": "ticket_promedio"}, inplace=True)
    mostrar_dataframe(df.sort_values(by="ticket_promedio", ascending=False).head(10),
                      "Ticket promedio")

def facturas_altas():
    if "facturas_enc" not in csvs:
        messagebox.showwarning("Atención", "Carga facturas_enc")
        return
    facturas, _ = csvs["facturas_enc"]
    df = facturas.sort_values(by="total", ascending=False).head(10)
    mostrar_dataframe(df, "Facturas más altas")

def ventas_por_mes():
    if "facturas_enc" not in csvs:
        messagebox.showwarning("Atención", "Carga facturas_enc")
        return None
    facturas, _ = csvs["facturas_enc"]
    if facturas.empty or "fecha" not in facturas.columns or "total" not in facturas.columns:
        messagebox.showerror("Error", "El archivo facturas_enc no tiene datos válidos.")
        return None
    facturas["fecha"] = pd.to_datetime(facturas["fecha"], errors="coerce")
    df = facturas.groupby(facturas["fecha"].dt.to_period("M"))["total"].sum().reset_index()
    df.rename(columns={"fecha": "mes"}, inplace=True)
    mostrar_dataframe(df, "Ventas por mes")
    return df

def producto_mas_vendido():
    if "facturas_det" not in csvs or "productos" not in csvs:
        messagebox.showwarning("Atención", "Carga facturas_det y productos")
        return
    fdet, _ = csvs["facturas_det"]
    prods, _ = csvs["productos"]
    df = fdet.groupby("id_producto")["cantidad"].sum().reset_index()
    df = pd.merge(df, prods, on="id_producto")
    mostrar_dataframe(df.sort_values(by="cantidad", ascending=False).head(5),
                      "Productos más vendidos")

def ventas_por_rubro():
    if "facturas_det" not in csvs or "productos" not in csvs or "rubros" not in csvs:
        messagebox.showwarning("Atención", "Carga facturas_det, productos y rubros")
        return
    fdet, _ = csvs["facturas_det"]
    prods, _ = csvs["productos"]
    rubros, _ = csvs["rubros"]
    df = pd.merge(fdet, prods, on="id_producto")
    df = pd.merge(df, rubros, on="id_rubro")
    df = df.groupby("nombre")["cantidad"].sum().reset_index()
    mostrar_dataframe(df.sort_values(by="cantidad", ascending=False),
                      "Ventas por rubro")

def grafico_ventas():
    df_mes = ventas_por_mes()
    if df_mes is None or df_mes.empty:
        messagebox.showwarning("Atención", "No hay datos para graficar.")
        return
    df_mes.set_index("mes")["total"].plot(kind="bar", figsize=(8, 4))
    plt.title("Ventas mensuales")
    plt.xlabel("Mes")
    plt.ylabel("Total")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


#-----------------
#Top productos por facturación
def top_productos_facturacion():
    if "facturas_det" not in csvs or "productos" not in csvs:
        messagebox.showwarning("Atención", "Carga facturas_det y productos")
        return
    fdet, _ = csvs["facturas_det"]
    prods, _ = csvs["productos"]
    df = pd.merge(fdet, prods, on="id_producto")
    df["importe"] = df["cantidad"] * df["precio_unitario"]
    df = df.groupby("nombre")["importe"].sum().reset_index()
    mostrar_dataframe(df.sort_values(by="importe", ascending=False).head(10),
                      "Top productos por facturación")
#---------------------
#OPCIONES DE CRUD
def abrir_crud():
    if not csvs:
        messagebox.showwarning("Atención", "No hay CSVs cargados")
        return

    # Ventana de selección
    ventana_crud = tk.Toplevel()
    ventana_crud.title("Gestión CRUD")
    ventana_crud.geometry("500x400")

    tk.Label(ventana_crud, text="Selecciona un CSV:").pack(pady=5)
    lista = tk.Listbox(ventana_crud, height=6)
    lista.pack(pady=5)

    for nombre in csvs.keys():
        lista.insert(tk.END, nombre)

    def abrir_tabla():
        sel = lista.curselection()
        if not sel:
            messagebox.showerror("Error", "Selecciona un CSV")
            return
        nombre = lista.get(sel[0])
        mostrar_crud_tabla(nombre)
        ventana_crud.destroy()

    tk.Button(ventana_crud, text="Abrir", command=abrir_tabla).pack(pady=10)

def mostrar_crud_tabla(nombre):
    df, ruta = csvs[nombre]

    crud_tabla = tk.Toplevel(root)
    crud_tabla.title(f"CRUD - {nombre}")

    # Treeview
    tree = ttk.Treeview(crud_tabla, columns=list(df.columns), show="headings")
    tree.pack(fill="both", expand=True)

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    # cargar datos
    for _, row in df.iterrows():
        tree.insert("", tk.END, values=list(row))

    # ---- Funciones CRUD ----
    def agregar():
        form = tk.Toplevel(crud_tabla)
        form.title("Agregar fila")
        entradas = {}
        for i, col in enumerate(df.columns):
            tk.Label(form, text=col).grid(row=i, column=0, padx=5, pady=5)
            e = tk.Entry(form)
            e.grid(row=i, column=1, padx=5, pady=5)
            entradas[col] = e

        def guardar():
            nonlocal df
            nueva = {col: entradas[col].get() for col in df.columns}
            df = pd.concat([df, pd.DataFrame([nueva])], ignore_index=True)
            tree.insert("", tk.END, values=list(nueva.values()))
            csvs[nombre] = (df, ruta)
            form.destroy()

        tk.Button(form, text="Guardar", command=guardar).grid(row=len(df.columns), column=0, columnspan=2, pady=10)

    def modificar():
        item = tree.selection()
        if not item:
            messagebox.showerror("Error", "Selecciona una fila")
            return
        vals = tree.item(item)["values"]

        form = tk.Toplevel(crud_tabla)
        form.title("Modificar fila")
        entradas = {}
        for i, col in enumerate(df.columns):
            tk.Label(form, text=col).grid(row=i, column=0, padx=5, pady=5)
            e = tk.Entry(form)
            e.insert(0, vals[i])
            e.grid(row=i, column=1, padx=5, pady=5)
            entradas[col] = e

        def guardar():
            nueva = [entradas[col].get() for col in df.columns]
            idx = tree.index(item)
            tree.item(item, values=nueva)
            df.iloc[idx] = nueva
            csvs[nombre] = (df, ruta)
            form.destroy()

        tk.Button(form, text="Guardar", command=guardar).grid(row=len(df.columns), column=0, columnspan=2, pady=10)

    def eliminar():
        item = tree.selection()
        if not item:
            messagebox.showerror("Error", "Selecciona una fila")
            return
        idx = tree.index(item)
        tree.delete(item)
        nonlocal df
        df = df.drop(idx).reset_index(drop=True)
        csvs[nombre] = (df, ruta)

    def guardar_cambios():
        opcion = messagebox.askyesnocancel("Guardar", "¿Deseas guardar los cambios en el archivo original?\n(Sí = sobreescribe, No = Guardar como, Cancelar = no guardar)")
        if opcion is True:  # sí
            df.to_csv(ruta, index=False)
            messagebox.showinfo("Guardado", f"Archivo sobrescrito: {ruta}")
        elif opcion is False:  # guardar como
            nueva_ruta = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
            if nueva_ruta:
                df.to_csv(nueva_ruta, index=False)
                messagebox.showinfo("Guardado", f"Archivo guardado en: {nueva_ruta}")

    # Botones CRUD
    tk.Button(frame_btn, text="Agregar fila", command=agregar).grid(row=0, column=11, padx=5)
    tk.Button(frame_btn, text="Modificar fila", command=modificar).grid(row=1, column=10, padx=5)
    tk.Button(frame_btn, text="Eliminar fila", command=eliminar).grid(row=1, column=11, padx=5)
    tk.Button(frame_btn, text="Guardar cambios", command=guardar_cambios).grid(row=1, column=12, padx=5)


#Menu Tkinter
# -----------------
# Interfaz principal
root = tk.Tk()
root.title("DataManager v2c")
root.geometry("1000x600")
root.resizable(False, False)  # evita cambios

# Botones
frame_btn = tk.Frame(root)
frame_btn.pack(pady=10)

btn_cargar = tk.Button(frame_btn, text="📂 Cargar CSV", command=cargar_csv)
btn_cargar.grid(row=0, column=0, padx=5)

btn_guardar = tk.Button(frame_btn, text="💾 Guardar CSVs", command=guardar_todos)
btn_guardar.grid(row=0, column=1, padx=5)

btn_subir = tk.Button(frame_btn, text="⬆️ Subir a SQL", command=subir_sql)
btn_subir.grid(row=0, column=2, padx=5)

# Reportes
btn_rank = tk.Button(frame_btn, text="📊 Ranking clientes", command=ranking_clientes)
btn_rank.grid(row=1, column=0, padx=5)

btn_ticket = tk.Button(frame_btn, text="🎟 Ticket promedio", command=ticket_promedio)
btn_ticket.grid(row=1, column=1, padx=5)

btn_facturas = tk.Button(frame_btn, text="💸 Facturas altas", command=facturas_altas)
btn_facturas.grid(row=1, column=2, padx=5)

btn_mes = tk.Button(frame_btn, text="📆 Ventas por mes", command=ventas_por_mes)
btn_mes.grid(row=2, column=0, padx=5)

btn_grafico = tk.Button(frame_btn, text="📈 Gráfico ventas", command=grafico_ventas)
btn_grafico.grid(row=2, column=1, padx=5)

btn_prod = tk.Button(frame_btn, text="📦 Prod. más vendido", command=producto_mas_vendido)
btn_prod.grid(row=2, column=2, padx=5)

btn_rubro = tk.Button(frame_btn, text="🏷 Ventas por rubro", command=ventas_por_rubro)
btn_rubro.grid(row=3, column=0, padx=5)

btn_top = tk.Button(frame_btn, text="⭐ Top facturación", command=top_productos_facturacion)
btn_top.grid(row=3, column=1, padx=5)

# Botones CRUD

btn_crud = tk.Button(frame_btn, text="🛠 CRUD CSV", command=abrir_crud)
btn_crud.grid(row=3, column=2, padx=5)
    
# Tabla
tree = ttk.Treeview(root, show="headings")
tree.pack(fill="both", expand=True)

root.mainloop()


#UNUSED. Only for reference -Maxi
#-----------------
# Unificar más de dos tablas en cadena
def unify_tables():
    if len(csvs) < 2:
            print("Necesitas al menos 2 CSVs cargados.")
            return
            print("Archivos disponibles:")

    for i, nombre in enumerate(csvs):
            print(f"{i+1}. {nombre}")

    try:
        indices = input("Elige los números de los CSVs a unir (separados por coma, ej: 1,2,3): ")
        indices = [int(x.strip()) - 1 for x in indices.split(",") if x.strip().isdigit()]
        if len(indices) < 2:
            print("Debes seleccionar al menos 2 CSVs.")
            return

        # Tomar el primero como base
        nombre_base = list(csvs.keys())[indices[0]]
        merged_df, _ = csvs[nombre_base]

        # Para unir los demás en cadena
        for idx in indices[1:]:
            nombre = list(csvs.keys())[idx]
            df, _ = csvs[nombre]

            print(f"\nUniendo {nombre_base} con {nombre}...")
            print("Columnas disponibles en la tabla base:", list(merged_df.columns))
            print("Columnas disponibles en", nombre, ":", list(df.columns))
            key = input("Columna en común para unir: ").strip()

            merged_df = pd.merge(merged_df, df, on=key, how="left")
            nombre_base += f"_{nombre}"  # ir concatenando nombres para el resultado

        print("\n Resultado de la unión en cadena (primeras filas):")
        print(merged_df.head())

        # Guardar opcionalmente
        guardar = input("¿Quieres guardar el resultado como un nuevo CSV? (s/n): ").strip().lower()
        if guardar == "s":
            nuevo_nombre = f"{nombre_base}_merge"
            csvs[nuevo_nombre] = (merged_df, f"{nuevo_nombre}.csv")
            merged_df.to_csv(f"{nuevo_nombre}.csv", index=False)
            print(f"\n Unión en cadena guardada como {nuevo_nombre}.csv y disponible en memoria.")
        else:
            print("\n Unión no guardada, solo mostrada en pantalla.")

    except Exception as e:
        print(f"Error al unir tablas: {e}")

'''
#-----------------
# Menú bash
while True:
    print("\n--- MENÚ ---")
    print("1. Insertar uno o varios CSVs")
    print("2. Checar un CSV")
    print("3. Modificar un CSV")
    print("4. Guardar todos los cambios")
    print("5. Subir datos a SQL")
    print("6. Unificar tablas")
    print("7. Reportes")
    print("0. Salir")

    opcion = input("Elige una opción: ")
    
    if opcion == "1":
        cargar_csv()
    elif opcion == "2":
        check_csv()
    elif opcion == "3":
        modify_csv()
    elif opcion == "4":
        save_all_csvs()
    elif opcion == "5":
        upload_to_sql()
    elif opcion == "6":
        unify_tables()
    elif opcion == "7":
        print("\n--- REPORTES ---")
        print("1. Ranking clientes")
        print("2. Ticket promedio")
        print("3. Facturas más altas")
        print("4. Ventas por mes")
        print("5. Producto más vendido")
        print("6. Ventas por rubro")
        print("7. Gráfico ventas mensuales")
        print("8. Top productos facturación")
        sub = input("Elige reporte: ")
        if sub == "1": ranking()
        elif sub == "2": ticket_promedio()
        elif sub == "3": top_facturas()
        elif sub == "4": ventas_por_mes()
        elif sub == "5": top_prods()
        elif sub == "6": det_rubro()
        elif sub == "7": grafico_ventas_mensuales()
        elif sub == "8": fac_prod()
        else: print("Opción inválida")
    elif opcion == "0":
        print("👋 Saliendo del programa...")
        break
    else:
        print("Opción no válida")
#-----------------'''
#