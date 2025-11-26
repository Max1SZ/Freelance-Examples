#-----------
#
#VERSION EXPERIMENTAL. Solo de prueba. por ahora.
#
#---------
import os #interactua con el sistema operativo, por eso el nombre.
import sys #interactua con python y su interprete
import pandas as pd
import sqlalchemy
from typing import List
from sqlalchemy import create_engine, text, MetaData, Table
from sqlalchemy.engine import Engine
from sqlalchemy.dialects.mysql import insert as mysql_insert
#importamos librerias (asegurate de descargarlas)

#config de BD
dbhost = "localhost"
dbuser = "root"
dbpass = "" 
dbname = "prueba1"

#elegir csv y deducir de donde viene
def get_engine() -> Engine:
    uri = f"mysql+pymysql://{dbuser}:{dbpass}@{dbhost}/{dbname}"
    return create_engine(uri,future=True)

engine = get_engine()
print(f"Bien! Conexion a {dbname} exitosa!")

def get_csv() -> str:
    ruta = input("Inserte ruta del CSV a cargar (ej: clientes.csv):").strip().strip('"').strip("'")
    if not os.path.exists(ruta):
        print("no existe el archivo.")
        sys.exit(1)
    return ruta

def get_csvs() -> List[str]:
    rutas = input("Inserte rutas de los CSV a cargar (separadas por coma): ").split(",")
    rutas = [r.strip().strip('"').strip("'") for r in rutas if r.strip()]
    for ruta in rutas:
        if not os.path.exists(ruta):
            print(f"No existe el archivo: {ruta}")
            sys.exit(1)
    return rutas

csv_paths = get_csvs()

for csv_path in csv_paths:
    table_name = os.path.splitext(os.path.basename(csv_path))[0]
    print(f"\nCargando tabla del destino: {dbname}.{table_name}")

    df = pd.read_csv(csv_path)
    print("\n vista rapida(primeras filas):")
    print(df.head())
    print("\n columnas detectadas:")
    print(list(df.columns))

    #inspecciona la tabla en mysql (columnas y PKs)
    #nos deja hacer upsert sin tener que hacerlo manualmente en sql
    def info_tabla(engine: Engine, schema: str, table: str):
        # Columnas
        cols = pd.read_sql(
            text("""
            SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = :s AND TABLE_NAME = :t
            ORDER BY ORDINAL_POSITION
            """),
            engine, params={"s": schema, "t": table}
        )["COLUMN_NAME"].tolist()

        # PK (puede ser compuesta)
        pk = pd.read_sql(
            text("""
            SELECT k.COLUMN_NAME
            FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS t
            JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE k
              ON t.CONSTRAINT_NAME = k.CONSTRAINT_NAME
             AND t.TABLE_SCHEMA = k.TABLE_SCHEMA
             AND t.TABLE_NAME = k.TABLE_NAME
            WHERE t.CONSTRAINT_TYPE = 'PRIMARY KEY'
              AND t.TABLE_SCHEMA = :s
              AND t.TABLE_NAME = :t
            ORDER BY k.ORDINAL_POSITION
            """),
            engine, params={"s": schema, "t": table}
        )["COLUMN_NAME"].tolist()

        # Siempre retornar listas, aunque estén vacías
        return cols, pk

    table_cols, pk_cols = info_tabla(engine, dbname, table_name)
    if not table_cols:
        print(f"La tabla {table_name} no existe en la base {dbname}. Créala o exportá el CSV de una tabla existente.")
        continue

    print("Columnas en la tabla:", table_cols)
    print("Clave primaria:", pk_cols if pk_cols else "(no definida)")

    #ahora alineamos columnas
    #descartamos columnas extra, reordenamos la tabla, advertimos si faltan columnas
    extras = [c for c in df.columns if c not in table_cols]
    if extras:
       print("columnas extra en CSV(se descartan):", extras)
       df = df.drop(columns = extras)
    #columnas faltantes
    faltantes = [c for c in table_cols if c not in df.columns]
    if faltantes:
       print("columnas faltantes!! (se completaran como null al subir): ", faltantes)
        #agregamos columnas faltantes vacias
    for c in faltantes:
        df[c] = pd.NA
    #reodernmaos columnas en la tabla
    df = df[table_cols]

    #Menu CRUD, osea, agregar/modificar/eliminar(solo en el csv, no afecta a SQL asi no pasa nada con las FK)
    def imprimir_df(dfi: pd.DataFrame, n:int=10):
        print("\n DataFrame (primeras filas):")
        print(dfi.head(n))
        print(f"(filas: {len(dfi)}, columnas: {list(dfi.columns)})")

    def agregar_fila(dfi: pd.DataFrame):
        print("\n Agregar fila:")
        nueva = {}
        for col in dfi.columns:
            val = input(f"  {col} = ")
            nueva[col] = None if val == "" else val
        return pd.concat([dfi, pd.DataFrame([nueva])], ignore_index=True)

    def modificar_celda(dfi: pd.DataFrame):
        print("\n Modificar celda (usa el índice que ves en la primera columna imprimida)")
        try:
            idx = int(input("  índice de fila = "))
            if idx < 0 or idx >= len(dfi):
                print("  índice inválido")
                return dfi
            col = input(f"  columna a cambiar (opciones: {', '.join(dfi.columns)}) = ").strip()
            if col not in dfi.columns:
                print("  columna inválida")
                return dfi
            val = input("  nuevo valor (vacío = NULL) = ")
            dfi.at[idx, col] = None if val == "" else val
        except ValueError:
            print("  entrada inválida")
        return dfi

    def eliminar_fila(dfi: pd.DataFrame):
        print("\n Eliminar fila (esto NO elimina en SQL con UPSERT).")
        try:
            idx = int(input("  índice de fila = "))
            if idx < 0 or idx >= len(dfi):
                print("  índice inválido")
                return dfi
            dfi = dfi.drop(index=idx).reset_index(drop=True)
        except ValueError:
            print("  entrada inválida")
        return dfi

    #Diccionario para agregar multiples csv
    archivos = {}


