import math 
# Datos del conjunto original 
total = 10 
aceptaron_total = 5 
no_aceptaron_total = 5 
# Entropía del conjunto original 
p_si = aceptaron_total / total 
p_no = no_aceptaron_total / total 
H_S = - (p_si * math.log2(p_si) + p_no * math.log2(p_no)) 
# Agrupamos edades en rangos: Joven (≤30), Adulto (31–50), Mayor (>50) 
# Datos por grupo: 
# Joven: ID 1, 4, 6, 8 → edades 25, 22, 30, 28 → 4 personas → 0 aceptaron, 4 no 
# Adulto: ID 2, 3, 7, 9, 10 → edades 45, 35, 50, 40, 33 → 5 
# personas → 4 aceptaron, 1 no 
# Mayor: ID 5 → edad 60 → 1 persona → 1 aceptó, 0 no 
# Entropía de cada grupo 
def entropy(p1, p2): 
    total = p1 + p2 
    if total == 0 or p1 == 0 or p2 == 0: 
        return 0.0 
    p1 /= total 
    p2 /= total 
    return - (p1 * math.log2(p1) + p2 * math.log2(p2)) 

# Joven: 0 sí, 4 no 
H_joven = entropy(0, 4) 
# Adulto: 4 sí, 1 no 
H_adulto = entropy(4, 1) 
# Mayor: 1 sí, 0 no 
H_mayor = entropy(1, 0) 
# Entropía ponderada 
H_division = (4/10)*H_joven + (5/10)*H_adulto + (1/10)*H_mayor 
# Ganancia de información 
ganancia_edad = H_S - H_division 
ganancia_edad 
print("H_S: ", H_S) 
print("H_division/entropia ponderada: ", H_division) 
print("ganancia_edad: ", ganancia_edad) 