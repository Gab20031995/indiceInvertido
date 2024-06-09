import os
import re
import unicodedata
import datetime

def listar_archivos_en_carpeta(carpeta):
    archivos = []
    for nombre_archivo in os.listdir(carpeta):
        ruta_archivo = os.path.join(carpeta, nombre_archivo)
        if os.path.isfile(ruta_archivo):
            archivos.append(nombre_archivo)
    return archivos

def eliminar_tildes(texto):
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

def normalizar_texto(texto):
    texto = texto.lower()
    texto = eliminar_tildes(texto)
    texto = re.sub(r'[^\w\s\n¡¿]', '', texto)   # Eliminar signos de puntuación excepto saltos de línea
    return texto

def crear_diccionario_archivos(archivos):
    return {archivo: f"{i:04}" for i, archivo in enumerate(archivos, 1)}

def buscar_palabras_en_archivos(carpeta, palabras, diccionario_archivos):
    archivos = listar_archivos_en_carpeta(carpeta)
    resultados = {palabra: [] for palabra in palabras}

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

    # Filtrar palabras prohibidas
    palabras = palabras - forbidden_words

    for fileName in archivos:
        with open(os.path.join(carpeta, fileName), encoding="utf8") as currentFile:
            currentLineNumber = 1
            for line in currentFile:
                clean_line = normalizar_texto(line)
                palabras_linea = set(clean_line.split()) - forbidden_words
                for palabra in palabras:
                    if palabra in palabras_linea:
                        resultados[palabra].append((diccionario_archivos[fileName], currentLineNumber))
                currentLineNumber += 1

    # Filtrar resultados para eliminar palabras con cero coincidencias
    resultados_filtrados = {k: v for k, v in resultados.items() if v}
    return resultados_filtrados

def buscadorArchivos(frase=None):
    carpeta_libros = 'Libros'

    # Obtener lista de archivos y crear diccionario de códigos de 4 dígitos
    archivos_libros = listar_archivos_en_carpeta(carpeta_libros)
    diccionario_archivos = crear_diccionario_archivos(archivos_libros)

    # Solicitar frase al usuario
    frase = input("Introduce la frase a buscar: ")

    # Registrar el tiempo de inicio de la busqueda
    tiempo_inicio = datetime.datetime.now()

    # Dividir la frase en palabras y convertirlas a minúsculas
    palabras = set(normalizar_texto(frase).split())

    # Realizar la busqueda en los archivos
    resultados = buscar_palabras_en_archivos(carpeta_libros, palabras, diccionario_archivos)

    # Registrar el tiempo de finalización de la busqueda
    tiempo_fin = datetime.datetime.now()

    # Calcular el tiempo total de busqueda en milisegundos
    tiempo_total = (tiempo_fin - tiempo_inicio).total_seconds() * 1000
    
    # Mostrar el tiempo de inicio, fin y total de la busqueda en milisegundos
    print("Tiempo de inicio de la busqueda:", tiempo_inicio.strftime("%H:%M:%S"))
    print("Tiempo de finalización de la busqueda:", tiempo_fin.strftime("%H:%M:%S"))
    print("Tiempo total de la busqueda (milisegundos):", tiempo_total)
    for palabra, coincidencias in resultados.items():
            conteo = len(coincidencias)
            print(f"Palabra '{palabra}': {conteo}")

    # Mostrar los resultados de la busqueda
    print(f"Resultados para la frase '{frase}':")
    for palabra, coincidencias in resultados.items():
        print(f"Palabra '{palabra}':")
        if coincidencias:
            for codigo, linea in coincidencias:
                print(f"({codigo},{linea}), ")
        else:
            print("  No se encontró en ningún archivo.")
    
    nombre_archivo = f"resultadosbusqueda-{int(tiempo_fin.timestamp())}.txt"
    with open(nombre_archivo, 'w') as archivo:
        archivo.write("^----------------------------------------------------^\n")
        archivo.write(f"BUSQUEDA POR ARCHIVO\n")
        archivo.write("^----------------------------------------------------^\n")
        archivo.write(f"Resultados para la frase '{frase}':\n")
        archivo.write(f"Tiempo de inicio de la busqueda: {tiempo_inicio.strftime('%H:%M:%S')}.\n")
        archivo.write(f"Tiempo de finalizacion de la busqueda: {tiempo_fin.strftime('%H:%M:%S')}.\n")
        archivo.write(f"Tiempo total de la busqueda (milisegundos): {tiempo_total}.\n")
        archivo.write("^----------------------------------------------------^\n")
        
        for palabra, coincidencias in resultados.items():
            conteo = len(coincidencias)
            archivo.write(f"Palabra '{palabra}': {conteo} veces.\n\n^----------------------------------------------------^\n\n")
        for palabra, coincidencias in resultados.items():
            archivo.write(f"\n\nPalabra '{palabra}':\n\n")    
            for codigo, linea in coincidencias:             
                archivo.write(f"({codigo},{linea}), ")

    print(f"Los resultados de la busqueda se han guardado en el archivo '{nombre_archivo}'.")

if __name__ == "__main__":
    buscadorArchivos()