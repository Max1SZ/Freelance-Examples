import os
import pandas as pd
import sqlalchemy

# --- Configuración base de datos ---
db_user = "root"
db_pass = ""
db_host = "localhost"
db_name = "prueba1"  # Cambiar según tu base

engine = sqlalchemy.create_engine(f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}")

# --- Pedimos CSV al usuario ---
csv_path = input("Inserte la ruta del CSV a cargar (ej: clientes.csv): ").strip().strip('"').strip("'")
table_name = os.path.splitext(os.path.basename(csv_path))[0]  # deducimos tabla por nombre de archivo

# --- Cargar CSV si existe ---
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    print(f"✅ CSV '{csv_path}' cargado correctamente")
else:
    print("⚠️ CSV no encontrado. Se creará uno nuevo al guardar.")
    cols = input("Ingrese los nombres de las columnas separados por comas: ").strip()
    col_list = [c.strip() for c in cols.split(",") if c.strip()]
    df = pd.DataFrame(columns=col_list)

# --- Menú simple ---
while True:
    print("\n--- MENÚ ---")
    print("1. Agregar fila")
    print("2. Guardar en CSV")
    print("3. Subir CSV a la base de datos")
    print("4. Mostrar datos actuales")
    print("5. Salir")

    opcion = input("Elige una opción: ").strip()

    if opcion == "1":
        nueva_fila = {}
        for col in df.columns:
            val = input(f"{col} = ")
            nueva_fila[col] = val if val != "" else None
        df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
        print("✅ Fila agregada")

    elif opcion == "2":
        df.to_csv(csv_path, index=False)
        print(f"✅ Datos guardados en {csv_path}")

    elif opcion == "3":
        try:
            df.to_sql(table_name, engine, if_exists="append", index=False)
            print(f"✅ CSV enviado a la tabla '{table_name}' en la base de datos")
        except Exception as e:
            print("❌ Error al subir datos:", e)

    elif opcion == "4":
        print("\nDatos actuales:")
        print(df.head(10))
        print(f"(Total filas: {len(df)}, columnas: {list(df.columns)})")

    elif opcion == "5":
        print("👋 Saliendo del programa...")
        break

    else:
        print("Opción no válida")
