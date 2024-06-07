import socket
import struct
import os 
import hashlib
import time
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import math

HOST =          "127.0.0.1"  # Standard loopback interface address (localhost)
PORTDESTINO =       65432   # Port to listen on (non-privileged ports are > 1023)

#|=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-|#    
#|  Preambulo(6)(b'UPLOAD')                                                             |#
#|  Tamanho do Nome(1) | Nome(Tamanho do Nome) | Tamanho Arquivo(4)                     |#
#|  Pacote de Dados(Maximo 1024) | Repetir até que o arquivo seja enviado por completo  |#
#|  EOF(3)(b'EOF') | Checksum(40)                                                       |#
#|=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-|#    



class Barra:
    def __init__(self, numero):
        self.__porcentagemTotal = math.ceil(numero)
        self.__porcentagemAtual = 0

    def incrementa(self):
        self.__porcentagemAtual += 1
        self.mostra_barra()

    def mostra_barra(self):
        proporcao_completa = self.__porcentagemAtual / self.__porcentagemTotal
        proporcao_faltante = 1 - proporcao_completa

        barra_completa = '|' * int(proporcao_completa * 40)
        barra_faltante = '-' * int(proporcao_faltante * 40)

        print(f"Progresso: {barra_completa}{barra_faltante}")

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    Tk().withdraw()
    path = askopenfilename()
    filename = os.path.basename(path)
    print(f'Arquivo selecionado: {filename} esta em {path}')
    if not os.path.exists(path):
        print(f"O arquivo {filename} não existe")
        exit(0)
    with open(path, "rb") as file:
        sizeName = len(filename.encode())
        size = os.path.getsize(path)
        sizeAtual = size
        s.sendto(b'UPLOAD', (HOST,PORTDESTINO))
        s.sendto(struct.pack('>BI',sizeName, size), (HOST,PORTDESTINO))
        s.sendto(filename.encode(), (HOST,PORTDESTINO))
        sha1 = hashlib.sha1()
        barra = Barra(size/1024)
        while sizeAtual > 0:
            barra.incrementa()
            data = file.read(min(1024, sizeAtual))
            s.sendto(data, (HOST,PORTDESTINO))
            print(f"Pacote Enviado enviado com sucesso")
            sizeAtual -= len(data)
            time.sleep(0.01)
            
        s.sendto(b"EOF", (HOST,PORTDESTINO))
        file.seek(0)  # Go back to the start of the file
        sha1.update(file.read())  # Read the whole file and update the SHA1
        checksum = sha1.hexdigest()
        print(f"Checksum: {checksum}")
        s.sendto(checksum.encode(), (HOST,PORTDESTINO))
    file.close()

