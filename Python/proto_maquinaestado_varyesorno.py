nums = {"while", "for", "def"}

valor = input("prototipo, M.Estado validador de variables\n-------\ningrese el nombre para su variable:")


if valor not in nums:
    print("-"*20)
    print(f"nombre valido")

else:
    print("nombre no valido")
    