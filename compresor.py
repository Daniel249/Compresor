#compresor.py
import re
from collections import Counter
import sys

def compact_dict_keys(input_dict, start_from=0):
    return {new_key: value for new_key, (_, value) in enumerate(input_dict.items(), start=start_from)}


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
    #sequences = re.findall(r'[\w\W]+?(?=[\s.,;:\n])|[\w\W]+', text)
    #sequences = re.findall(r'\b\w+\b', text)

    # Step 1: Find all sequences (words)
    sequences = re.findall(r'(?<!\w)\w+(?!\w)', text)

    # Step 2: Filter sequences with 5 or more characters and exclude those containing '<'
    sequences = [seq for seq in sequences if len(seq) >= 6 and '<' not in seq]

    # Step 3: Count the frequency of each sequence
    sequence_counts = Counter(sequences)

    # Step 4: Filter sequences that appear 5 or more times
    frequent_sequences = {seq: count for seq, count in sequence_counts.items() if count >= 5}

    # Step 5: Create the compacted dictionary (words as keys and consecutive integers as values)
    compacted_frequent_sequences = {seq: i for i, seq in enumerate(frequent_sequences.keys())}

    # Step 6: Create the dictionary string to write to the compressed file (using compacted keys)
    dictionary = '\n'.join([f'{num}:{seq}' for seq, num in compacted_frequent_sequences.items()])

    # Step 7: Reemplazar las secuencias en el texto original por su número de referencia
    compressed_text = text
    print(len(compacted_frequent_sequences))
    # Reemplazar todas las apariciones de las palabras, incluso si están dentro de otras palabras
    for word, num in compacted_frequent_sequences.items():
        compressed_text = re.sub(re.escape(word), f'{{{str(num)}}}', compressed_text)

    # Paso 7: Guardar el archivo comprimido
    with open(output_file, 'w', encoding=encoding_used) as file:
        file.write(dictionary + '\n\n' + compressed_text)

# Usar el código con el archivo de entrada y salida
input_file = 'text1.txt'  # Reemplazar con el archivo de entrada
output_file = 'comprimido.ec2'  # El archivo comprimido de salida
input_file = sys.argv[1]
compress_text(input_file, output_file)
