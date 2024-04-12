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


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65435  # Port to listen on (non-privileged ports are > 1023)

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    while True:
        data = conn.recv(1024)
        
        if not data:
            break
        
        print(f"Received {repr(data)} from {addr}")
        words = data.decode().split()  # Split the message into words
        
        if words[0] == 'CONNECT':
            if words[1] in users and words[2] == users[words[1]]:
                messagetosend = 'SUCCESS'
            else:
                messagetosend = 'ERROR'             
            conn.sendall(messagetosend.encode())
        else:
            if words[0] == 'PWD':
                messagetosend = os.getcwd()
                conn.sendall(messagetosend.encode())

            else:
                if words[0] == 'EXIT':
                    messagetosend = 'EXIT'
                    conn.sendall(messagetosend.encode())
                    conn.close()
                    break
                else:
                    if words[0] == 'CHDIR':
                        try:
                            os.chdir(words[1])
                            messagetosend = 'SUCCESS'
                        except OSError:
                            messagetosend = 'ERROR'
                        conn.sendall(messagetosend.encode())
                    else:
                        if words[0] == 'GETFILES':
                            files = [name for name in os.listdir('.') if os.path.isfile(name)]
                            if not files:
                                messagetosend = 'No files found'
                            else:
                                messagetosend = ', '.join(files)
                            conn.sendall(messagetosend.encode())
                        else:
                            if words[0] == 'GETDIRS':
                                directories = [name for name in os.listdir('.') if os.path.isdir(name)]
                                if not directories:
                                    messagetosend = 'No directories found'
                                else:
                                    messagetosend = ', '.join(directories)
                                conn.sendall(messagetosend.encode())

def start_server():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))                                           
    server.listen()
    print(f"Server is listening on {HOST}:{PORT}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"Active connections: {threading.activeCount() - 1}")

start_server()