import pickle
import datetime

def cargar_indice():
    try:
        with open('indicePalabras.data', 'rb') as archivo:
            indice = pickle.load(archivo)
        return indice
    except FileNotFoundError:
        print("El archivo 'indicePalabras.data' no se encontró.")
        return {}
    except (pickle.UnpicklingError, EOFError) as e:
        print(f"Error al deserializar el archivo: {e}")
        return {}

def buscar_palabras(indice, palabras):
    resultados = {}
    lineas_coincidentes = []
    for palabra in palabras:
        resultado = indice.get(palabra, "No se encontró en el índice.")
        if resultado != "No se encontró en el índice.":
            resultados[palabra] = resultado
            lineas_coincidentes.extend(resultado)
    return resultados, lineas_coincidentes

def buscadorIndice(frase=None):
    # Cargar el índice desde el archivo
    indice = cargar_indice()

    if not indice:
        print("No se pudo cargar el índice.")
        return

    # Lista de palabras prohibidas
    forbidden_words = set([
        'de', 'la', 'que', 'el', 'en',
        'y', 'a', 'los', 'del', 'se', 'las', 'por', 'un', 
        'para', 'con', 'una', 'su', 'al', 'lo', 'como', 'más', 
        'pero', 'sus', 'le', 'ya', 'o', 'este', 'sí', 'porque', 
        'esta','muy', 'sin', 'me', 'hay', 'nos', 'uno', 'les', 
        'ni','otros', 'ese', 'eso', 'ante', 'ellos', 'e', 'esto', 
        'mí', 'qué', 'unos', 'yo', 'otro', 'otras', 'otra', 'él', 
        'esa', 'estos', 'mucho', 'nada', 'muchos', 'cual', 'poco',
        'ella', 'estar', 'estas', 'algunas', 'algo', 'mi', 'mis', 
        'tú', 'te', 'ti', 'tu', 'tus', 'ellas', 'os', 'mío', 'mía',
        'míos', 'mías', 'tuyo', 'tuya', 'tuyos', 'tuyas', 'suyo', 
        'suya', 'suyos', 'suyas', 'esos', 'esas', 'estoy', 'estás',
        'está', 'estad', 'he', 'has', 'ha', 'hemos', 'habéis', 
        'han', 'haya', 'soy', 'eres', 'es', 'somos', 'sois', 'son',
        'sea', 'seas', 'seamos', 'seáis', 'sean', 'seré', 'serás',
        'será', 'seremos', 'seréis', 'serán', 'sería'])

    # Solicitar frase al usuario
    frase = input("Introduce la frase a buscar: ")

    # Registrar el tiempo de inicio de la busqueda
    tiempo_inicio = datetime.datetime.now()

    # Dividir la frase en palabras y convertirlas a minúsculas
    palabras = set(frase.lower().split()) - forbidden_words

    # Realizar la busqueda
    resultados, lineas_coincidentes = buscar_palabras(indice, palabras)

    # Registrar el tiempo de finalizacion de la busqueda
    tiempo_fin = datetime.datetime.now()

    # Calcular el tiempo total de busqueda en milisegundos
    tiempo_total = (tiempo_fin - tiempo_inicio).total_seconds() * 1000

    conteo_resultados = {}
    for palabra, resultado in resultados.items():
        if resultado != "No se encontró en el índice.":
            conteo_resultados[palabra] = sum(1 for _ in resultado)

    # Mostrar los resultados de la busqueda
    print(f"Resultados para la frase '{frase}':")
    for palabra, resultado in resultados.items():
        print(f"Palabra '{palabra}': {resultado}")

    # Mostrar el tiempo de inicio, fin y total de la busqueda en milisegundos
    print("Tiempo de inicio de la busqueda:", tiempo_inicio.strftime("%H:%M:%S"))
    print("Tiempo de finalizacion de la busqueda:", tiempo_fin.strftime("%H:%M:%S"))
    print("Tiempo total de la busqueda (milisegundos):", tiempo_total)

    nombre_archivo = f"resultadosbusqueda-{int(tiempo_fin.timestamp())}.txt"
    with open(nombre_archivo, 'w') as archivo:
        archivo.write("^----------------------------------------------------^\n")
        archivo.write(f"BUSQUEDA POR INDICE\n")
        archivo.write("^----------------------------------------------------^\n")
        archivo.write(f"Resultados para la frase '{frase}':\n")
        for palabra, resultado in resultados.items():
            conteo = conteo_resultados.get(palabra, 0)
            archivo.write(f"Palabra '{palabra}': {conteo} veces.\n")
        archivo.write(f"Tiempo de inicio de la busqueda: {tiempo_inicio.strftime('%H:%M:%S')}.\n")
        archivo.write(f"Tiempo de finalizacion de la busqueda: {tiempo_fin.strftime('%H:%M:%S')}.\n")
        archivo.write(f"Tiempo total de la busqueda (milisegundos): {tiempo_total}.\n")
        archivo.write("^----------------------------------------------------^\n")
        for palabra, resultado in resultados.items():
            archivo.write(f"Palabra '{palabra}': {resultado}\n\n^----------------------------------------------------^\n\n")

    print(f"Los resultados de la busqueda se han guardado en el archivo '{nombre_archivo}'.")

if __name__ == "__main__":
    buscadorIndice()



