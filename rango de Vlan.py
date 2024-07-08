while True:
    print("Este es un Script para identificar si una VLAN es 'Normal' o 'Extendida'")

    Opcion = int(input("Ingrese el número de VLAN: "))

    if Opcion <= 1005:
        print("Es una VLAN de rango Normal")
    elif Opcion >= 1006 and Opcion <= 4094:
        print("Es una VLAN de rango Extendida")
    else:
        print(f"El número de VLAN {Opcion} está fuera del rango válido")
        print("Porfavor ingrese una opción válida")

    respuesta = input("¿Desea realizar otra consulta? (s/n): ")
    if respuesta.lower() != 's':
        print("Saliendo del Script")
        break