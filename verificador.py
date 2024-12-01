#verificador.py
import time
import sys
def are_files_identical(file1, file2):
    try:
        try:
            with open(file1, 'r', encoding='utf-8') as f1:
                content1 = f1.read()
            encoding1 = 'utf-8'
        except UnicodeDecodeError:
            with open(file1, 'r', encoding='windows-1252') as f1:
                content1 = f1.read()
            encoding1 = 'windows-1252'

        try:
            with open(file2, 'r', encoding='utf-8') as f2:
                content2 = f2.read()
            encoding2 = 'utf-8'
        except UnicodeDecodeError:
            with open(file2, 'r', encoding='windows-1252') as f2:
                content2 = f2.read()
            encoding2 = 'windows-1252'

        if content1 == content2:
            print("ok")
            return True
        else:
            print("nok")
            return False
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return False

# Definir los nombres de los archivos
file1 = 'text5.txt'  # Reemplazar con el primer archivo
file2 = 'descomprimido-ec2.txt'  # Reemplazar con el segundo archivo

file1 = sys.argv[1]
file2 = sys.argv[2]

# Comparar los archivos
start_time = time.time()
are_files_identical(file1, file2)
end_time = time.time()
execution_time = end_time - start_time
print(f"Tiempo de ejecución: {execution_time:.2f} segundos")