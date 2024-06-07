# Aplicação do cliente
#
# Autores:
#          Marcos Rampaso - 2149435
#          Pedro Costa - 2135663


import socket
import time
import hashlib

HOST = "127.0.0.1" # (localhost)
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:    # Cria o socket
    s.connect((HOST, PORT)) # Conecta ao servidor
    while True:
        message = input("""Envie a mensagem:Comandos disponíveis: CONNECT, PWD, EXIT, CHDIR, GETFILES, GETDIRS, STOP: \t""") 
        if message == 'STOP':
            break
        words = message.replace(',', ' ').split()   # Substitui as virgulas por ' ' e em seguida separa a string em substrings a cada ' ' assim dividindo em palavras
        if words[0] == 'CONNECT':                   # Se a primeira palavra for CONNECT
            sha512_hash = hashlib.sha512()          
            sha512_hash.update(words[2].encode())   # Atualiza o hash com a senha
            words[2] = sha512_hash.hexdigest()      # Transforma a senha em hash
            message_to_send = ' '.join(words)       # Junta as palavras em uma string para ser enviada
            print(f"Enviando: {message_to_send}")   # Mostra a string que será enviada
            s.sendall(message_to_send.encode())     # Envia a string no mode utf-8
            print(f"Recebido: "+s.recv(7).decode()) # Recebe a resposta do servidor

        elif words[0] == 'PWD':
            s.sendall(message.encode())
            data = s.recv(1024)
            print(f"Recebido: "+data.decode())

        elif words[0] == 'CHDIR':
            s.sendall(message.encode())
            data = s.recv(1024)
            print(f"Recebido: "+data.decode())

        elif words[0] == 'GETFILES':
            s.sendall(message.encode())
            tamanhoQuantidade = int(s.recv(1).decode())
            print(f"tamanhoQuantidade: {tamanhoQuantidade}")
            if tamanhoQuantidade == 0:
                print("Diretório vazio")
            else:
                Quantidade =        int(s.recv(tamanhoQuantidade).decode())
                print(f"Quantidade: {Quantidade}")
                for i in range(Quantidade):
                    tamanhoDoTamanho =  int(s.recv(1).decode())
                    tamanhoDoNome =     int(s.recv(tamanhoDoTamanho).decode())
                    nome =              s.recv(tamanhoDoNome).decode()
                    print(f"Tamanho Do Tamanho {tamanhoDoTamanho} Tamanho Do Nome {tamanhoDoNome} Nome do Arquivo  {nome}")
        
        elif words[0] == 'GETDIRS':
            s.sendall(message.encode())
            tamanhoQuantidade = int(s.recv(1).decode())
            print(f"tamanhoQuantidade: {tamanhoQuantidade}")
            if tamanhoQuantidade == 0:
                print("Diretório vazio")
            else:
                Quantidade =        int(s.recv(tamanhoQuantidade).decode())
                print(f"Quantidade: {Quantidade}")
                for i in range(Quantidade):
                    tamanhoDoTamanho =  int(s.recv(1).decode())
                    tamanhoDoNome =     int(s.recv(tamanhoDoTamanho).decode())
                    nome =              s.recv(tamanhoDoNome).decode()
                    print(f"Tamanho Do Tamanho {tamanhoDoTamanho} Tamanho Do Nome {tamanhoDoNome} Nome do Arquivo  {nome}")

        elif words[0] == 'EXIT':
            s.sendall(message.encode())
            s.close()
            break


        else:
            print(f"Comando invalido: {words[0]}")
        
        time.sleep(0.5)
    
    print('Conexão encerrada...')