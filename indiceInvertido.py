import os
import re
import pickle
import unicodedata

def listar_archivos_en_carpeta(carpeta, extension=".txt"):
    archivos = []
    for nombre_archivo in os.listdir(carpeta):
        if nombre_archivo.endswith(extension):
            archivos.append(nombre_archivo)
    return archivos

def eliminar_tildes(texto):
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

def normalizar_texto(texto):
    texto = texto.lower()
    texto = eliminar_tildes(texto)
    texto = re.sub(r'[^\w\s\n¡¿]', '', texto)   # Eliminar signos de puntuación
    return texto

def crear_indice_invertido(carpeta_libros, lista_archivos, diccionario_libros):
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
        'está', 'estad', 'he', 'has', 'ha', 'hemos','han', 'haya',
        'soy', 'eres', 'es', 'somos', 'sois', 'son','sea', 'seas', 
        'seamos', 'sean', 'seré', 'serás','será', 'seremos', 'seréis', 
        'serán', 'sería'])
    indice_palabras = {}

    for fileName in lista_archivos:
        file_id = diccionario_libros[fileName]
        with open(os.path.join(carpeta_libros, fileName), encoding="utf8") as currentFile:
            current_line_number = 1            
            for line in currentFile:
                clean_line = normalizar_texto(line)
                words = re.split(r'\s+', clean_line)  # Separar por espacios y caracteres de nueva línea

                for word in words:
                    if word and word not in forbidden_words:
                        if word in indice_palabras:
                            indice_palabras[word].append((file_id, current_line_number))
                        else:
                            indice_palabras[word] = [(file_id, current_line_number)]

                current_line_number += 1

    return indice_palabras

def guardar_indice(indice_palabras):
    with open('indicePalabras.data', 'wb') as f:
        pickle.dump(indice_palabras, f, pickle.HIGHEST_PROTOCOL)

def main():
    # Carpeta que contiene los libros
    carpeta_libros = 'Libros'
    
    # Verifica si la carpeta existe
    if not os.path.exists(carpeta_libros):
        print(f"La carpeta {carpeta_libros} no existe.")
        return
    
    # Genera la lista de archivos en la carpeta
    archivos_libros = listar_archivos_en_carpeta(carpeta_libros)
    
    # Crear el diccionario con un valor numérico de 4 dígitos para cada archivo
    diccionario_libros = {archivo: f"{i:04}" for i, archivo in enumerate(archivos_libros, 1)}
    
    # Crear el índice invertido
    indice = crear_indice_invertido(carpeta_libros, archivos_libros, diccionario_libros)
    
    # Guardar el índice invertido
    guardar_indice(indice)
    print("task Completed")
main()



#Visualizar muestra
#def cargar_indice():
#    with open('indicePalabras.data', 'rb') as f:
#        indice_palabras = pickle.load(f)
#    return indice_palabras

#def main():
#    indice = cargar_indice()
# Muestra las primeras 25 palabras 
#    for palabra, ocurrencias in list(indice.items())[:25]:  
#        print(f"{palabra}: {ocurrencias}\n")
#main()