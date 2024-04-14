import socket
import time
import hashlib

HOST = "127.0.0.1" # (localhost)
PORT = 65435

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:    # Cria o socket
    s.connect((HOST, PORT)) # Conecta ao servidor
    while True:
        message = input("""Envie a mensagem:
        Comandos disponíveis: CONNECT, PWD, EXIT, CHDIR, GETFILES, GETDIRS, STOP
        """) 
        if message == 'STOP':
            break
        words = message.replace(',', ' ').split()  # Divide a mensagem em palavras
        if words[0] == 'CONNECT':   # Se a primeira palavra for CONNECT
            sha512_hash = hashlib.sha512()  
            sha512_hash.update(words[2].encode())
            words[2] = sha512_hash.hexdigest()  # Transforma a senha em hash
        message_to_send = ' '.join(words)  #  Junta as palavras em uma mensagem
        print(f"Enviando: {message_to_send}")    # Mostra a mensagem enviada
        s.sendall(message_to_send.encode())
        data = s.recv(1024)
        print(f"Recebido: "+data.decode())
        if data.decode() == 'EXIT':
            break
        time.sleep(0.5)
print('Conexão encerrada...')