while True:
    imprimir_df(df, n=5)
    # Menú inicial para elegir modo de carga
    print("\n¿Desea cargar uno o varios CSV?")
    print("1) Un solo CSV")
    print("2) Varios CSV")
    modo = input("Opción: ").strip()

    if modo == "1":
        csv_paths = [get_csv()]
    elif modo == "2":
        csv_paths = get_csvs()
    else:
        print("Opción inválida.")
        sys.exit(1)

    print("\n--- MENÚ ---")
    print("1) Agregar fila")
    print("2) Modificar celda")
    print("3) Eliminar fila (solo en CSV/DF)")
    print("4) Guardar CSV")
    print("5) Enviar a la base (UPSERT por PK)")
    print("0) Salir")
    op = input("Opción: ").strip()

    if op == "1":
        df = agregar_fila(df)
    elif op == "2":
        df = modificar_celda(df)
    elif op == "3":
        df = eliminar_fila(df)
    elif op == "4":
        df.to_csv(csv_path, index=False)
        print(f"Guardado en {csv_path}")
    elif op == "5":
        break  # salimos del bucle y hacemos UPSERT abajo
    elif op == "0":
        print("Salida sin enviar a base.")
        sys.exit(0)
    else:
        print("Opción inválida")

#Upsert en python para no afectar FKs
def upsert_df(engine: Engine, schema: str, table: str, dfi: pd.DataFrame, pk_cols: List[str]):
    if not pk_cols:
        print("❌ No hay PK definida; no se puede hacer UPSERT. Usá la opción de reemplazar tabla (con cuidado).")
        return

    meta = MetaData()
    t = Table(table, meta, autoload_with=engine, schema=schema)

    # Solo enviamos columnas que existen en la tabla
    send_cols = [c.name for c in t.columns if c.name in dfi.columns]
    data = dfi[send_cols].to_dict(orient="records")

    # SET para ON DUPLICATE: todas menos las PK
    non_pk_cols = [c for c in send_cols if c not in pk_cols]
    if not non_pk_cols:
        print("⚠️ La PK cubre todas las columnas; nada que actualizar. Se harán INSERT IGNORE implícitos.")
    with engine.begin() as conn:
        stmt = mysql_insert(t).values(data)
        if non_pk_cols:
            update_map = {c: stmt.inserted[c] for c in non_pk_cols}
            stmt = stmt.on_duplicate_key_update(**update_map)
        conn.execute(stmt)
    print("✅ UPSERT completado (insert/update por PK).")

#Ejecutar acciones
# ¿Qué opción eligió el usuario al salir del menú?
if op == "5":
    upsert_df(engine, dbname, table_name, df, pk_cols)
else:
    # llegó aquí por salir sin guardar
    pass

print("🏁 Listo.")
