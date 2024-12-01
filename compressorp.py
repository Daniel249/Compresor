# compresorp.py
from mpi4py import MPI
import re
import sys
from collections import Counter
import time

def generate_dictionary(text):
    # encuentra secuencias de texto
    #sequences = re.findall(r'[\w\W]+?(?=[\s.,;:\n])|[\w\W]+', text)
    sequences = re.findall(r'(?<!\w)\w+(?!\w)', text)
    sequences = [seq for seq in sequences if len(seq) >= 6 and '<' not in seq]

    # Cuenta la frecuencia de las secuencias
    sequence_counts = Counter(sequences)

    # Diccionario filtra secuencias de palabras mayor a 5
    #dictionary = {seq: i for i, (seq, count) in enumerate(sequence_counts.items()) if count >= 5}

    filtered_sequences = {seq: count for seq, count in sequence_counts.items() if count >= 5}

    # Paso 2 crear un diccionario compacto donde las palabras y simbolos tienen una representacion enumerada
    compacted_dictionary = {seq: i for i, seq in enumerate(filtered_sequences.keys())}
    return compacted_dictionary

def replace_with_dictionary(text, dictionary):
    # Reemplaza las palabras dentro del diccionario
    for word, num in dictionary.items():
        text = re.sub(re.escape(word), f'{{{num}}}', text)
    return text

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Asegurar al menos 2 procesos, 1 para organizar y otro para ejecutar
    if size < 2:
        if rank == 0:
            print("This program requires at least 2 MPI processes.")
        exit()

    if rank == 0:
        # Proceso 0: lee el texto y establece un dicionario
        start_time = time.time()
        input_file = 'LaBiblia.txt'
        input_file = sys.argv[1]
        try:
            with open(input_file, 'r', encoding='utf-8') as file:
                text = file.read()
            encoding_used = 'utf-8'
        except UnicodeDecodeError:
            with open(input_file, 'r', encoding='windows-1252') as file:
                text = file.read()
            encoding_used = 'windows-1252'

        # genera un diccionario
        dictionary = generate_dictionary(text)

        # Prepara y distribuye los chunks dentro del diccionario
        chunk_size = len(text) // (size - 1)
        for i in range(1, size):
            start = (i - 1) * chunk_size
            end = i * chunk_size if i != size - 1 else len(text)  # El ultimo proceso del remanente
            comm.send((text[start:end], dictionary), dest=i, tag=10 + i)

        # Tomar los chunks procesados
        processed_chunks = []
        for i in range(1, size):
            processed_chunk = comm.recv(source=i, tag=20 + i)
            processed_chunks.append(processed_chunk)

        # Combinar todos los chunks procesados
        combined_text = ''.join(processed_chunks)

        # Escribir la salida final
        output_file = 'comprimido.ec2'
        with open(output_file, 'w', encoding=encoding_used) as file:
            file.write('\n'.join(f'{num}:{word}' for word, num in dictionary.items()) + '\n\n')
            file.write(combined_text)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Tiempo de ejecución: {execution_time:.2f} segundos")

    else:
        # Procesos de trabajador agrupa el texto y los envia
        text_part, dictionary = comm.recv(source=0, tag=10 + rank)
        compressed_text = replace_with_dictionary(text_part, dictionary)
        comm.send(compressed_text, dest=0, tag=20 + rank)

if __name__ == "__main__":
    main()
