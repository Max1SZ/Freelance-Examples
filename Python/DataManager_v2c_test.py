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
'''
base para que agarre csvs
usar bucle for para el with:

import csv

ruta_csv = ("ruta del csv")

datos =[]

with open(ruta_csv, mode='r', encoding='utf-8') as archivo:
    lector = csv.DictReader(archivo)
    
    for fila in lector:
        datos.append(dict(fila))
        
for cliente in datos:
    print(cliente)

---------------
*Usar parte del codigo de DataManager 1 para la conexion con SQL.
'''
import pandas as pd
import sqlalchemy

engine = sqlalchemy.create_engine("mysql+pymysql://root:@localhost/empresa_ca")

#Para que copies, o almenos tengas una base de lo que seria la ruta.
#  
# C:/Users/estudiante/Desktop/TareasPYTHON/2025/clientes.csv
#
#dependiendo de donde tengas el csv, cambia la ruta despues de Users ovbio.
#  
#FUNCIONES
#------------

# Cargamos CSV 
def get_csv():
    ruta = input("Ruta del CSV: ").strip() #strip es para eliminar espacios inecesarios.
    if ruta == "" or not ruta.endswith(".csv"):
        print("Ruta inválida.")
        return get_csv()
    return ruta
#-----------------
#Checar csv
def check_csv(ruta):
    df = pd.read_csv(ruta)
    print(df)

#-----------------    
#Modificar csv
def modify_csv(ruta):
    df = pd.read_csv(ruta)
    print("Columnas disponibles:", list(df.columns))#muestra las columnas del csv
    try:
        fila = int(input("Número de fila a modificar de la tabla (chequea el csv sino): "))
        if fila < 0 or fila >= len(df): #checa que la fila exista o concuerde con el csv 
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
    except ValueError:
        print("Entrada inválida.")
#-----------------    
#Guardar cambios en csv
def save_csv(df, ruta):
    df.to_csv(ruta, index=False)
    print("Cambios guardados en", ruta)
#-----------------
# Menú simple
while True:
    print("\n--- MENÚ ---")
    print("1. Insertar CSV")
    print("2. Checar CSV")
    print("3. Modificar CSV")
    print("4. Guardar cambios")
    print("9. [SIN TERMINAR]")
    print("0. Salir")

    opcion = input("Elige una opción: ")
    
    if opcion == "1":
        csv_path = get_csv()
        df = pd.read_csv(csv_path)
        print("✅ CSV cargado.")
    elif opcion == "2":
        print("\n")
        print("-"*20)
        check_csv(csv_path)
        print("-"*20)
    elif opcion == "3":
        modify_csv(csv_path)
    elif opcion == "0":
        print("👋 Saliendo del programa...")
        break
    else:
        print("Opción no válida")