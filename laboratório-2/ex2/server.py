# Aplicação do servidor
#
# Autores:
#          Marcos Rampaso - 2149435
#          Pedro Costa - 2135663
import socket
import struct
import os
import logging
import threading


HOST = '127.0.0.1'  # Server IP address
PORT = 65432        # Server port
PORTALTERNATIVA = 65435
# Todas as funções dentro do servidor estão com try e except, para que se houver algum erro
# Seja enviado ao cliente um cabeçalho indicando que houve um erro.

# Configurando o logging para enviar mensagens para um arquivo chamado 'logfile.log'


logging.basicConfig(filename='./server_files/server.log', level=logging.INFO)

def add_file(conn, filename, file_size):
    try:
        if not os.path.exists('server_files'):
            os.makedirs('server_files')
        filename = os.path.join('server_files', filename)
        with open(filename, 'wb') as f:
            while file_size:
                chunk = conn.recv(min(file_size, 1024))
                f.write(chunk)
                file_size -= len(chunk)
        f.close()
        logging.info(f'File {filename} added')
        conn.sendall(struct.pack('>BBB', 2, 1, 1))  # SUCCESS
    except:
        conn.sendall(struct.pack('>BBB', 2, 1, 1))  # ERRO
        logging.info(f'Erro no ADDFILE')

#Função para deletar um arquivo do servidor
def delete_file(conn, filename):
    try:
        filename = os.path.join('server_files', filename)
        os.remove(filename)
        logging.info(f'File {filename} deleted')
        conn.sendall(struct.pack('>BBB', 2, 2, 1))  # SUCCESS
    except:
        conn.sendall(struct.pack('>BBB', 2, 2, 2))  # Error
        logging.info(f'Error no DELETEFILE')


#Função para recuperar os arquivos do servidor
def get_files_list(conn):    
    try:
        files = os.listdir('server_files')
        count = len(files)
        resultado_parcial = count.to_bytes(2,'big')
        for file in files:
            resultado_parcial = resultado_parcial + len(file).to_bytes(1, 'big') + file.encode()
        result = struct.pack('>BBB', 2, 3, 1) + resultado_parcial
        conn.sendall(result)
        logging.info('File list sent ')
    except:
        conn.sendall(struct.pack('>BBB', 2, 3, 2))

#Função para envoar o arquivo que será baixado
def get_file(conn, filename):
    filename = os.path.join('server_files', filename)
    try:
        with open(filename, 'rb') as f:
            data = f.read()
        f.close()
        conn.sendall(struct.pack('>BBB', 2, 4, 1))  # SUCCESS
        conn.sendall(struct.pack('>I', len(data)))
        conn.sendall(data)
        logging.info(f'File {filename} sent')
    except:
        conn.sendall(struct.pack('>BBB', 2, 4, 2))  # ERROR

def handle_client(conn, addr):
    logging.info(f'Connected by {addr}')
    while True:
        try:
            msg_type, cmd_id, filename_size = struct.unpack('>BBB', conn.recv(3))
            filename = conn.recv(filename_size).decode()
            if cmd_id == 1:  # ADDFILE
                file_size, = struct.unpack('>I', conn.recv(4))
                print(f"ADDFILE addr = {addr}")
                add_file(conn, filename, file_size)
            elif cmd_id == 2:  # DELETE
                print(f"DELETE addr = {addr}")
                delete_file(conn, filename)
            elif cmd_id == 3:  # GETFILESLIST
                print(f"GETFILESLIST addr = {addr}")
                get_files_list(conn)
            elif cmd_id == 4:  # GETFILE
                print(f"GETFILE addr = {addr}")
                get_file(conn, filename)
        except struct.error:
            break

def start_server():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:                        #testa a porta padrão, caso falhe, testa secundária, caso falhe de novo informa ao log que houve erro.
        server.bind((HOST, PORT))
        server.listen()
    except:
        server.bind(HOST, PORTALTERNATIVA)
        server.listen
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"conexoes ativas: {threading.active_count() - 1}")


start_server()