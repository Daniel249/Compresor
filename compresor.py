#compresor.py
import re
from collections import Counter
import sys
import time

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
    # encontrar todas las palabras en un array
    sequences = re.findall(r'(?<!\w)\w+(?!\w)', text)
    # remove short words
    sequences = [seq for seq in sequences if len(seq) >= 6 and '<' not in seq]
    sequence_counts = Counter(sequences)
    # create dictionary 
    frequent_sequences = {seq: count for seq, count in sequence_counts.items() if count >= 5}
    compacted_frequent_sequences = {seq: i for i, seq in enumerate(frequent_sequences.keys())}
    dictionary = '\n'.join([f'{num}:{seq}' for seq, num in compacted_frequent_sequences.items()])

    compressed_text = text
    # print(len(compacted_frequent_sequences))

    for word, num in compacted_frequent_sequences.items():
        compressed_text = re.sub(re.escape(word), f'{{{str(num)}}}', compressed_text)

    # Guardar el archivo comprimido
    with open(output_file, 'w', encoding=encoding_used) as file:
        file.write(dictionary + '\n\n' + compressed_text)

# Usar el código con el archivo de entrada y salida
#input_file = 'text1.txt'  # Reemplazar con el archivo de entrada
output_file = 'comprimido.ec2'  # El archivo comprimido de salida
input_file = sys.argv[1]
start_time = time.time()
compress_text(input_file, output_file)
end_time = time.time()
execution_time = end_time - start_time
print(f"Tiempo de ejecución: {execution_time:.2f} segundos")