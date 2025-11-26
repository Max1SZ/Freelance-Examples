import pandas as pd
ventas = pd.read_csv("C:/Users/estudiante/Desktop/TareasPYTHON/2025/ventas.csv")
facturas_encabezado = pd.read_csv("C:/Users/estudiante/Desktop/TareasPYTHON/2025/facturas_enc.csv")
'''
clientes = pd.read_csv("C:/Users/estudiante/Desktop/TareasPYTHON/2025/clientes.csv")

ventas_clientes = pd.merge(ventas, facturas_encabezado, on="id_sucursal", how="left")
ventas_clientes = pd.merge(ventas_clientes, clientes, on="id_cliente", how="left")
#print(ventas_clientes.columns.tolist()) #para checar la tabla. 
#print(ventas_clientes[['id_factura', 'fecha_y', 'nombre', 'total']].head())'''
fac_det = pd.read_csv("C:/Users/estudiante/Desktop/TareasPYTHON/2025/facturas_det.csv") 


print("-"*12)
print("Columnas en ventas:", ventas.columns.tolist())
print("Columnas en facturas_det:", fac_det.columns.tolist())

