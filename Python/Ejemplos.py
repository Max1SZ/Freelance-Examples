# Tipos de datos y declaración de variables
#---------------
entero = 10  # Integer
flotante = 10.5  # Float
cadena = "Hola, Mundo"  # String
booleano = True  # Boolean

#---------------
#ejemplos de sets y diccionarios
#---------------
diccio = {"maxi": "a","pauli": "b"} #en diccionarios los valores tienen otros valores adentro.
sets = {"maxi", "pauli"}#sets son como listas pero eliminan las cosas repetidas
listas = [1, 2, 3, 4] 

print(entero)  # Salida: 10
print(flotante)  # Salida: 10.5
print(cadena)  # Salida: Hola, Mundo
print(booleano)  # Salida: True

#---------------
# Inicialización de variables
nombre = "Juan"
edad = 25
#---------------
# Concatenación en la impresión
print("Hola, " + nombre + ". Tienes " + str(edad) + " años.")
# siempre usa f-strings si vas a poner una variable dentro de un texto.
print(f"Hola, {nombre}. Tienes {edad} años.")


a = 10
b = 5

print(a + b)  # Suma: 15
print(a - b)  # Resta: 5
print(a * b)  # Multiplicación: 50
print(a / b)  # División: 2.0
print(a % b)  # Módulo: 0
print(a ** b)  # Exponente: 100000
print(a // b)  # División entera: 2
#---------------
#Operadores Relacionales
x = 10
y = 20
z = [10, 20, 30, 40]

print(x == y)  # Igual a: False
print(x != y)  # No igual a: True
print(x > y)  # Mayor que: False
print(x < y)  # Menor que: True
print(x >= y)  # Mayor o igual que: False
print(x <= y)  # Menor o igual que: True
print(len(z)) # cuenta cuantos numeros hay en la lista
#---------------
#Operadores Lógicos
verdadero = True
falso = False

print(verdadero and falso)  # AND lógico: False
print(verdadero or falso)  # OR lógico: True
print(not verdadero)  # NOT lógico: False
#---------------
#podes usar "in" o "not in" que actuan como booleanos.
#se puede en listas, strings, sets, diccionarios
word = "manzana"
letter = input("adivinar la letra en la palabra: ")


if letter in word:
    print(f"{letter} si esta")
else:
    print(f"{letter} no esta")
        
#---------------
# Solicitar al usuario que ingrese su nombre
nombre = input("Por favor, ingresa tu nombre: ")

# Solicitar al usuario que ingrese su edad
# Convertimos la entrada a un entero ya que input() devuelve una cadena por defecto
edad = int(input("Por favor, ingresa tu edad: "))

# Solicitar al usuario que ingrese su altura
# Convertimos la entrada a un flotante
altura = float(input("Por favor, ingresa tu altura en metros (ej. 1.75): "))

# Imprimir los valores ingresados
print(f"Nombre: {nombre}")
print(f"Edad: {edad} años")
print(f"Altura: {altura} metros")


'''EJEMPLO COMPLETO'''
# Declaración e inicialización de variables
nombre = "Ana"
edad = 30
altura = 1.65
mensaje = f"{nombre} tiene {edad} años y mide {altura} metros."

# Operaciones aritméticas
suma_edades = edad + 5
producto_altura = altura * 2

# Operadores relacionales y lógicos
es_adulta = edad > 18
puede_votar = es_adulta and edad < 70

# Impresión de resultados
print(mensaje)  # Salida: Ana tiene 30 años y mide 1.65 metros.
print(f"En 5 años, {nombre} tendrá {suma_edades} años.")  # Salida: En 5 años, Ana tendrá 35 años.
print(f"El doble de su altura es {producto_altura} metros.")  # Salida: El doble de su altura es 3.3 metros.
print(f"¿Es adulta? {es_adulta}")  # Salida: ¿Es adulta? True
print(f"¿Puede votar? {puede_votar}")  # Salida: ¿Puede votar? True
#---------------
# Ejemplo básico de if
numero = 10

if numero > 0:
    print("El número es positivo.")
elif numero == 0:
    print("El número es cero.")
else:
    print("El número es negativo.")

# Salida: El número es positivo.
#Alternativamente te introduzco una version mas corta de lo de arriba sin tercera opcion:
resultado = "positivo" if numero > 0 else "negativo"

print(resultado)
#---------------
# Ejemplos básicos de while
contador = 1

while contador <= 5:
    print(f"Contador: {contador}")
    contador += 1  # Incrementar el contador en 1

# Salida: va del 1 al 5
#segundo ejemplo:

food = input("ingrese su comida (presione q para cerrar): ")

while not food == "q":
    print(f"te gusta {food}")
    food = input("ingrese su comida (presione q para cerrar): ")

print("adios")
#---------------
# Otro ejemplo:
name = input("ponga nombre: ")
while name == "":
    print("pone nombre >:(")
    name = input("ponga nombre: ")
print(f"hola {nombre}")
#hasta que no pongas tu nombre, se repetira el que no pusiste nombre
#se queda en bucle si no se pone algo dsps del primer print

#---------------
# Ejemplo básico de for con un rango de números
#el for se compone de (comienzo, final, pasos).
#puede iterar strings, booleanos etc
for i in range(5):
    print(f"Número: {i}")

# Salida: 0 al 4
num = 1234-5678-9101112

for x in num:
    print(x)
#imprime lo que contiene num.
#---------------
# Ejemplo completo combinando if, while y for
# Solicitar un número al usuario
numero = int(input("Ingresa un número positivo menor a 10: "))

# Validar el número ingresado
if numero > 0 and numero < 10:
    print(f"El número {numero} es válido.")
else:
    print("Número no válido. Intenta de nuevo.")
#---------------
# Usar while para contar desde 1 hasta el número ingresado
contador = 1
while contador <= numero:
    print(f"Contador: {contador}")
    contador += 1
#---------------
# Usar for para imprimir los primeros números pares menores que el número ingresado
print("Números pares:")
for i in range(numero):
    if i % 2 == 0:
        print(i)

#la salida diria que 5 es válido, cuenta del 1 al 5 y despues te da los numeros impares 0,2,4
#---------------
#try y except sirven para evitar errores inesperados
#se usan juntos. Ejemplo:
    try:
        x = 10 / 0 #esto da error
    except ZeroDivisionError:
        print("no se puede dividir por 0")
        
#-------- Agosto 2025 Ahorro de lineas----------
#Una nueva funcion, "eval". Se presenta asi:
    print(eval("34+45*12.6/20"))
#Bastante bueno para ahorrar lineas.

#Listas
#---------
cuadrados = [x**2 for x in range(1,11)]
print(cuadrados)
#funcion lambda o anonima o inline
def suma(x,y):
    return x+y
print(suma(1,2))

suma2 = lambda x,y : x+y
print(suma2(1,2))

impares = list(filter(lambda x:x%2,numeros))
print(impares)

numeros = [12,35,55]   

#podemos usar lower o casefold. Es mejor casefold 
nombres = ["ale","Ale \n","Juan","Abel ","Tito"]
nombres_con_a = list(filter(lambda x:x.strip().lower().startswith("a").strip(),nombres))
print(nombres_con_a)
