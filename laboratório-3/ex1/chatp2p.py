import socket
import threading
import struct


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT1 = 65432  # Port to listen on (non-privileged ports are > 1023)
PORT2 = 65433  # Port to listen on (non-privileged ports are > 1023)

nomes_e_portas = {
    "Nome1": 65432,
    "Nome2": 65433,
    "Nome3": 65434,
    "Nome4": 65435,
    "Nome5": 65436,
    "Nome6": 65437,
}

def Enviar(nameProprio):

    while True:


        alvo = input("Digite o nome do destinatário: ")
        if alvo in nomes_e_portas:
            PORT = nomes_e_portas[alvo]
            print(f"Enviando mensagens para {PORT}")


        while PORT != None:
            tipo = input("digite o tipo de mensagem que deve ser enviada: MSG, ECHO , URL ou EMOJI > ")
            if tipo == "MSG":
                messageType = 0
                message = input("Digite a mensagem a ser enviada: ") + "\n"
                print(f"Enviando mensagem : {message}")
            elif tipo == "ECHO":
                messageType = 1
                message = "ECHO" 
            elif tipo == "URL":
                messageType = 2
                message = input(f"Digite a URL a ser enviada: ")
            elif tipo == "EMOJI":
                messageType = 3
                emote = input(f"Qual emoji deve ser enviado? \n smile\t\t:) \n sad\t\t:( \n bigSmile\t:D\n bigSad\t\t:C\n mid\t\t:|\n cute\t\t:3\n")
                if emote == "smile":
                    message = ":)"
                elif emote == "sad":
                    message = ":("
                elif emote == "bigSmile":
                    message = ":D"
                elif emote == "bigSad":
                    message = ":C"
                elif emote == "mid":
                    message = ":|"
                elif emote == "cute":
                    message = ":3"
                else:
                    print(f"Emoji padrão smile :) selecionado.")
                    message = ":)"

            elif tipo == "EXIT":
                break
            else:
                tipo == "ERRADO"
            if(tipo == "MSG" or tipo == "ECHO" or tipo == "URL" or tipo == "EMOJI"):
                data = struct.pack('>BB', messageType, len(nameProprio)) + nameProprio.encode() + struct.pack('>B', len(message)) + message.encode()
                s.sendto(data, (HOST, PORT))
            tipo = ""

def Receber(nameProprio):
    while True:
        data, addr = s.recvfrom(322)

        if data != None:
            doisPrimeirosCampos = data[:2]
            messageType, tamanhoName = struct.unpack('>BB', doisPrimeirosCampos)

            terceiroCampo = data[2:2+tamanhoName]
            name = terceiroCampo.decode()

            quartoCampo = data[2+tamanhoName:3+tamanhoName]
            tamanhoMessage = struct.unpack('>B', quartoCampo)[0]
            quintoCampo = data[3+tamanhoName:3+tamanhoName+tamanhoMessage]
            message = quintoCampo.decode()
            if messageType == 0:
                print(f"Mensagem recebida de {name}: {message}\n")
            elif messageType == 1:
                print(f"\nRecebido PING de {addr}")
                print(f"Enviando PONG para {addr}")
                data = struct.pack('>BB', 4, len(nameProprio)) + nameProprio.encode() + struct.pack('>B', len("PONG")) + "PONG".encode()
                s.sendto(data, addr)
            elif messageType == 2:
                print(f"\nURL recebida de {name}: {message}")
            elif messageType == 3:
                print(f"\nEmoji recebido de {name}: {message}")
            elif messageType == 4:
                print(f"\nResposta PONG de {addr}")

       

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:

    nameProprio = input("Digite seu nome: ")
    PORT = nomes_e_portas[nameProprio]
    s.bind((HOST, PORT))

    threadRecev = threading.Thread(target=Receber, args=(nameProprio,))
    threadRecev.start()
    threadEnv = threading.Thread(target=Enviar, args=(nameProprio,))
    threadEnv.start()
    
    while True:
        pass