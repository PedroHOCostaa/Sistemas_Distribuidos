import socket
import time
import hashlib

HOST = "127.0.0.1"
PORT = 65435

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        message = input("Enter message to send or 'STOP' to quit: ")
        if message == 'STOP':
            break
        words = message.replace(',', ' ').split()  # Split the message into words
        if words[0] == 'CONNECT':
            sha512_hash = hashlib.sha512()
            sha512_hash.update(words[2].encode())
            words[2] = sha512_hash.hexdigest()  # Replace the third word with its SHA512 hash
        message_to_send = ' '.join(words)  # Join the words with a space
        print(f"Sending: {message_to_send}")
        s.sendall(message_to_send.encode())
        data = s.recv(1024)
        print(f"Received "+data.decode())
        if data.decode() == 'EXIT':
            break