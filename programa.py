from buscadorIndice import buscadorIndice
from buscadorArchivos import buscadorArchivos

def main():
    while True:
        print("Menú: \n")
        print("a. Buscar en todos los archivos")
        print("b. Buscar por medio de índice")
        print("c. Comparar resultados")
        print("d. Salir \n")

        opcion = input("Seleccione una opción para continuar: ")
        print("^----------------------------------------------------^")

        if opcion == "a":
            while True:
                buscadorArchivos(frase=None)
                respuesta = input("¿Desea realizar otra búsqueda? (s/n): ")
                if respuesta.lower() != "s":
                    break

        elif opcion == "b":
            while True:
                buscadorIndice(frase=None)
                respuesta = input("¿Desea realizar otra búsqueda? (s/n): ")
                if respuesta.lower() != "s":
                    break
        
        
        elif opcion == "c":
            print("pppp")


        elif opcion == "d":
            print("Fin del programa!")
            print("^----------------------------------------------------^")
            break
        else:
            print("Alerta!!! Opción no válida. Por favor, elija una de las opciones anteriores.")
            print("^----------------------------------------------------^")

if __name__ == "__main__":
    main()
