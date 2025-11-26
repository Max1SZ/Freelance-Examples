def cargar():
    alumnos={}
    for x in range(3):
        dni=int(input("Ingrese el numero de dni:"))
        listamaterias=[]
        continua="s"
        while continua=="s":
            materia=input("Ingrese el nombre de materia que cursa:")
            nota=int(input("Ingrese la nota:"))
            listamaterias.append((materia,nota))
            continua=input("Desea cargar otra materia para dicho alumno [s/n}:")
        alumnos[dni]=listamaterias
    return alumnos


def listar(alumnos):
    for dni in alumnos:
        print("Dni del alumno",dni)
        print("Materias que cursa y notas")
        for nota,materia in alumnos[dni]:
            print(materia,nota)


def consulta_notas(alumnos):
    dni=int(input("Ingrese el dni a consultar:"))
    if dni in alumnos:
        for nota,materia in alumnos[dni]:
            print(materia,nota)


# bloque principal

alumnos=cargar()
listar(alumnos)
consulta_notas(alumnos)   