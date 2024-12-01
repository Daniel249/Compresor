# compresorp.py
from mpi4py import MPI
import re
import sys
from collections import Counter
import time

def generate_dictionary(text):
    # Find sequences of text
    #sequences = re.findall(r'[\w\W]+?(?=[\s.,;:\n])|[\w\W]+', text)
    sequences = re.findall(r'(?<!\w)\w+(?!\w)', text)
    sequences = [seq for seq in sequences if len(seq) >= 6 and '<' not in seq]

    # Count the frequency of sequences
    sequence_counts = Counter(sequences)

    # Filter sequences appearing 5 or more times
    #dictionary = {seq: i for i, (seq, count) in enumerate(sequence_counts.items()) if count >= 5}

    filtered_sequences = {seq: count for seq, count in sequence_counts.items() if count >= 5}

    # Step 2: Create a compacted dictionary where the keys are words (sequences) and the values are compacted integers
    compacted_dictionary = {seq: i for i, seq in enumerate(filtered_sequences.keys())}
    return compacted_dictionary

def replace_with_dictionary(text, dictionary):
    # Replace words in the text based on the dictionary
    for word, num in dictionary.items():
        text = re.sub(re.escape(word), f'{{{num}}}', text)
    return text

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Ensure we have at least 2 processes (1 for coordination, others for work)
    if size < 2:
        if rank == 0:
            print("This program requires at least 2 MPI processes.")
        exit()

    if rank == 0:
        # Process 0: Read the file and generate the dictionary
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

        # Generate the dictionary
        dictionary = generate_dictionary(text)

        # Prepare and distribute chunks of text and the dictionary
        chunk_size = len(text) // (size - 1)
        for i in range(1, size):
            start = (i - 1) * chunk_size
            end = i * chunk_size if i != size - 1 else len(text)  # the last process takes the remainder
            comm.send((text[start:end], dictionary), dest=i, tag=10 + i)

        # Collect processed chunks
        processed_chunks = []
        for i in range(1, size):
            processed_chunk = comm.recv(source=i, tag=20 + i)
            processed_chunks.append(processed_chunk)

        # Combine all processed chunks
        combined_text = ''.join(processed_chunks)

        # Write the final output
        output_file = 'comprimido.ec2'
        with open(output_file, 'w', encoding=encoding_used) as file:
            file.write('\n'.join(f'{num}:{word}' for word, num in dictionary.items()) + '\n\n')
            file.write(combined_text)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Tiempo de ejecución: {execution_time:.2f} segundos")

    else:
        # Worker processes: Receive text and dictionary, process, and send back
        text_part, dictionary = comm.recv(source=0, tag=10 + rank)
        compressed_text = replace_with_dictionary(text_part, dictionary)
        comm.send(compressed_text, dest=0, tag=20 + rank)

if __name__ == "__main__":
    main()
