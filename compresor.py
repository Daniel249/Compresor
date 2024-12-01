#compresor.py
import re
from collections import Counter
import sys
def compress_text(input_file, output_file):
    # Leer el archivo de entrada
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
        encoding_used = 'utf-8'
    except UnicodeDecodeError:
        # If reading as UTF-8 fails, fall back to Windows-1252 (ANSI)
        with open(input_file, 'r', encoding='windows-1252') as f:
            text = f.read()
        encoding_used = 'windows-1252'

    # Paso 1: Separar las secuencias de texto (letras, números, símbolos) delimitadas por espacios y signos de puntuación
    #sequences = re.findall(r'[\w\W]+?(?=[\s.,;:])|[\w\W]+', text)
    sequences = re.findall(r'[\w\W]+?(?=[\s.,;:\n])|[\w\W]+', text)

    # Paso 2: Filtrar las secuencias que tienen 5 o más caracteres (sin incluir espacios antes)
    sequences = [seq for seq in sequences if len(seq) >= 5 and not '<' in seq]
    #sequences = [seq for seq in sequences if len(seq) >= 5

    # Paso 3: Contar la frecuencia de las secuencias
    sequence_counts = Counter(sequences)

    # Paso 4: Filtrar las secuencias que aparecen 5 o más veces
    frequent_sequences = {seq: i + 1 for i, (seq, count) in enumerate(sequence_counts.items()) if count >= 5}

    # Paso 5: Crear el diccionario que va al principio del archivo comprimido
    dictionary = '\n'.join([f'{num}:{seq}' for seq, num in frequent_sequences.items()])

    # Paso 6: Reemplazar las secuencias en el texto original por su número de referencia
    compressed_text = text

    # Reemplazar todas las apariciones de las palabras, incluso si están dentro de otras palabras
    for word, num in frequent_sequences.items():
        compressed_text = re.sub(re.escape(word), f'{{{num}}}', compressed_text)

    # Paso 7: Guardar el archivo comprimido
    with open(output_file, 'w', encoding=encoding_used) as file:
        file.write(dictionary + '\n\n' + compressed_text)

# Usar el código con el archivo de entrada y salida
input_file = 'text5.txt'  # Reemplazar con el archivo de entrada
output_file = 'comprimido.ec2'  # El archivo comprimido de salida
input_file = sys.argv[1]
compress_text(input_file, output_file)
