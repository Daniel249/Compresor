# descompresorp.py
from mpi4py import MPI
import re
import time
import sys

def decompress_text_part(compressed_text, num_to_word):
    # Replace numbers with corresponding words using the dictionary
    def replace_match(match):
        num = match.group(1)
        return num_to_word.get(num, match.group(0))  # Replace if in the dictionary

    decompressed_text = re.sub(r'\{(\d+)\}', replace_match, compressed_text)
    return decompressed_text

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if size < 2:
        if rank == 0:
            print("This program requires at least 2 MPI processes.")
        exit()

    if rank == 0:
        # Process 0: Read the dictionary and the compressed text
        input_file = 'comprimido.ec2'
        input_file = sys.argv[1]
        output_file = 'descomprimido-ec2.txt'

        try:
            with open(input_file, 'r', encoding='utf-8') as file:
                content = file.read()
            encoding_used = 'utf-8'
        except UnicodeDecodeError:
            with open(input_file, 'r', encoding='windows-1252') as file:
                content = file.read()
            encoding_used = 'windows-1252'


        # Separate dictionary and compressed text
        parts = content.split('\n\n', 1)
        if len(parts) < 2:
            print("The input file is not in the expected format.")
            return

        dictionary_part, compressed_text = parts
        dictionary_lines = dictionary_part.strip().split('\n')

        # Create the dictionary from the text
        num_to_word = {}
        for line in dictionary_lines:
            if ':' in line:
                num, word = line.split(':', 1)
                num_to_word[num] = word

        # Divide the compressed text into chunks for each worker
        chunk_size = len(compressed_text) // (size - 1)  # excluding process 0
        for i in range(1, size):
            start = (i - 1) * chunk_size
            end = i * chunk_size if i != size - 1 else len(compressed_text)  # last process takes the remainder
            comm.send((num_to_word, compressed_text[start:end]), dest=i, tag=10 + i)

        # Collect the decompressed text from all workers
        decompressed_text = ''
        for i in range(1, size):
            decompressed_part = comm.recv(source=i, tag=20 + i)
            decompressed_text += decompressed_part

        # Save the decompressed text to the output file
        with open(output_file, 'w', encoding=encoding_used) as file:
            file.write(decompressed_text)

        #print(f"Decompression complete. Output saved to {output_file}")

    else:
        # Worker processes: Receive dictionary and text part, decompress, and send back
        num_to_word, text_part = comm.recv(source=0, tag=10 + rank)
        decompressed_text = decompress_text_part(text_part, num_to_word)
        comm.send(decompressed_text, dest=0, tag=20 + rank)

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    if MPI.COMM_WORLD.Get_rank() == 0:
        print(f"Execution time: {end_time - start_time:.2f} seconds")