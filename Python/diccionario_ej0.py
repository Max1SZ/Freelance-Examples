


def imprimir(paises):
    for clave in paises:
        print(clave, paises[clave])

#esto muestra una lista y su version con set mediante un comando "set" en vez de hacerlo a mano.
mi_lista = [1, 5, 3, 2, 5, 3, 4]
print (f"lista comun: {mi_lista}")
print("-"*20)

mi_set = set(mi_lista)

print(f"lista con set: {mi_set}")
print("-"*20)
#definir un diccionario que almacene los nombres de paises
#como clave y como valor la cantidad de habitantes. De ahi sale el def imprimir

paises={"argentina":40000000, "españa":46000000, "brasil":190000000, "uruguay": 3400000}
imprimir(paises)


