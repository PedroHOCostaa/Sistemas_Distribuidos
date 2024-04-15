# echo-server.py

import socket
import threading
import hashlib
import os

#Dicionario com os usuarios e senhas
users = {
    "pedro"     :   hashlib.sha512(b"123mudar").hexdigest(),    
    "marcos"    :   hashlib.sha512(b"123mudar").hexdigest(),
    "campiolo"  :   hashlib.sha512(b"123mudar").hexdigest(),
}


HOST = "127.0.0.1"  # (localhost)
PORT = 65435

def handle_client(conn, addr):     # Função que lida com o cliente
    print(f"Connected by {addr}")  # Mostra o endereço do cliente
    while True:                    # Loop para receber mensagens do cliente
        data = conn.recv(1024)     # Recebe a mensagem do cliente
        
        if not data:               # Se não houver mensagem, encerra a conexão
            break
        
        print(f"Recebido {repr(data)} do endereco: {addr}")     # Mostra a mensagem recebida
        words = data.decode().split()  # Separa a mensagem em palavras
        
        if words[0] == 'CONNECT':   # Se a primeira palavra for CONNECT
            if words[1] in users and words[2] == users[words[1]]:   # Se o usuário e senha estiverem corretos
                messagetosend = 'SUCCESS'               # Envia a mensagem de sucesso
            else:                                       # Se o usuário ou senha estiverem incorretos
                messagetosend = 'ERROR'                 # Envia a mensagem de erro
            conn.sendall(messagetosend.encode())        
        else:
            if words[0] == 'PWD':                       # Se a primeira palavra for PWD
                messagetosend = os.getcwd()             # Envia o diretório atual
                conn.sendall(messagetosend.encode())    # Envia a mensagem

            else:
                if words[0] == 'EXIT':                  # Se a primeira palavra for EXIT
                    messagetosend = 'EXIT'                  
                    conn.sendall(messagetosend.encode())# Envia a mensagem de saída
                    conn.close()                        # Encerra a conexão
                    break
                else:
                    if words[0] == 'CHDIR':             # Se a primeira palavra for CHDIR
                        try:                            # Tenta mudar de diretório
                            os.chdir(words[1])          # Muda de diretório
                            messagetosend = 'SUCCESS'   # Envia a mensagem de sucesso
                        except OSError:                 # Se houver erro
                            messagetosend = 'ERROR'     # Envia a mensagem de erro
                        conn.sendall(messagetosend.encode())    #Envia a mensagem
                    else:
                        if words[0] == 'GETFILES':      # Se a primeira palavra for GETFILES
                            files = [name for name in os.listdir('.') if os.path.isfile(name)]  # Lista os arquivos
                            if not files:               # Se não houver arquivos
                                messagetosend = 'Nao foram eoncontrados arquivos'
                            else:
                                messagetosend = ', '.join(files)    # Envia a lista de arquivos
                            conn.sendall(messagetosend.encode())
                        else:
                            if words[0] == 'GETDIRS': # Se a primeira palavra for GETDIRS
                                directories = [name for name in os.listdir('.') if os.path.isdir(name)] # Lista os diretórios
                                if not directories:
                                    messagetosend = 'Nao foram encontrados diretorios'
                                else:
                                    messagetosend = ', '.join(directories) # Envia a lista de diretórios
                                conn.sendall(messagetosend.encode())

# Função para iniciar o servidor
def start_server():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria o socket de conexão TCP 
    server.bind((HOST, PORT))                                   # Associa o socket ao endereço e porta    
    server.listen()                                             # Habilita o servidor para aceitar conexões
    print(f"Server is listening on {HOST}:{PORT}")              # Mostra que o servidor está ativo
    while True:
        conn, addr = server.accept()                            # Aceita a conexão do cliente
        thread = threading.Thread(target=handle_client, args=(conn, addr))  #Cria uma thread para lidar com o cliente permitindo que o servidor continue aceitando conexões
        thread.start()                                         # Inicia a thread
        print(f"conexoes ativas: {threading.activeCount() - 1}")  # Mostra o número de conexões ativas

start_server()