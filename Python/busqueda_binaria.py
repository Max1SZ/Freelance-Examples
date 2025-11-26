'''lista = [10,3,4,2,6]

for i in range(len(lista)):
    for j in range(len(lista)):
        if lista[i] < lista[j]:
                    lista[i],lista[j] = lista[j],lista[i]
        else:
            lista[i],lista[j] = lista[i],lista[j]

print(lista)'''

 
def busqueda_binaria(lista,objetivo): #lista recibe nuestra lista, objetivo el num que queremos buscar en la lista.
    lista.sort()#ordena la lista, para poder buscar numeros mas grandes
    inicio = 0
    fin = len(lista) - 1
    
    while inicio <= fin:
        medio = (inicio + fin) // 2
        #calcula el punto medio
        if lista[medio] == objetivo:
            return medio # se encuentra lo buscado y devuelve donde esta(su indice)
        elif lista[medio] < objetivo:
            inicio = medio + 1 #busca a la derecha
        else:
            fin = medio - 1 #busca a la izquierda
    
    return -1 #si no encuentra el elemento, practicamente no hace nada.

#Ponemos a prueba la funcion

nums = [1, 3, 5, 7, 20, 40, 15, 4, 21]

valor = int(input("ingrese el numero a buscar:"))

indice = busqueda_binaria(nums, valor)

if indice != -1:
    print(f"el numero {valor} se encuentra en la posicion {indice}")
else:
    print("numero no encontrado")
    