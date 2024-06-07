import socket
import struct
import hashlib
import os
import logging
import datetime

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT =      65432   # Port to listen on (non-privileged ports are > 1023)

download_dir = os.path.join(os.getcwd(), 'pastaDownload')
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

log_dir = os.path.join(os.getcwd(), 'logFiles')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
logging.basicConfig(filename='./logFiles/server.log', level=logging.INFO)



with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    while True:
        print(f"Esperando por conexão")
        data, address = s.recvfrom(len(b'UPLOAD'))
        tempoInicial = datetime.datetime.now()
        if data == b'UPLOAD':
            print(f"Recebi um pedido de UPLOAD")
            sizeName, sizeFile = struct.unpack('>BI', s.recv(5))
            name = s.recv(sizeName).decode()
            print(f"Tamanho Nome {sizeName} Nome {name} Tamanho Arquivo {sizeFile}")
            sha1 = hashlib.sha1()
            file_path = os.path.join(os.getcwd(), "pastaDownload", name)
            with open(file_path, 'wb') as f:
                sizeFaltante = sizeFile
                while sizeFaltante > 0:
                    data = s.recv(min(1024, sizeFile))
                    f.write(data)
                    sha1.update(data)
                    sizeFaltante -= len(data)
                    print(f"Pacote Recebido com sucesso")
                f.close()
            eof = s.recv(3)
            if eof != b'EOF':
                print(f"Erro na recepção do arquivo")
            checksumCalculado = sha1.hexdigest()
            checksumRecebido = s.recv(40).decode()
            if checksumCalculado == checksumRecebido:
                print(f"Arquivo recebido com sucesso")
            else:
                print(f"Erro na recepção do arquivo")
            tempoFinal = datetime.datetime.now()
            logging.info(f"Horário de início {tempoInicial} e término {tempoFinal}, nome do arquivo: {name}, tamanho do arquivo: {sizeFile} Bytes,origem do arquivo{address}, checksum calculado: {checksumCalculado}, checksum recebido: {checksumRecebido}")
