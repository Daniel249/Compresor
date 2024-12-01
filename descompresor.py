#descompresor.py
import re
import time
import sys
def decompress_text(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        encoding_used = 'utf-8'
    except UnicodeDecodeError:
        # If reading as UTF-8 fails, fall back to Windows-1252 (ANSI)
        with open(input_file, 'r', encoding='windows-1252') as f:
            content = f.read()
        encoding_used = 'windows-1252'

    # Separar el diccionario y el texto comprimido
    parts = content.split('\n\n', 1)  # Divide en dos partes: diccionario y texto comprimido
    if len(parts) < 2:
        print("El archivo no tiene el formato esperado.")
        return
    
    dictionary_part, compressed_text = parts
    # dictionary into array
    dictionary_lines = dictionary_part.strip().split('\n')

    # generate dictionary from each entry in array
    num_to_word = {}
    for line in dictionary_lines:
        if ':' in line:
            num, word = line.split(':', 1)
            num_to_word[num] = word

    # Reemplazar los números en el texto comprimido por las palabras del diccionario
    def replace_match(match):
        num = match.group(1)
        return num_to_word.get(num, match.group(0))  # Reemplaza si está en el diccionario

    decompressed_text = re.sub(r'\{(\d+)\}', replace_match, compressed_text)

    # Guardar el texto descomprimido en el archivo de salida
    with open(output_file, 'w', encoding=encoding_used) as file:
        file.write(decompressed_text)

# Usar el código con el archivo de entrada y salida
input_file = 'comprimido.ec2'  # Reemplazar con el archivo comprimido
#input_file = sys.argv[1]
output_file = 'descomprimido-ec2.txt'  # El archivo descomprimido de salida
start_time = time.time()
decompress_text(input_file, output_file)
end_time = time.time()
execution_time = end_time - start_time
print(f"Tiempo de ejecución: {execution_time:.2f} segundos")
