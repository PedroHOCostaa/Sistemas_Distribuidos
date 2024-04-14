import socket
import struct
import os
import logging

HOST = '127.0.0.1'  # Server IP address
PORT = 65435        # Server port

def add_file(conn, filename, file_size):
    if not os.path.exists('server_files'):
        os.makedirs('server_files')
    filename = os.path.join('server_files', filename)
    with open(filename, 'wb') as f:
        while file_size:
            chunk = conn.recv(min(file_size, 1024))
            f.write(chunk)
            file_size -= len(chunk)
    logging.info(f'File {filename} added')
    conn.sendall(struct.pack('>BBB', 2, 1, 1))  # SUCCESS

def delete_file(conn, filename):
    filename = os.path.join('server_files', filename)
    os.remove(filename)
    logging.info(f'File {filename} deleted')
    conn.sendall(struct.pack('>BBB', 2, 2, 1))  # SUCCESS

def get_files_list(conn):
    files = os.listdir('server_files')
    for file in files:
        conn.sendall(file.encode() + b'\n')
    logging.info('File list sent')
    conn.sendall(struct.pack('>BBB', 2, 3, 1))  # SUCCESS

def get_file(conn, filename):
    filename = os.path.join('server_files', filename)
    with open(filename, 'rb') as f:
        data = f.read()
    conn.sendall(struct.pack('>I', len(data)))
    conn.sendall(data)
    logging.info(f'File {filename} sent')
    conn.sendall(struct.pack('>BBB', 2, 4, 1))  # SUCCESS

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    while True:
        conn, addr = server.accept()
        with conn:
            logging.info(f'Connected by {addr}')
            while True:
                try:
                    msg_type, cmd_id, filename_size = struct.unpack('>BBB', conn.recv(3))
                    filename = conn.recv(filename_size).decode()
                    if cmd_id == 1:  # ADDFILE
                        file_size, = struct.unpack('>I', conn.recv(4))
                        add_file(conn, filename, file_size)
                    elif cmd_id == 2:  # DELETE
                        delete_file(conn, filename)
                    elif cmd_id == 3:  # GETFILESLIST
                        get_files_list(conn)
                    elif cmd_id == 4:  # GETFILE
                        get_file(conn, filename)
                except struct.error:
                    break

if __name__ == '__main__':
    start_server()