import math
import pandas as pd

# ============================
# FUNCIONES DE ENTROPÍA Y GANANCIA DE INFORMACIÓN
# ============================
def entropia(p, n):
    """Calcula la entropía de un conjunto con p positivos y n negativos"""
    if p == 0 or n == 0:
        return 0
    total = p + n
    p_ratio = p / total
    n_ratio = n / total
    return - (p_ratio * math.log2(p_ratio) + n_ratio * math.log2(n_ratio))

def ganancia_info(total_p, total_n, divisiones):
    """
    Calcula la ganancia de información
    divisiones: lista de tuplas (positivos, negativos)
    """
    entropia_total = entropia(total_p, total_n)
    total = total_p + total_n
    entropia_ponderada = 0
    for (p, n) in divisiones:
        entropia_ponderada += ((p+n)/total) * entropia(p, n)
    return entropia_total, entropia_ponderada, entropia_total - entropia_ponderada

# ============================
# 1. Cargar los datos
# ============================
data = pd.DataFrame({
    "Edad": [24, 38, 29, 45, 52, 33, 41, 27, 36, 31],
    "UsoGB": [2.5, 6.0, 3.0, 8.0, 7.5, 4.0, 5.5, 2.0, 6.5, 3.5],
    "LineaFija": ["No", "Sí", "No", "Sí", "Sí", "No", "Sí", "No", "Sí", "No"],
    "Acepta": ["No", "Sí", "No", "Sí", "Sí", "No", "Sí", "No", "Sí", "No"]
})
print("=== Conjunto de datos ===")
print(data)

# ============================
# 2. Entropía del conjunto original
# ============================
p_total = sum(data["Acepta"] == "Sí")
n_total = sum(data["Acepta"] == "No")
print("\n=== 1. ENTROPÍA DEL CONJUNTO ORIGINAL ===")
print(f"Positivos (Sí): {p_total}, Negativos (No): {n_total}")
print(f"Entropía total: {entropia(p_total, n_total):.4f}")

# ============================
# 3. Evaluar atributos
# ============================

print("\n=== 2. GANANCIA DE INFORMACIÓN POR ATRIBUTO ===")

# ---- Edad agrupada ----
bins_edad = [0, 30, 50, 100]
labels_edad = ["Joven", "Adulto", "Mayor"]
data["EdadGrupo"] = pd.cut(data["Edad"], bins=bins_edad, labels=labels_edad, right=True)

tabla_edad = data.groupby("EdadGrupo")["Acepta"].value_counts().unstack().fillna(0)
divisiones_edad = [(int(row.get("Sí",0)), int(row.get("No",0))) for idx,row in tabla_edad.iterrows()]
ent_total, ent_pond, ganancia = ganancia_info(p_total, n_total, divisiones_edad)
print(f"Edad → Ganancia: {ganancia:.4f}")

# ---- Línea fija ----
tabla_linea = data.groupby("LineaFija")["Acepta"].value_counts().unstack().fillna(0)
divisiones_linea = [(int(row.get("Sí",0)), int(row.get("No",0))) for idx,row in tabla_linea.iterrows()]
ent_total, ent_pond, ganancia = ganancia_info(p_total, n_total, divisiones_linea)
print(f"Línea fija → Ganancia: {ganancia:.4f}")

# ---- Uso de datos agrupado ----
bins_datos = [0, 3, 6, 100]
labels_datos = ["Bajo", "Medio", "Alto"]
data["UsoGrupo"] = pd.cut(data["UsoGB"], bins=bins_datos, labels=labels_datos, right=True)

tabla_datos = data.groupby("UsoGrupo")["Acepta"].value_counts().unstack().fillna(0)
divisiones_datos = [(int(row.get("Sí",0)), int(row.get("No",0))) for idx,row in tabla_datos.iterrows()]
ent_total, ent_pond, ganancia = ganancia_info(p_total, n_total, divisiones_datos)
print(f"Uso de datos → Ganancia: {ganancia:.4f}")

# ============================
# 4. Conclusión y construcción del árbol
# ============================

print("\n=== 3. CONSTRUCCIÓN DEL ÁRBOL ===")
print("Se elige como nodo raíz el atributo con mayor ganancia de información.")
print("Luego, se repite el proceso dentro de cada rama.")

print("\n=== 4. CONCLUSIÓN ===")
print("El atributo con mayor ganancia de información es el mejor para empezar el árbol.\
      Este atributo permitirá predecir si un cliente aceptará la oferta dividiendo los datos\
      en grupos más homogéneos.") 
