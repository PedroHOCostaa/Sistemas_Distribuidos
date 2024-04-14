import socket
import struct
import os

HOST = '127.0.0.1'  # Server IP address
PORT = 65435        # Server port

# Função para adicionar um arquivo no servidor
def add_file(s, filename):
    if not os.path.exists('client_files'):
        os.makedirs('client_files')
    full_path = os.path.join('client_files', filename)
    with open(full_path, 'rb') as f:
        data = f.read() # Le o arquivo para enviar ao servidor
    base_filename = os.path.basename(filename)  # Extrai o nome do arquivo do caminho completo
    s.sendall(struct.pack('>BBB', 1, 1, len(base_filename)) + base_filename.encode() + struct.pack('>I', len(data)) + data) # evia o comando ADDFILE para o servidor, conforme o cabeçalho definido

# Funçao para deletar um arquivo no servidor
def delete_file(s, filename):
    s.sendall(struct.pack('>BBB', 1, 2, len(filename)) + filename.encode()) # Envia o comando DELETE para o servidor, conforme o cabeçalho definido

# FUuçao para receber a lista de arquivos do servidor
def get_files_list(s):
    s.sendall(struct.pack('>BBB', 1, 3, 0)) # Envia o comando GETFILESLIST para o servidor, conforme o cabeçalho definido

# Funçao para receber um arquivo do servidor
def get_file(s, filename):
    s.sendall(struct.pack('>BBB', 1, 4, len(filename)) + filename.encode()) # Envia o comando GETFILE para o servidor, conforme o cabeçalho definido

    file_size = struct.unpack('>I', s.recv(4))[0]   # Recebe o tamanho do arquivo onde o servidor envia o tamanho do arquivo, que é um inteiro de 4 bytes
                                                    
    if not os.path.exists('client_files'):          # Verifica se o diretório client_files existe, caso não exista, cria o diretório
        os.makedirs('client_files')

    full_path = os.path.join('client_files', filename) # Define o caminho completo do arquivo
    with open(full_path, 'wb') as f:                   # Abre o arquivo para escrita em binário
        while file_size > 0:                           # Enquanto o tamanho do arquivo for maior que 0
            data = s.recv(min(4096, file_size))        # Recebe os dados do arquivo em pedaços de 4096 bytes
            f.write(data)                              # Escreve os dados no arquivo
            file_size -= len(data)                     # Decrementa o tamanho do arquivo para controlar o loop

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:    # Cria um socket TCP
    s.connect((HOST, PORT))                                     # Conecta ao servidor
    while True:
        command = input("Comandos > (ADDFILE, DELETE, GETFILESLIST, GETFILE) ou 'STOP' para sair: ")
        if command == 'STOP':                            # Se o comando for STOP, encerra a conexão
            print("Encerrando conexao...")
            break
        elif command == 'ADDFILE':
            filename = input("Insira o nome do arquivo: ")
            add_file(s, filename)                      # Chama a função add_file para enviar o arquivo para o servidor
        elif command == 'DELETE':
            filename = input("Insira o nome do arquivo: ")
            delete_file(s, filename)               # Chama a função delete_file para deletar o arquivo no servidor
        elif command == 'GETFILESLIST':
            get_files_list(s)           # Chama a função get_files_list para receber a lista de arquivos do servidor
        elif command == 'GETFILE':
            filename = input("Insira o nome do arquivo: ")
            get_file(s, filename)       # Chama a função get_file para receber um arquivo do servidor
        else:
            print("Comando invalido, os comandos disponiveis sao:")
            continue
        data = s.recv(1024) # Recebe a resposta do servidor
        print(f"Recebido: {data.decode()}")